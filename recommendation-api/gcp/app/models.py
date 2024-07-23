from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):
    pass

class StorageUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preferences = Column(String, nullable=False)

class StorageItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)

    # relationships
    menu = relationship("StorageMenu", back_populates="items")

class StorageMenu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    # relationships
    items = relationship("StorageItem", back_populates="menu")
    restaurant = relationship("StorageRestaurant", back_populates="menus")

class StorageRestaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # relationships
    menus = relationship("StorageMenu", back_populates="restaurant")