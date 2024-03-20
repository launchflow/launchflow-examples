import asyncio
import launchflow as lf
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, UploadFile, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from google.cloud import storage
from app.infra import gcs_bucket, pg
from app.models import Base, User


engine = pg.sqlalchemy_engine()
Base.metadata.create_all(bind=engine)
get_db = lf.fastapi.sqlalchemy(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.gather(
        gcs_bucket.connect_async(),
    )
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def list_users(db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return {"users": [u.__dict__ for u in users]}


@app.post("/")
async def create_user(
    name: str,
    photo: UploadFile,
    db: Session = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = User(name=name, photo=photo.filename)
    db.add(user)
    db.commit()
    blob_path = f"users/{user.id}/{photo.filename}"
    bucket.blob(blob_path).upload_from_file(photo.file, content_type=photo.content_type)
    return user.__dict__


@app.get("/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = db.get(User, user_id)
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
    db: Session = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.photo = photo.filename
    db.commit()
    bucket.blob(f"users/{user.id}/{user.photo}").upload_from_file(
        photo.file, content_type=photo.content_type
    )
    return user.__dict__


@app.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    bucket: storage.Bucket = Depends(gcs_bucket.bucket),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    bucket.delete_blob(f"users/{user.id}/{user.photo}")
    return "success"
