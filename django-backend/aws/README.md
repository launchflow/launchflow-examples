<div align="center" style="display: flex; flex-direction: column; justify-content: center;">
    <a style="align-self: center" href="https://launchflow.com/#gh-dark-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-dark.png#gh-dark-mode-only">
    </a>
    <a style="align-self: center" href="https://launchflow.com/#gh-light-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-light.svg#gh-light-mode-only">
    </a>
    <div style="display: flex; align-content: center; gap: 4px; justify-content: center; margin-top: 12px; margin-bottom: 12px;  border-bottom: none;">
        <h1 style="margin-top: 0px; margin-bottom: 0px; border-bottom: none;">
            Example Django Backend on AWS
        </h1>
    </div>
</div>
<div style="text-align: center;" align="center">

📖 [LaunchFlow Docs](https://docs.launchflow.com/) &nbsp; | &nbsp; ⚡ [LaunchFlow Quickstart](https://docs.launchflow.com/docs/get-started) &nbsp; | &nbsp; 👋 [LaunchFlow Slack](https://join.slack.com/t/launchflowusers/shared_invite/zt-27wlowsza-Uiu~8hlCGkvPINjmMiaaMQ)

</div>

## ℹ️ Project Info

An example Django backend that deploys to [ECS Fargate on AWS](https://aws.amazon.com/fargate/) using [LaunchFlow](https://launchflow.com/).

This project will configure the following AWS resources in your AWS account:
- Postgres database hosted on [AWS RDS](https://aws.amazon.com/rds/)
- Redis cache hosted on [AWS Elasticache](https://aws.amazon.com/elasticache/)
- Static files hosted on a [S3 Bucket](https://aws.amazon.com/s3/)

<strong>NOTE:</strong> The AWS infrastructure is defined in [infra.py](/django-backend/aws/app/infra.py)

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


## ⚒️ Create your Infrastructure

### Automatically find and create all infrastructure used in your code

```bash
lf create
```

Learn how the `lf create` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-create).

## 📦 Setup Django

Django applications require a few steps to get started.

### Create and apply the database migrations

```bash
python manage.py makemigrations && python manage.py migrate
```

### Add yourself as a superuser to the Django application

```bash
python manage.py createsuperuser
```

### Load static files used by the Django Admin UI (CSS, JS, images)

```bash
python manage.py collectstatic
```

## 🏃 Run your Application (local)

Run the Django application locally using [Django's Development Server](https://docs.djangoproject.com/en/5.0/intro/tutorial01/#the-development-server).

```bash
lf run {your env} -- python manage.py runserver 127.0.0.1:8000
```

<strong>NOTE:</strong> The Django Development Server is not suitable for production. The [Dockerfile](/django-backend/aws/Dockerfile) uses [Gunicorn](https://gunicorn.org/) instead.

## 🚀 Deploy your Application (remote)

### Automatically <strong>build</strong> and <strong>deploy</strong> the Django application to AWS ECS Fargate

```bash
lf deploy
```

Learn how the `lf deploy` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-deploy).

## 🧹 Clean up your infrastructure

### Automatically delete all infrastructure used by your application.

```bash
lf destroy
```

Learn how this command works in the [LaunchFlow Docs](https://docs.launchflow.com/reference/cli#launchflow-clean).

Learn how the `lf destroy` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-destroy).

