import launchflow as lf

# Docs: https://docs.launchflow.com/reference/gcp-resources/gcs-bucket
bucket = lf.gcp.GCSBucket(
    f"launchflow-bucket-for-quickstart-{lf.environment}", force_destroy=True
)
service = lf.gcp.CloudRun("launchflow-quickstart", publicly_accessible=False)
