import fastapi
import launchflow as lf

service = lf.gcp.CloudRun("my-service", domain="my-domain.com")
secret = lf.gcp.SecretManagerSecret("my-secret")

# Define your infrastructure alongside your application code
# postgres_vm = lf.aws.EC2Postgres(f"tanke-postgres-{lf.environment}")
# postgres_cluster = lf.aws.RDSPostgres(f"tanke-cloud-sql-{lf.environment}")
# fargate = lf.aws.ECSFargate(f"tanke-fargate-{lf.environment}")

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return f"Hello from {lf.environment}!"


# @app.get("/query_vm")
# def query_vm(query: str):
#     return postgres_vm.query(query)


# @app.get("/query_cluster")
# def query_cluster(query: str):
#     return postgres_cluster.query(query)


# if __name__ == "__main__":
#     for postgres in [postgres_vm, postgres_cluster]:
#         print(
#             # LaunchFlow automates client configuration across multiple environments
#             postgres.query(
#                 f"""
#                 DROP TABLE IF EXISTS users;
#                 CREATE TABLE users (
#                     id SERIAL PRIMARY KEY,
#                     name VARCHAR(255) NOT NULL,
#                     environment VARCHAR(255) NOT NULL
#                 );

#                 INSERT INTO users (name, environment) VALUES ('Alice', '{lf.environment}');

#                 SELECT * FROM users;
#                 """
#             )
#         )
