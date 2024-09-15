import launchflow as lf

# ECSFargate Docs: https://docs.launchflow.com/reference/aws-services/ecs-fargate
service = lf.aws.ECSFargate(
    "my-ecs-java",
    dockerfile="Dockerfile",  # Path to your Dockerfile
)
