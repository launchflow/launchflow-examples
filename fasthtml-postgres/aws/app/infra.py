import launchflow as lf

postgres = lf.aws.RDSPostgres("fasthtml-example")

ecs_fargate = lf.aws.ECSFargate("fasthtml-service")
