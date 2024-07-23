from typing import List

from app.models import StorageItem, StorageUser, StorageRestaurant, StorageMenu
from pydantic import BaseModel
import asyncio


class UserResponse(BaseModel):
    id: int
    name: str
    preferences: str

    @classmethod
    def from_storage(cls, storage_user: StorageUser):
        return cls(id=storage_user.id, name=storage_user.name, preferences=storage_user.preferences)
    


class ItemsResponse(BaseModel):
    id: int
    name: str
    price: float
    reason: str

    @classmethod
    def from_storage(cls, storage_item: StorageItem, reason: str=""):
        return cls(id=storage_item.id, name=storage_item.name, price=storage_item.price, reason=reason)


class ListItemsResponse(BaseModel):
    items: List[ItemsResponse]

    @classmethod
    def from_storage(cls, storage_items: List[StorageItem], reasons: List[str]):
        return cls(items=[ItemsResponse.from_storage(item, reason) for item, reason in zip(storage_items, reasons)])


class MenuResponse(BaseModel):
    id: int
    name: str
    items: ListItemsResponse

    @classmethod
    async def from_storage(cls, storage_menu: StorageMenu):
        storage_items = await storage_menu.awaitable_attrs.items
        items = ListItemsResponse.from_storage(storage_items)
        return cls(id=storage_menu.id, name=storage_menu.name, items=items)


class ListMenusResponse(BaseModel):
    menus: List[MenuResponse]

    @classmethod
    async def from_storage(cls, storage_menus: List[StorageMenu]):
        menus = await asyncio.gather(*[MenuResponse.from_storage(menu) for menu in storage_menus])
        return cls(menus=menus)

class RestaurantResponse(BaseModel):
    id: int
    name: str
    menus: ListMenusResponse

    @classmethod
    async def from_storage(cls, storage_restaurant: StorageRestaurant):
        storage_menus = await storage_restaurant.awaitable_attrs.menus
        menus = await ListMenusResponse.from_storage(storage_menus)
        return cls(id=storage_restaurant.id, name=storage_restaurant.name, menus=menus)