from fastapi import APIRouter, Depends
from typing import List
from app.modules.auth.router import get_current_user
from app.modules.pets.schemas import PetCreate, PetUpdate, PetOut
from app.modules.pets import service

router = APIRouter()

@router.get("", response_model=List[PetOut])
async def list_pets(user=Depends(get_current_user)):
    return await service.list_my_pets(user["id"])

@router.post("", response_model=PetOut, status_code=201)
async def create_pet(body: PetCreate, user=Depends(get_current_user)):
    return await service.create_my_pet(user["id"], body.model_dump())

@router.get("/{pet_id}", response_model=PetOut)
async def get_pet(pet_id: str, user=Depends(get_current_user)):
    return await service.get_my_pet(user["id"], pet_id)

@router.put("/{pet_id}", response_model=PetOut)
async def update_pet(pet_id: str, body: PetUpdate, user=Depends(get_current_user)):
    payload = {k: v for k, v in body.model_dump().items() if v is not None}
    return await service.update_my_pet(user["id"], pet_id, payload)

@router.delete("/{pet_id}", status_code=204)
async def delete_pet(pet_id: str, user=Depends(get_current_user)):
    await service.delete_my_pet(user["id"], pet_id)
    return
