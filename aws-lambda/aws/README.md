<div align="center" style="display: flex; flex-direction: column; justify-content: center;">
    <a style="align-self: center" href="https://launchflow.com/#gh-dark-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-dark.png#gh-dark-mode-only">
    </a>
    <a style="align-self: center" href="https://launchflow.com/#gh-light-mode-only" target="_blank">
        <img  height="auto" width="270" src="https://storage.googleapis.com/launchflow-public-images/launchflow-logo-light.svg#gh-light-mode-only">
    </a>
    <div style="display: flex; align-content: center; gap: 4px; justify-content: center; margin-top: 12px; margin-bottom: 12px;  border-bottom: none;">
        <h1 style="margin-top: 0px; margin-bottom: 0px; border-bottom: none;">
            Deploy AWS Lambdas with LaunchFlow
        </h1>
    </div>
</div>
<div style="text-align: center;" align="center">

📖 [LaunchFlow Docs](https://docs.launchflow.com/) &nbsp; | &nbsp; ⚡ [LaunchFlow Quickstart](https://docs.launchflow.com/docs/get-started) &nbsp; | &nbsp; 👋 [LaunchFlow Slack](https://join.slack.com/t/launchflowusers/shared_invite/zt-27wlowsza-Uiu~8hlCGkvPINjmMiaaMQ)

</div>

## ℹ️ Project Info

3 examples of AWS Lambda functions that can be deployed using LaunchFlow:
1. [Lambda in VPC](/aws-lambda/aws/example-1)
2. [Lambda + RDS (mysql) in VPC](/aws-lambda/aws/example-2)
3. [Lambda + RDS (mysql) in VPC with public internet access](/aws-lambda/aws/example-3)

This project will configure the following AWS resources in your AWS account:
- MySQL database hosted on [AWS RDS](https://aws.amazon.com/rds/)
- [API Gateway](https://aws.amazon.com/api-gateway/) to expose the Lambda functions as HTTP endpoints
- [Lambda functions](https://aws.amazon.com/lambda/) that interact with the RDS database and Redis cache
- [NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html) to allow the Lambda functions to access the internet

## ⚙️ Prerequisites

NOTE: Make sure you cd into the example directory you want to deploy before running the commands below.

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

