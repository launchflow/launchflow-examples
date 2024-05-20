import asyncio

import launchflow as lf
import tornado
from models import Base, StorageUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Automatically create / connect to a Postgres database running on RDS in AWS
postgres = lf.aws.RDSPostgres("launchflow-example-db")


class ExamplePostgresHandler(tornado.web.RequestHandler):
    def initialize(self, db_connection_pool: async_sessionmaker[AsyncSession]):
        self.db_connection_pool = db_connection_pool

    async def get(self):
        async with self.db_connection_pool() as connection:
            result = await connection.execute(select(StorageUser))
            users = result.scalars().all()
            self.write({"users": [user.as_dict() for user in users]})


async def main():
    # Connect to the database / create a pool of connections to share across requests
    async_engine = await postgres.sqlalchemy_async_engine()
    db_connection_pool = async_sessionmaker(bind=async_engine)

    # Create the database tables defined in the models.py file
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # This adds example users to the database for demonstration purposes
    async with db_connection_pool() as connection:
        connection.add(StorageUser(email="josh@launchflow.com", name="Josh"))
        connection.add(StorageUser(email="caleb@launchflow.com", name="Caleb"))
        connection.add(StorageUser(email="michael@launchflow.com", name="Michael"))
        await connection.commit()

    app = tornado.web.Application(
        [
            (r"/", ExamplePostgresHandler, dict(db_connection_pool=db_connection_pool)),
        ],
    )
    app.listen(8888)
    print("Application running on port 8888")
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()
    print("Shutting down...")


if __name__ == "__main__":
    asyncio.run(main())
