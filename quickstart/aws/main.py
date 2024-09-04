import launchflow as lf

mysql_rds = lf.aws.RDS(
    "mysql-rds",
    publicly_accessible=False,
    engine_version=lf.aws.rds.RDSEngineVersion.MYSQL8_0,
)


def lambda_handler(event, context):
    print("fetching outputs for mysql_rds")
    print(mysql_rds.outputs())
    print("outputs fetched")
    print("querying database")
    print(mysql_rds.query("SELECT 1"))
    print("database queried")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": f"Hello from {lf.environment}!",
    }


elastic_ip = lf.aws.ElasticIP("tanke-elastic-ip")
nat = lf.aws.NATGateway("tanke-nat-gateway", elastic_ip=elastic_ip)

api = lf.aws.LambdaStaticService(
    "tanke-lambda-v2",
    handler=lambda_handler,
    static_directory=".",  # TODO: rename to build_directory
    requirements_txt_path="requirements.txt",
    python_packages=["sqlalchemy", "pymysql[rsa]"],
    # domain can be a string or composite resource class
    # TODO: see if resource.depends_on(resource) works for "hidden" resources
    # TODO: learn how to migrate from lambda to api gateway without zero downtime
    # domain="tanke.dev",
    # domain=lf.aws.APIGatewayDomain("tanke-api-gateway", domain_name="tanke.dev"),
    # domain=lf.aws.ALBDomain("tanke-alb", domain_name="tanke.dev"),
    # domain=lf.aws.LambdaDomain("tanke-alb", domain_name="tanke.dev"),
)


if __name__ == "__main__":
    print(api.outputs())
