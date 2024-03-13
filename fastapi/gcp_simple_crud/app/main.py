import asyncio
from contextlib import asynccontextmanager

import redis
from fastapi import Depends, FastAPI, HTTPException, Response, UploadFile
from google.cloud import storage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.infra import gcs_bucket, pg, redis_cluster, redis_vm
from app.models import Base, User

pool = None
SessionLocal = None


async def init_db() -> AsyncEngine:
    global pool
    global SessionLocal

    if pool is None:
        pool = await pg.sqlalchemy_async_engine()
        SessionLocal = async_sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=pool
        )
        async with pool.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def get_db():
    global SessionLocal
    if SessionLocal is None:
        raise ValueError("Connection pool not initialized")
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.gather(
        gcs_bucket.connect_async(),
        redis_vm.connect_async(),
        redis_cluster.connect_async(),
        pg.connect_async(),
    )
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User)).scalars().all()
    return {"users": [u.__dict__ for u in users]}


@app.post("/users")
async def create_user(
    name: str,
    photo: UploadFile,
    db: AsyncSession = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = User(name=name, photo=photo.filename)
    db.add(user)
    await db.commit()
    blob_path = f"users/{user.id}/{photo.filename}"
    bucket.blob(blob_path).upload_from_file(photo.file, content_type=photo.content_type)
    return user.__dict__


@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    blob = bucket.blob(f"users/{user.id}/{user.photo}")
    photo = blob.download_as_bytes()
    return Response(
        photo, media_type=blob.content_type, headers={"X-User-Name": user.name}
    )


@app.put("/users/{user_id}")
async def update_user(
    user_id: int,
    name: str,
    photo: UploadFile,
    db: AsyncSession = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.photo = photo.filename
    await db.commit()
    bucket.blob(f"users/{user.id}/{user.photo}").upload_from_file(
        photo.file, content_type=photo.content_type
    )
    return user.__dict__


@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    bucket.delete_blob(f"users/{user.id}/{user.photo}")
    return "success"


@app.get("/test_db")
async def test_db(db: AsyncSession = Depends(get_db)):
    # create a test user in the db then query it back
    user = User(name="test", photo="test.jpg")
    db.add(user)
    await db.commit()
    user = await db.get(User, user.id)
    return {
        "id": user.id,
        "name": user.name,
        "photo": user.photo,
    }


@app.get("/test_redis")
async def test_redis(redis_client: redis.Redis = Depends(redis_cluster.redis_async)):
    # set a key in redis and read it back
    await redis_client.set("test", "test")
    return await redis_client.get("test")


@app.get("/test_redis_vm")
async def test_redis_vm(redis_client: redis.Redis = Depends(redis_vm.redis_async)):
    # set a key in redis and read it back
    await redis_client.set("test", "test")
    return await redis_client.get("test")


@app.get("/test_gcs")
async def test_gcs(bucket: storage.Bucket = Depends(gcs_bucket.bucket)):
    # create a test file in the gcs bucket then read it back
    blob = bucket.blob("test.txt")
    blob.upload_from_string("test")
    return blob.download_as_text()
