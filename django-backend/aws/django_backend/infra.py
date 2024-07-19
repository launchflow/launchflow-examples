import launchflow as lf

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/cloudsql
postgres = lf.aws.RDSPostgres("django-backend-postgres")

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/memorystore
redis = lf.aws.ElasticacheRedis("django-backend-redis")

# GCSBucket Docs: https://docs.launchflow.com/reference/gcp-resources/gcs
storage = lf.aws.S3Bucket("django-backend-storage-1234")

# CloudRun Docs: https://docs.launchflow.com/reference/gcp-services/cloud-run
ecs_fargate = lf.aws.ECSFargate("django-backend-service", dockerfile="Dockerfile")
