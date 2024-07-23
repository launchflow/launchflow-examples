import launchflow as lf


postgres = lf.gcp.ComputeEnginePostgres("recommendation-api-postgres")
api_key = lf.gcp.SecretManagerSecret("recommendation-api-api-key")
api = lf.gcp.CloudRun("recommendation-api")


if __name__ == "__main__":
    from models import Base
    engine = postgres.sqlalchemy_engine()
    Base.metadata.drop_all(engine)
    print("Dropped all tables")
    Base.metadata.create_all(engine)
    print("Created all tables")
    