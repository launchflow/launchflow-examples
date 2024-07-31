import dataclasses
from typing import Optional

from sqlalchemy import Boolean, Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class StorageTodo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)


@dataclasses.dataclass
class Todo:
    id: Optional[int] = None
    title: str = ""
    done: bool = False

    @classmethod
    def from_storage(cls, storage_todo: StorageTodo):
        return cls(id=storage_todo.id, title=storage_todo.title, done=storage_todo.done)


"""
Lifecycle functions for the async session
"""
_async_session = None


def async_session() -> AsyncSession:
    global _async_session
    if _async_session is None:
        raise ValueError("Async session not set up")
    return _async_session()


def setup_async_session(engine: AsyncEngine):
    global _async_session
    if _async_session is not None:
        raise ValueError("Async session already set up")
    _async_session = async_sessionmaker(bind=engine)


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


"""
CRUD operations for todos
"""


async def list_todos() -> list[Todo]:
    async with async_session() as db:
        storage_todos = (await db.execute(select(StorageTodo))).scalars().all()
        return [Todo.from_storage(storage_todo) for storage_todo in storage_todos]


async def get_todo(id: int) -> Todo:
    async with async_session() as db:
        storage_todo = await db.get(StorageTodo, id)
        return Todo.from_storage(storage_todo)


async def insert_todo(todo: Todo) -> Todo:
    async with async_session() as db:
        storage_todo = StorageTodo(title=todo.title, done=todo.done)
        db.add(storage_todo)
        await db.commit()
        await db.refresh(storage_todo)
        return Todo.from_storage(storage_todo)


async def update_todo(todo: Todo) -> Todo:
    async with async_session() as db:
        storage_todo = await db.get(StorageTodo, todo.id)
        storage_todo.title = todo.title
        storage_todo.done = todo.done
        await db.commit()
        await db.refresh(storage_todo)
        return Todo.from_storage(storage_todo)


async def delete_todo(id: int) -> Todo:
    async with async_session() as db:
        storage_todo = await db.get(StorageTodo, id)
        db.delete(storage_todo)
        await db.commit()
        await db.refresh(storage_todo)
        return Todo.from_storage(storage_todo)


if __name__ == "__main__":
    import asyncio

    from infra import postgres

    async def recreate_tables():
        engine = await postgres.sqlalchemy_async_engine()
        print("Dropping tables")
        await drop_tables(engine)
        print("Tables dropped")
        print("Creating tables")
        await create_tables(engine)
        print("Tables created")

    asyncio.run(recreate_tables())
