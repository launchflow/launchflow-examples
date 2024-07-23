from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
import launchflow as lf
from launchflow.fastapi import sqlalchemy_async_depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StorageItem, StorageRestaurant, StorageUser, StorageMenu
from app.schemas import ItemsResponse, ListItemsResponse, RestaurantResponse, UserResponse, MenuResponse
from app.infra import postgres, api_key
import instructor
from pydantic import BaseModel
from openai import OpenAI
import asyncio


PROMPT = """
You are a recommendation engine for a restaurant.
You are tasked with recommending menu items to the user.
You will be given the user's preferences and the restaurant's menu items.

User preference:
{user_preference}

Restaurant menu items:
{restaurant_menu_items}

Return a sorted list from best to worst of all the items that the user might like.
Return the list in this format:
- {{item_id}}
- {{item_id}}
- {{item_id}}
Exclude items that the user would not like.
Always recommend at least 3 items, but never more than 10 items.
"""

class ItemInfoFromPrompt(BaseModel):
    item_ids: List[int]


def get_llm_client() -> OpenAI:
    return instructor.from_openai(OpenAI(api_key=api_key.version().decode("utf-8")))


async_session = sqlalchemy_async_depends()


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = await postgres.sqlalchemy_async_engine()
    async_session.setup(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return f"Hello from {lf.environment}"


@app.post("/add_user")
async def add_user(name: str, preferences: str, db: AsyncSession = Depends(async_session)):
    user = StorageUser(
        name=name,
        preferences=preferences,
    )
    db.add(user)
    await db.commit()
    return UserResponse.from_storage(user)


@app.post("/add_restaurant")
async def add_restaurant(name: str, db: AsyncSession = Depends(async_session)):
    restaurant = StorageRestaurant(name=name)
    db.add(restaurant)
    await db.commit()
    return await RestaurantResponse.from_storage(restaurant)


@app.post("/add_menu")
async def add_menu(restaurant_id: int, name: str, db: AsyncSession = Depends(async_session)):
    menu = StorageMenu(
        name=name,
        restaurant_id=restaurant_id,
    )
    db.add(menu)
    await db.commit()
    return await MenuResponse.from_storage(menu)


@app.post("/add_item")
async def add_item(menu_id: int, name: str, price: float, db: AsyncSession = Depends(async_session)):
    item = StorageItem(
        name=name,
        price=price,
        menu_id=menu_id,
    )
    db.add(item)
    await db.commit()
    return ItemsResponse.from_storage(item)


@app.get("/recommend")
async def recommend_items(
    user_id: int, 
    restaurant_id: int, 
    db: AsyncSession = Depends(async_session), 
    llm_client: OpenAI = Depends(get_llm_client),   
):
    # Get user and restaurant preferences from the database
    user = await db.get(StorageUser, user_id)
    restaurant = await db.get(StorageRestaurant, restaurant_id)

    # Get all items from the restaurant's menus
    menus = await restaurant.awaitable_attrs.menus
    all_items = []
    for menu in menus:
        all_items.append(menu.awaitable_attrs.items)
    all_items = await asyncio.gather(*all_items)
    flattened_items = [item for sublist in all_items for item in sublist]
    items_json = [ItemsResponse.from_storage(item).model_dump_json() for item in flattened_items]

    # Prompt the LLM for the item recommendations
    item_info: ItemInfoFromPrompt = llm_client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=ItemInfoFromPrompt,
        messages=[{"role": "user", "content": PROMPT.format(
            user_preference=user.preferences,
            restaurant_menu_items=items_json,
        )}],
    )
    
    # Look up the items in the database
    items_result = await db.execute(select(StorageItem).where(StorageItem.id.in_(item_info.item_ids)))
    items = items_result.scalars().all()
    # Return the items
    if len(items) == 0:
        raise HTTPException(status_code=400, detail="No recommendations")
    return ListItemsResponse.from_storage(items)
