import launchflow as lf
from sqlalchemy import text

postgres = lf.gcp.CloudSQLPostgres("my-database")

postgres_vm = lf.gcp.ComputeEnginePostgres("my-database-vm")


if __name__ == "__main__":
    engine = postgres.sqlalchemy_engine()

    with engine.connect() as connection:
        print(connection.execute(text("SELECT 1")).fetchone())  # prints (1,)
