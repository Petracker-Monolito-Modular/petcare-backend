from typing import Optional
from app.core.db import get_db
from bson import ObjectId

async def get_user_by_email(email: str) -> Optional[dict]:
    db = get_db()
    return await db["users"].find_one({"email": email})

async def get_user_by_id(id_str: str) -> Optional[dict]:
    db = get_db()
    return await db["users"].find_one({"_id": ObjectId(id_str)})

async def create_user(user_data: dict) -> str:
    """
    user_data: {"email", "name", "hashed_password"}
    """
    db = get_db()
    res = await db["users"].insert_one(user_data)
    return str(res.inserted_id)
