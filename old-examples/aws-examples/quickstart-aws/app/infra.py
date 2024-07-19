import launchflow as lf

bucket = lf.aws.S3Bucket(f"tanke-bucket-{lf.environment}")
