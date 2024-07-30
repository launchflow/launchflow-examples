from app.dependencies import async_session
from app.models import StorageUser
from app.schemas import ListUsersResponse, UserResponse
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users")


@router.get("/")
async def list_users(db: AsyncSession = Depends(async_session)):
    storage_users = (await db.execute(select(StorageUser))).scalars().all()
    return ListUsersResponse.from_storage(storage_users)


@router.post("/")
async def create_user(email: str, name: str, db: AsyncSession = Depends(async_session)):
    storage_user = StorageUser(email=email, name=name)
    db.add(storage_user)
    await db.commit()
    return UserResponse.from_storage(storage_user)


@router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(async_session)):
    storage_user = await db.get(StorageUser, user_id)
    if storage_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_storage(storage_user)


@router.put("/{user_id}")
async def update_user(
    user_id: int, name: str, db: AsyncSession = Depends(async_session)
):
    storage_user = await db.get(StorageUser, user_id)
    if storage_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    storage_user.name = name
    await db.commit()
    return UserResponse.from_storage(storage_user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(async_session)):
    storage_user = await db.get(StorageUser, user_id)
    if storage_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(storage_user)
    await db.commit()
    return UserResponse.from_storage(storage_user)
