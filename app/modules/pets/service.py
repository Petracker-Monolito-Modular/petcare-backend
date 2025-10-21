# app/modules/pets/service.py
from datetime import datetime
from fastapi import HTTPException, status
from app.core.oid import serialize_doc
from app.modules.pets import repository as repo

def _doc_to_out(d: dict) -> dict:
    d = serialize_doc(d)
    bd = d.get("birth_date")
    if isinstance(bd, datetime):
        d["birth_date"] = bd.date()
    return d

async def list_my_pets(owner_id: str, limit: int, offset: int) -> dict:
    docs = await repo.list_pets_by_owner(owner_id, limit=limit, offset=offset)
    total = await repo.count_pets_by_owner(owner_id)
    items = [_doc_to_out(d) for d in docs]
    return {"items": items, "total": total, "limit": limit, "offset": offset}

async def create_my_pet(owner_id: str, data: dict) -> dict:
    pet_id = await repo.create_pet(owner_id, data)
    return await get_my_pet(owner_id, pet_id)

async def get_my_pet(owner_id: str, pet_id: str) -> dict:
    doc = await repo.get_pet(owner_id, pet_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return _doc_to_out(doc)

async def update_my_pet(owner_id: str, pet_id: str, data: dict) -> dict:
    ok = await repo.update_pet(owner_id, pet_id, data)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return await get_my_pet(owner_id, pet_id)

async def delete_my_pet(owner_id: str, pet_id: str) -> None:
    ok = await repo.delete_pet(owner_id, pet_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
