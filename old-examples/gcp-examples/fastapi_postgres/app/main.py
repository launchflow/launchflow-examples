from contextlib import asynccontextmanager

from app.infra import postgres
from app.models import Base, StorageUser
from app.schemas import ListUsersResponse, UserResponse
from launchflow.fastapi import sqlalchemy_async_depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, FastAPI, HTTPException

# Create the global FastAPI dependency for the SQLAlchemy async session
async_session = sqlalchemy_async_depends()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the SQLAlchemy async engine (connection pool)
    engine = await postgres.sqlalchemy_async_engine()
    # Create the database tables using the engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Set up the FastAPI dependency
    async_session.setup(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def list_users(db: AsyncSession = Depends(async_session)):
    storage_users = (await db.execute(select(StorageUser))).scalars().all()
    return ListUsersResponse.from_storage(storage_users)


@app.post("/")
async def create_user(email: str, name: str, db: AsyncSession = Depends(async_session)):
    storage_user = StorageUser(email=email, name=name)
    db.add(storage_user)
    await db.commit()
    return UserResponse.from_storage(storage_user)


@app.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(async_session)):
    storage_user = await db.get(StorageUser, user_id)
    if storage_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_storage(storage_user)


@app.put("/{user_id}")
async def update_user(
    user_id: int, name: str, db: AsyncSession = Depends(async_session)
):
    storage_user = await db.get(StorageUser, user_id)
    if storage_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    storage_user.name = name
    await db.commit()
    return UserResponse.from_storage(storage_user)


@app.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(async_session)):
    storage_user = await db.get(StorageUser, user_id)
    if storage_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(storage_user)
    await db.commit()
    return UserResponse.from_storage(storage_user)
