import launchflow as lf

# Docs: https://docs.launchflow.com/reference/aws-resources/s3-bucket
bucket = lf.aws.S3Bucket(f"launchflow-bucket-{lf.environment}", force_destroy=True)
service = lf.aws.ECSFargate("my-service", port=8080, desired_count=2)
