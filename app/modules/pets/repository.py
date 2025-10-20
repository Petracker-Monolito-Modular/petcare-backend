from typing import List, Optional
from bson import ObjectId
from app.core.db import get_db

async def list_pets_by_owner(owner_id: str) -> list[dict]:
    db = get_db()
    cursor = db["pets"].find({"owner_id": ObjectId(owner_id)})
    return await cursor.to_list(length=1000)

async def create_pet(owner_id: str, data: dict) -> str:
    db = get_db()
    doc = {**data, "owner_id": ObjectId(owner_id)}
    res = await db["pets"].insert_one(doc)
    return str(res.inserted_id)

async def get_pet(owner_id: str, pet_id: str) -> Optional[dict]:
    db = get_db()
    return await db["pets"].find_one({"_id": ObjectId(pet_id), "owner_id": ObjectId(owner_id)})

async def update_pet(owner_id: str, pet_id: str, data: dict) -> bool:
    db = get_db()
    res = await db["pets"].update_one(
        {"_id": ObjectId(pet_id), "owner_id": ObjectId(owner_id)},
        {"$set": data},
    )
    return res.matched_count == 1

async def delete_pet(owner_id: str, pet_id: str) -> bool:
    db = get_db()
    res = await db["pets"].delete_one({"_id": ObjectId(pet_id), "owner_id": ObjectId(owner_id)})
    return res.deleted_count == 1
