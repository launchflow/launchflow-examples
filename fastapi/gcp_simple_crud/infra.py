import launchflow as lf

# TODO(developer): Set these variables with your own values
db = lf.gcp.CloudSQLPostgres("launchflow-demo-db")
lf_bucket = lf.gcp.GCSBucket("launchflow-demo-bucket-1")
