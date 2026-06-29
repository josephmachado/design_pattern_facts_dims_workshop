from pyspark.sql import DataFrame, SparkSession

TABLE_NAME = "local.silver.dim_customer_v2"


def extract(spark: SparkSession) -> dict[str, DataFrame]:
    customer_df = spark.sql("""
    SELECT *
    FROM prod.db.customer
    """)

    dim_mktsegment_df = spark.sql("""
    SELECT *
    FROM prod.db.dim_mktsegment
    """)

    return {"customer": customer_df, "dim_mktsegment": dim_mktsegment_df}


def transform(input_dfs: dict[str, DataFrame]) -> DataFrame:
    input_dfs['customer'].createOrReplaceTempView('customer')
    input_dfs['dim_mktsegment'].createOrReplaceTempView('dim_mktsegment')
    return spark.sql("""
        SELECT
          c.c_custkey,
          c.c_name,
          c.c_address,
          c.c_nationkey,
          c.c_phone,
          c.c_acctbal,
          c.c_mktsegment,
          c.c_comment,
          s.segment_description,
          s.priority_tier
        FROM customer c
        LEFT JOIN dim_mktsegment s
          ON c.c_mktsegment = s.c_mktsegment
    """)


def load(output_df: DataFrame, spark: SparkSession) -> None:
    output_df.writeTo(TABLE_NAME).createOrReplace()


def run(spark: SparkSession) -> None:
    load(transform(extract(spark)), spark)


if __name__ == "__main__":
    spark = SparkSession.builder.appName(TABLE_NAME).master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    run(spark)