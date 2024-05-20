from contextlib import asynccontextmanager

import launchflow as lf
from fastapi import Depends, FastAPI
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

postgres = lf.aws.EC2Postgres("sandbox-postgres")
redis = lf.aws.EC2Redis("sandbox-redis")


async_session = lf.fastapi.sqlalchemy_async_depends()


@asynccontextmanager
async def lifespan(app: FastAPI):
    lf.connect_all(postgres, redis)
    # Create the SQLAlchemy async engine (connection pool)
    engine = await postgres.sqlalchemy_async_engine()
    # Setup the async session dependency
    async_session.setup(engine)
    yield


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/redis")
async def test_redis(
    key: str,
    value: str,
    redis_client: Redis = Depends(redis.redis_async),
) -> str:
    await redis_client.set(key, value)
    test_value = await redis_client.get(key)
    return f"Set {key} to {test_value}"


@app.get("/postgres")
async def test_postgres(
    db: AsyncSession = Depends(async_session),
) -> str:
    result = await db.execute(text("SELECT 1"))
    return {"Result": result.scalar_one_or_none()}


if __name__ == "__main__":
    postgres.ssh()
