from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
http_bearer = HTTPBearer(auto_error=True)
# Usamos Argon2id como predeterminado y dejamos bcrypt para compatibilidad
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
    # endurecer parámetros Argon2id (ajústalos si el server es débil)
    argon2__type="ID",
    argon2__memory_cost=65536,  # ~64 MiB
    argon2__time_cost=3,
    argon2__parallelism=2,
)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_min)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
