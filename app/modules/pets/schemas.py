from pydantic import BaseModel, Field
from typing import Optional

class PetCreate(BaseModel):
    name: str = Field(min_length=1)
    species: str = Field(min_length=1)
    birth_date: Optional[str] = None  # ISO date string simple v0

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    birth_date: Optional[str] = None

class PetOut(BaseModel):
    id: str
    name: str
    species: str
    birth_date: Optional[str] = None
    owner_id: str
