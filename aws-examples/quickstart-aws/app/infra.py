import launchflow as lf
from launchflow.aws.codebuild_project import (
    CodeBuildProject,
    Environment,
    Source,
    EnvironmentVariable,
    LogsConfig,
    CloudWatchLogsConfig,
)
from launchflow.flows.lf_cloud_migration import migrate
from launchflow.config import config
from launchflow.backend import LaunchFlowBackend

# Docs: https://docs.launchflow.com/reference/aws-resources/s3-bucket
# bucket = lf.aws.S3Bucket(f"launchflow-bucket-{lf.environment}", force_destroy=True)
ecr = lf.aws.ECRRepository("my-repo")
project = CodeBuildProject(
    "my-cbp",
    build_timeout_minutes=15,
    environment=Environment(
        compute_type="BUILD_GENERAL1_SMALL",
        type="LINUX_CONTAINER",
        image="aws/codebuild/standard:7.0",
        privileged_mode=True,
        environment_variables=[EnvironmentVariable(name="ECR_NAME", value=ecr.name)],
    ),
    logs_config=LogsConfig(cloud_watch_logs=CloudWatchLogsConfig(status="DISABLED")),
    build_source=Source(type="NO_SOURCE", buildspec_path="buildspec.yaml"),
)
project.depends_on = [ecr]
service = lf.aws.ECSFargate("my-service")
