from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# This will create a "users" table in your database
class StorageUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True, nullable=False, unique=True)
    name = Column(String, nullable=False)

    def as_dict(self):
        return {"id": self.id, "email": self.email, "name": self.name}
