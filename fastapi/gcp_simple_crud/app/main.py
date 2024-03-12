import asyncio
import launchflow as lf
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from google.cloud import storage
from app.infra import gcs_bucket, pg, redis, redis_vm
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
        redis.connect_async(),
        pg.connect_async(),
    )
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await db.execute(select(User)).scalars().all()
    return {"users": [u.__dict__ for u in users]}


@app.post("/")
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


@app.get("/{user_id}")
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


@app.put("/{user_id}")
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


@app.delete("/{user_id}")
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
