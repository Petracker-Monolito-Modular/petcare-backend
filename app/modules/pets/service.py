from fastapi import HTTPException, status
from app.core.oid import serialize_doc
from app.modules.pets import repository as repo

async def list_my_pets(owner_id: str) -> list[dict]:
    docs = await repo.list_pets_by_owner(owner_id)
    return [serialize_doc(d) for d in docs]

async def create_my_pet(owner_id: str, data: dict) -> dict:
    pet_id = await repo.create_pet(owner_id, data)
    return {"id": pet_id, "owner_id": owner_id, **data}

async def get_my_pet(owner_id: str, pet_id: str) -> dict:
    doc = await repo.get_pet(owner_id, pet_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return serialize_doc(doc)

async def update_my_pet(owner_id: str, pet_id: str, data: dict) -> dict:
    ok = await repo.update_pet(owner_id, pet_id, data)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return await get_my_pet(owner_id, pet_id)

async def delete_my_pet(owner_id: str, pet_id: str) -> None:
    ok = await repo.delete_pet(owner_id, pet_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
