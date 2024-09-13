"""infra.py

This file is used to customize the infrastructure your application deploys to.

Create your cloud infrastructure with:
    lf create

Deploy your application with:
    lf deploy

For more information, visit https://docs.launchflow.com/docs/user-guides/project-structure
"""

import launchflow as lf

# ECSFargate Docs: https://docs.launchflow.com/reference/aws-services/ecs-fargate
service = lf.aws.ECSFargate(
    "my-ecs-service",
    dockerfile="Dockerfile",  # Path to your Dockerfile
)
