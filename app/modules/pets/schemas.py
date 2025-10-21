from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import date, datetime

class Species(str, Enum):
    felino = "felino"
    canino = "canino"
    otro   = "otro"

class Sex(str, Enum):
    macho        = "macho"
    hembra       = "hembra"
    desconocido  = "desconocido"

class PetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    species: Species
    breed: Optional[str] = Field(default=None, max_length=60)
    sex: Sex = Sex.desconocido
    weight_kg: Optional[float] = Field(default=None, gt=0, le=120)
    birth_date: Optional[date] = None

class PetUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=60)
    species: Optional[Species] = None
    breed: Optional[str] = Field(default=None, max_length=60)
    sex: Optional[Sex] = None
    weight_kg: Optional[float] = Field(default=None, gt=0, le=120)
    birth_date: Optional[date] = None

class PetOut(BaseModel):
    id: str
    name: str
    species: Species
    breed: Optional[str] = None
    sex: Sex
    weight_kg: Optional[float] = None
    birth_date: Optional[date] = None
    owner_id: str
    created_at: datetime
    updated_at: datetime
