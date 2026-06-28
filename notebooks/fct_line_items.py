import argparse

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

TABLE_NAME = "local.silver.fct_lineitem"


def extract(
    spark: SparkSession,
    start_time: str,
    end_time: str,
) -> dict[str, DataFrame]:
    lineitem_df = spark.sql(f"""
    SELECT *
    FROM prod.db.lineitem
    WHERE l_shipdate >= '{start_time}'
    AND l_shipdate < '{end_time}'
    """)

    dim_date_df = spark.sql("""
    SELECT *
    FROM prod.db.dim_date
    """)

    return {"lineitem": lineitem_df, "dim_date": dim_date_df}


def transform(input_dfs: dict[str, DataFrame]) -> DataFrame:
    input_dfs['lineitem'].createOrReplaceTempView('lineitem')
    input_dfs['dim_date'].createOrReplaceTempView('dim_date')
    return spark.sql("""
        SELECT
          l.l_orderkey,
          l.l_partkey,
          l.l_suppkey,
          l.l_linenumber,
          l.l_quantity,
          l.l_extendedprice,
          l.l_discount,
          l.l_tax,
          l.l_returnflag,
          l.l_linestatus,
          l.l_shipdate,
          l.l_commitdate,
          l.l_receiptdate,
          l.l_shipinstruct,
          l.l_shipmode,
          l.l_comment,
          l.l_extendedprice * (1 - l.l_discount) AS net_amount,
          l.l_extendedprice * (1 - l.l_discount) * (1 + l.l_tax) AS net_amount_with_tax,
          d.date_key,
          d.year,
          d.quarter,
          d.quarter_name,
          d.month,
          d.month_name,
          d.day_of_month,
          d.day_name,
          d.week_of_year,
          d.iso_week,
          d.is_weekend,
          d.is_holiday,
          d.holiday_name
        FROM lineitem l
        LEFT JOIN dim_date d
          ON l.l_shipdate = d.full_date
    """)


def load(output_df: DataFrame, spark: SparkSession) -> None:

    if not spark.catalog.tableExists(TABLE_NAME):
        (
            output_df.writeTo(TABLE_NAME)
            .partitionedBy(F.partitioning.days("l_shipdate"))
            .createOrReplace()
        )
    else:
        output_df.writeTo(TABLE_NAME).overwritePartitions()


def run(spark: SparkSession, start_time: str, end_time: str) -> None:
    load(transform(extract(spark, start_time, end_time)), spark)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{TABLE_NAME} ETL")
    parser.add_argument(
        "--start-time",
        required=True,
        help="Start time (inclusive), format: YYYY-MM-DD HH:MM:SS",
    )
    parser.add_argument(
        "--end-time",
        required=True,
        help="End time (exclusive), format: YYYY-MM-DD HH:MM:SS",
    )
    args = parser.parse_args()

    spark = SparkSession.builder.appName(TABLE_NAME).master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    run(spark, args.start_time, args.end_time)