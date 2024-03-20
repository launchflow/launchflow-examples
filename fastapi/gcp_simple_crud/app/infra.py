import launchflow as lf


# TODO(developer): Set these variables with your own values
pg = lf.gcp.CloudSQLPostgres("launchflow-demo-db-3")
gcs_bucket = lf.gcp.GCSBucket("launchflow-demo-bucket-1")
