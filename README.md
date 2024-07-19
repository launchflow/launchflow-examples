[LaunchFlow Logo](https://storage.googleapis.com/launchflow-public-images/launchflow-logo-dark.png#gh-dark-mode-only)

[LaunchFlow Logo](https://storage.googleapis.com/launchflow-public-images/launchflow-logo-light.svg#gh-light-mode-only)

<div style="display: flex; flex-direction: column; justify-content: center;">
    <div style="display: flex; align-content: center; gap: 4px; justify-content: center; margin-top: 12px; margin-bottom: 12px;">
        <h1 style="margin-top: 0px; margin-bottom: 0px; border-bottom: none;">
            Example Django Backend on GCP
        </h1>
    </div>
</div>
<div style="text-align: center;">

📖 [LaunchFlow Docs](https://docs.launchflow.com/) &nbsp; | &nbsp; ⚡ [LaunchFlow Quickstart](https://docs.launchflow.com/docs/get-started) &nbsp; | &nbsp; 👋 [LaunchFlow Slack](https://join.slack.com/t/launchflowusers/shared_invite/zt-27wlowsza-Uiu~8hlCGkvPINjmMiaaMQ)

</div>

## ℹ️ Project Info

An example Django backend that deploys to [GCP Cloud Run](https://cloud.google.com/run/docs) using [LaunchFlow](https://launchflow.com/).

This project will create the following GCP resources in your GCP account:
- Postgres database hosted on [GCP CloudSQL](https://cloud.google.com/sql/docs)
- Redis cache hosted on [GCP Memorystore](https://cloud.google.com/memorystore/docs)
- Static files hosted on a [GCS Bucket](https://cloud.google.com/storage/docs)

<strong>NOTE:</strong> The GCP infrastructure is defined in [infra.py](/django-backend/gcp/django_backend/infra.py)

## ⚙️ Prerequisites

### Install the requirements
```bash
pip install -r requirements.txt
```

<strong>NOTE:</strong> This will install the LaunchFlow Python SDK + CLI

### Authenticate with GCP
```bash
gcloud auth application-default login
```
<strong>NOTE:</strong> You will need the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed to authenticate with GCP


## ⚒️ Create your Infrastructure

### Initialize LaunchFlow in your project directory

```bash
lf init
```

Learn how the `lf init` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-init).

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
lf run -- python manage.py runserver 127.0.0.1:8000
```

<strong>NOTE:</strong> The Django Development Server is not suitable for production. The [Dockerfile](/django-backend/gcp/Dockerfile) uses [Gunicorn](https://gunicorn.org/) instead.

## 🚀 Deploy your Application (remote)

### Automatically <strong>build</strong> and <strong>deploy</strong> the Django application to GCP Cloud Run

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

