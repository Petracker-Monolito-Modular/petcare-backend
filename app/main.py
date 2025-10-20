from fastapi import FastAPI
from app.core.db import init_db
from app.modules.auth.router import router as auth_router
from app.modules.pets.router import router as pets_router

app = FastAPI(title="PetCare API", version="0.1", swagger_ui_parameters={"persistAuthorization": True})

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/health")
async def health():
    return {"status": "ok"}

# Routers por módulo
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(pets_router, prefix="/pets", tags=["pets"])
