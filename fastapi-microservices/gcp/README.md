<div align="center" style="display: flex; flex-direction: column; justify-content: center;">
    <a style="align-self: center" href="https://launchflow.com/#gh-dark-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-dark.png#gh-dark-mode-only">
    </a>
    <a style="align-self: center" href="https://launchflow.com/#gh-light-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-light.svg#gh-light-mode-only">
    </a>
    <div style="display: flex; align-content: center; gap: 4px; justify-content: center; margin-top: 12px; margin-bottom: 12px;  border-bottom: none;">
        <h1 style="margin-top: 0px; margin-bottom: 0px; border-bottom: none;">
            Example FastAPI Microservices on GCP
        </h1>
    </div>
</div>
<div style="text-align: center;" align="center">

📖 [LaunchFlow Docs](https://docs.launchflow.com/) &nbsp; | &nbsp; ⚡ [LaunchFlow Quickstart](https://docs.launchflow.com/docs/get-started) &nbsp; | &nbsp; 👋 [LaunchFlow Slack](https://join.slack.com/t/launchflowusers/shared_invite/zt-27wlowsza-Uiu~8hlCGkvPINjmMiaaMQ)

</div>

## ℹ️ Project Info

An example FastAPI microservices project that deploys to [GCP Cloud Run](https://cloud.google.com/run) using [LaunchFlow](https://launchflow.com/).

## ⚙️ Prerequisites

### Install the requirements

Service 1:
```bash
pip install -r service1/requirements.txt
```

Service 2:
```bash
pip install -r service2/requirements.txt
```

<strong>NOTE:</strong> The starting requirements for Service 1 and 2 are the same, so you only need to install one of them to get started.

### Authenticate with GCP
```bash
gcloud auth application-default login
```
<strong>NOTE:</strong> You will need the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed to authenticate with GCP


## ⚒️ Create your Infrastructure

### Automatically find and create all infrastructure used in your code

```bash
lf create
```

Learn how the `lf create` command works in the [CLI Reference Docs](https://docs.launchflow.com/reference/cli#launchflow-create).


## 🏃 Run your Services (local)

Run the FastAPI services locally using [Uvicorn](https://www.uvicorn.org/).

Service 1:
```bash
lf run {your env} -- uvicorn service1.app.main:app --reload
```

Service 2:
```bash
lf run {your env} -- uvicorn service2.app.main:app --reload
```

## 🚀 Deploy your Services (remote)

### Automatically <strong>build</strong> and <strong>deploy</strong> both FastAPI services to GCP Cloud Run

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

