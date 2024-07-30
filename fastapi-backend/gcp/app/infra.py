import launchflow as lf

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/cloudsql
cloudsql_postgres = lf.gcp.CloudSQLPostgres("fastapi-backend-postgres")

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/memorystore
memorystore_redis = lf.gcp.MemorystoreRedis("fastapi-backend-redis")

# GCSBucket Docs: https://docs.launchflow.com/reference/gcp-resources/gcs
gcs_bucket = lf.gcp.GCSBucket("fastapi-backend-storage-bucket")

# CloudRun Docs: https://docs.launchflow.com/reference/gcp-services/cloud-run
cloud_run_service = lf.gcp.CloudRun("fastapi-backend-service", dockerfile="Dockerfile")
