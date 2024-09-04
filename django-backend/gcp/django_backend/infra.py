import launchflow as lf

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/cloudsql
postgres = lf.gcp.ComputeEnginePostgres("django-backend-postgres")

# CloudSQLPostgres Docs: https://docs.launchflow.com/reference/gcp-resources/memorystore
redis = lf.gcp.ComputeEngineRedis("django-backend-redis")

# GCSBucket Docs: https://docs.launchflow.com/reference/gcp-resources/gcs
storage = lf.gcp.GCSBucket("django-backend-storage-1234")  # needs to be globally unique

# CloudRun Docs: https://docs.launchflow.com/reference/gcp-services/cloud-run
cloud_run = lf.gcp.CloudRun("django-backend-service", dockerfile="Dockerfile")
