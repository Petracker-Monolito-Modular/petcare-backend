from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password, create_access_token
from app.modules.auth import repository as repo

async def register_user(email: str, name: str, password: str) -> dict:
    existing = await repo.get_user_by_email(email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user_doc = {"email": email, "name": name, "hashed_password": hash_password(password)}
    user_id = await repo.create_user(user_doc)
    return {"id": user_id, "email": email, "name": name}

async def login_user(email: str, password: str) -> str:
    user = await repo.get_user_by_email(email)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return create_access_token(str(user["_id"]))
