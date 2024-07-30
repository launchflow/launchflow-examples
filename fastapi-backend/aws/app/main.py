from contextlib import asynccontextmanager

import launchflow as lf
from app.api.users import router
from app.dependencies import async_session
from app.infra import ecs_fargate_service, elasticache_redis, rds_postgres, s3_bucket
from app.models import Base
from fastapi import Depends, FastAPI
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect and cache the Resource connection info
    await lf.connect_all(
        ecs_fargate_service, rds_postgres, elasticache_redis, s3_bucket
    )

    # Create the SQLAlchemy async engine (connection pool)
    engine = await rds_postgres.sqlalchemy_async_engine()

    # Create the database tables using the engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Configure the (async) SQLAlchemy connection pool
    async_session.setup(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def read_root():
    return f"Hello from {lf.environment}"


@app.get("/service_info")
async def service_info():
    if lf.is_deployment():
        # Return the ECS Fargate service info for this deployment
        return ecs_fargate_service.outputs().to_dict()
    return {"message": "Running locally"}


@app.get("/test_redis")
async def test_elasticache_redis(
    redis_client: Redis = Depends(elasticache_redis.redis_async),
):
    # Test the Redis connection by setting and getting a key
    await redis_client.set("key", "value")
    return await redis_client.get("key")


@app.get("/test_db")
async def test_db(db: AsyncSession = Depends(async_session)):
    # Test the RDS Postgres connection by executing a query
    result = await db.execute(text("SELECT 1"))
    return result.scalar_one()


@app.get("/test_storage")
async def test_storage():
    # Test the S3 connection by uploading and downloading a file
    s3_bucket.upload_from_string("Hello, world!", "test.txt")
    return s3_bucket.download_file("test.txt").decode("utf-8")
