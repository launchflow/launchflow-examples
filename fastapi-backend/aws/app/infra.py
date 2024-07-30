import launchflow as lf

# RDSPostgres Docs: https://docs.launchflow.com/reference/aws-resources/rds
rds_postgres = lf.aws.RDSPostgres("fastapi-backend-postgres")

# ElasticacheRedis Docs: https://docs.launchflow.com/reference/aws-resources/elasticache
elasticache_redis = lf.aws.ElasticacheRedis("fastapi-backend-redis")

# S3Bucket Docs: https://docs.launchflow.com/reference/aws-resources/s3
s3_bucket = lf.aws.S3Bucket("fastapi-backend-storage-bucket")

# ECSFargate Docs: https://docs.launchflow.com/reference/aws-services/ecs-fargate
ecs_fargate_service = lf.aws.ECSFargate(
    "fastapi-backend-service", dockerfile="Dockerfile"
)
