import launchflow as lf

# Docs: https://docs.launchflow.com/reference/gcp-resources/cloud-sql
pg = lf.gcp.CloudSQLPostgres("caleb-postgres3")

# Docs: https://docs.launchflow.com/reference/gcp-resources/gcs-bucket
gcs_bucket = lf.gcp.GCSBucket("caleb-bucket-unique-bucket-asdf")

# Docs: https://docs.launchflow.com/reference/gcp-resources/compute-engine
redis_vm = lf.gcp.ComputeEngineRedis("caleb-redis-vm")

# Docs: https://docs.launchflow.com/reference/gcp-resources/memorystore
redis_cluster = lf.gcp.MemorystoreRedis("caleb-redis3")
