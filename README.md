# README

> [!WARNING]
> 
> If you find an error when doing `just up`. It is likely due to this repo using an old Spark version. Go to [Dockerfile](./Dockerfile) and update the `RUN wget ` to use the dlcn version.

Start docker containers as shown below:

```bash
just restart # restart docker containers
sleep 30 # waith 30s for services to catchup
just nb # opens notebook
```

