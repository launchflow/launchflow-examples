import launchflow as lf

bucket = lf.aws.S3Bucket(f"new-bucket-{lf.project}-{lf.environment}", force_destroy=True)
ecs_fargate = lf.aws.ECSFargate("my-ecs-fargate")
