<div align="center" style="display: flex; flex-direction: column; justify-content: center;">
    <a style="align-self: center" href="https://launchflow.com/#gh-dark-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-dark.png#gh-dark-mode-only">
    </a>
    <a style="align-self: center" href="https://launchflow.com/#gh-light-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-light.svg#gh-light-mode-only">
    </a>
    <div style="display: flex; align-content: center; gap: 4px; justify-content: center; margin-top: 12px; margin-bottom: 12px;  border-bottom: none;">
        <h1 style="margin-top: 0px; margin-bottom: 0px; border-bottom: none;">
            Deploy FastHTML + Postgres on AWS
        </h1>
    </div>
</div>
<div style="text-align: center;" align="center">

📖 [LaunchFlow Docs](https://docs.launchflow.com/) &nbsp; | &nbsp; ⚡ [LaunchFlow Quickstart](https://docs.launchflow.com/docs/get-started) &nbsp; | &nbsp; 👋 [LaunchFlow Slack](https://join.slack.com/t/launchflowusers/shared_invite/zt-27wlowsza-Uiu~8hlCGkvPINjmMiaaMQ)

</div>

## ℹ️ Project Info

Deploy FastHTML to [ECS Fargate on AWS](https://aws.amazon.com/fargate/) using [LaunchFlow](https://launchflow.com/).

This project will configure the following AWS resources in your AWS account:
- Docker Repository hosted on [AWS ECR](https://aws.amazon.com/ecr/)
- A Docker build pipeline hosted on [AWS CodeBuild](https://aws.amazon.com/codebuild)
- Serverless FastHTML app hosted on [AWS ECS Fargate](https://aws.amazon.com/ecs/)
- A Postgres database hosted on [AWS RDS](https://aws.amazon.com/rds/)

## ⚙️ Prerequisites

### Install the requirements
```bash
pip install -r requirements.txt
```

<strong>NOTE:</strong> This will install the LaunchFlow Python SDK + CLI

### Authenticate with AWS

You can authenticate with AWS using the [AWS CLI](https://aws.amazon.com/cli/). 

You can check if you are authenticated by running the following command:
```bash
aws sts get-caller-identity
```

## ⚒️ Create AWS infrastructure

### Automatically find and create all infrastructure used in your code

```bash
lf create
```

Learn how the `lf create` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-create).

## 🏃 Run locally

### Run the FastHTML app locally using [Uvicorn](https://www.uvicorn.org/).

```bash
lf run {your environment name} -- uvicorn app.main:app --reload
```

## 🗑️ Drop / recreate the Postgres tables

### Run the utility defined in [crud.py](/fasthtml-postgres/aws/app/crud.py) to drop / recreate the database in a given environment.

```bash
lf run {your environment name} -- python app/crud.py
```

## 🚀 Deploy to AWS

### Automatically <strong>build</strong> and <strong>deploy</strong> the FastAPI application to AWS ECS Fargate

```bash
lf deploy
```

Learn how the `lf deploy` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-deploy).

## 🧹 Clean up your infrastructure

### Automatically delete infrastructure used by your application.

```bash
lf destroy
```

Learn how the `lf destroy` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-destroy).

