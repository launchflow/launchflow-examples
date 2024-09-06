import launchflow as lf

bucket = lf.gcp.GCSBucket(f"new-bucket-{lf.project}-{lf.environment}", force_destroy=True)
cloud_run = lf.gcp.CloudRun("my-cloud-run")
