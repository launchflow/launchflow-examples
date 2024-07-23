import launchflow as lf

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/cloudsql
postgres = lf.aws.RDSPostgres("fastapi-backend-postgres")

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/memorystore
redis = lf.aws.ElasticacheRedis("fastapi-backend-redis")

# GCSBucket Docs: https://docs.launchflow.com/reference/gcp-resources/gcs
storage = lf.aws.S3Bucket("fastapi-backend-storage-1234")

# CloudRun Docs: https://docs.launchflow.com/reference/gcp-services/cloud-run
ecs_fargate = lf.aws.ECSFargate("fastapi-backend-service", dockerfile="Dockerfile")
