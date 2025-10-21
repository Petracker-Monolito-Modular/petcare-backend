# app/modules/pets/repository.py
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone, date
from enum import Enum
from app.core.db import get_db

def _normalize_pet_data_for_db(data: dict) -> dict:
    out = {}
    for k, v in data.items():
        if isinstance(v, Enum):
            out[k] = v.value
        elif isinstance(v, date) and not isinstance(v, datetime):
            out[k] = datetime(v.year, v.month, v.day, tzinfo=timezone.utc)
        else:
            out[k] = v
    return out

async def list_pets_by_owner(owner_id: str, limit: int = 50, offset: int = 0) -> list[dict]:
    db = get_db()
    cursor = (db["pets"]
              .find({"owner_id": ObjectId(owner_id)})
              .sort("created_at", -1)
              .skip(offset)
              .limit(limit))
    return await cursor.to_list(length=limit)

async def count_pets_by_owner(owner_id: str) -> int:
    db = get_db()
    return await db["pets"].count_documents({"owner_id": ObjectId(owner_id)})

async def create_pet(owner_id: str, data: dict) -> str:
    db = get_db()
    now = datetime.now(timezone.utc)
    norm = _normalize_pet_data_for_db(data)
    doc = {
        **norm,
        "owner_id": ObjectId(owner_id),
        "created_at": now,
        "updated_at": now,
    }
    res = await db["pets"].insert_one(doc)
    return str(res.inserted_id)

async def get_pet(owner_id: str, pet_id: str) -> Optional[dict]:
    db = get_db()
    return await db["pets"].find_one({"_id": ObjectId(pet_id), "owner_id": ObjectId(owner_id)})

async def update_pet(owner_id: str, pet_id: str, data: dict) -> bool:
    db = get_db()
    norm = _normalize_pet_data_for_db(data)
    res = await db["pets"].update_one(
        {"_id": ObjectId(pet_id), "owner_id": ObjectId(owner_id)},
        {"$set": norm, "$currentDate": {"updated_at": True}},
    )
    return res.matched_count == 1

async def delete_pet(owner_id: str, pet_id: str) -> bool:
    db = get_db()
    res = await db["pets"].delete_one({"_id": ObjectId(pet_id), "owner_id": ObjectId(owner_id)})
    return res.deleted_count == 1
