<div style="display: flex; flex-direction: column; justify-content: center;">
    <a style="align-self: center" href="https://launchflow.com/" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-dark.png#gh-dark-mode-only">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-light.svg#gh-light-mode-only">
    </a>
    <div style="display: flex; align-content: center; gap: 4px; justify-content: center; margin-top: 12px; margin-bottom: 12px;">
        <h1 style="margin-top: 0px; margin-bottom: 0px; border-bottom: none;">
            Example FastAPI Microservices on AWS
        </h1>
    </div>
</div>
<div style="text-align: center;">

📖 [LaunchFlow Docs](https://docs.launchflow.com/) &nbsp; | &nbsp; ⚡ [LaunchFlow Quickstart](https://docs.launchflow.com/docs/get-started) &nbsp; | &nbsp; 👋 [LaunchFlow Slack](https://join.slack.com/t/launchflowusers/shared_invite/zt-27wlowsza-Uiu~8hlCGkvPINjmMiaaMQ)

</div>

## ℹ️ Project Info

An example FastAPI microservices project that deploys to [ECS Fargate on AWS](https://aws.amazon.com/fargate/) using [LaunchFlow](https://launchflow.com/).

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

### Authenticate with AWS

You can authenticate with AWS using the [AWS CLI](https://aws.amazon.com/cli/). 

You can check if you are authenticated by running the following command:
```bash
aws sts get-caller-identity
```

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


## 🏃 Run your Services (local)

Run the FastAPI services locally using [Uvicorn](https://www.uvicorn.org/).

Service 1:
```bash
lf run {your environment name} -- uvicorn service1.app.main:app --reload
```

Service 2:
```bash
lf run {your environment name} -- uvicorn service2.app.main:app --reload
```

## 🚀 Deploy your Services (remote)

### Automatically <strong>build</strong> and <strong>deploy</strong> both FastAPI services to AWS ECS Fargate

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

