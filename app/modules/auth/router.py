from fastapi import APIRouter, Depends, Header, HTTPException, status
from typing import Optional
import jwt

from app.modules.auth.schemas import UserCreate, UserLogin, UserOut, TokenOut
from app.modules.auth.service import register_user, login_user
from app.modules.auth import repository as repo
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
async def register(body: UserCreate):
    user = await register_user(body.email, body.name, body.password)
    return user

@router.post("/login", response_model=TokenOut)
async def login(body: UserLogin):
    token = await login_user(body.email, body.password)
    return {"access_token": token, "token_type": "bearer"}

# Dependencia simple para obtener usuario actual desde Authorization: Bearer
async def get_current_user(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split()[1]
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        sub = payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await repo.get_user_by_id(sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # Sanitizar
    return {"id": str(user["_id"]), "email": user["email"], "name": user.get("name", "")}
