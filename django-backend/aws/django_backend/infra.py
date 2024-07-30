import launchflow as lf

# RDSPostgres Docs: https://docs.launchflow.com/reference/aws-resources/rds
postgres = lf.aws.RDSPostgres("django-backend-postgres")

# ElasticacheRedis Docs: https://docs.launchflow.com/reference/aws-resources/elasticache
redis = lf.aws.ElasticacheRedis("django-backend-redis")

# S3Bucket Docs: https://docs.launchflow.com/reference/aws-resources/s3
storage = lf.aws.S3Bucket("django-backend-storage-1234")

# ECSFargate Docs: https://docs.launchflow.com/reference/aws-services/ecs-fargate
ecs_fargate = lf.aws.ECSFargate("django-backend-service", dockerfile="Dockerfile")
