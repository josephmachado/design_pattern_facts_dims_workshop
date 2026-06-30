# Design Patterns: Fact & Dimension Pipelines

## YouTube Live Workshop

[![YouTube Live workshop](https://img.youtube.com/vi/AXtcWgvCUtw/0.jpg)](https://www.youtube.com/live/AXtcWgvCUtw)

## Setup 

### CodeSpaces Setup (Recommended)

**Prerequisites**

1. [GitHub Account](https://github.com/)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/josephmachado/simple_dbt_project)

> [!NOTE]
> Wait about 5 minutes for all packages to be automatically installed

Open notebook at [./notebooks/workshop.ipynb](./notebooks/workshop.ipynb)

### Local Setup

**Prerequisites**

1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
**Windows users**: Please use WSL and Install Ubuntu using this [document](https://documentation.ubuntu.com/wsl/stable/howto/install-ubuntu-wsl2/#). In your ubuntu terminal install the prerequisites above.

Clone the repo & start the containers as shown below.

```bash 
git clone https://github.com/josephmachado/design_pattern_facts_dims_workshop.git
cd design_pattern_facts_dims_workshop
docker compose up -d --build
sleep 30 # sleep 30 seconds to wait for the container and its services to fully start
```

#### Running code 

Open Jupyter Lab at [http://localhost:8888](http://localhost:8888)

Open workshop notebook at [./notebooks/workshop.ipynb](./notebooks/workshop.ipynb)

## Switch off codespaces 

> [!CAUTION]
> Do not forget to stop your codespaces machine

## Troubleshooting 

> [!WARNING]
> 
> If you find an error when doing `just up`. It is likely due to this repo using an old Spark version. Go to [Dockerfile](./Dockerfile) and update the `RUN wget ` to use the dlcn version.

