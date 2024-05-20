import launchflow as lf

# Docs: https://docs.launchflow.com/reference/gcp-resources/cloud-sql
postgres = lf.aws.EC2Postgres("launchflow-sample-db")

# Docs: https://docs.launchflow.com/reference/gcp-resources/gcs-bucket
storage_bucket = lf.aws.S3Bucket("launchflow-sample-bucket-django")

# Docs: https://docs.launchflow.com/reference/services/gcp_cloud_run
fargate_service = lf.aws.ECSFargate("django-service")
