from fastapi import APIRouter, Depends, Header, HTTPException, status
from typing import Optional
import jwt
from app.core.security import http_bearer
from fastapi.security import HTTPAuthorizationCredentials
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
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials  # Swagger pondrá "Bearer ..." por ti
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await repo.get_user_by_id(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return {"id": str(user["_id"]), "email": user["email"], "name": user.get("name","")}