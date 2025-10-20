# PetCare Backend (FastAPI + Mongo)

## Requisitos
- Python 3.11+
- Docker (MongoDB)

## Desarrollo
1. `docker-compose up -d`
2. Crear `.env` desde `.env.example`
3. Instalar deps: `pip install -r requirements.txt` (o `uv/poetry`)
4. Run: `uvicorn app.main:app --reload`
5. Salud: `GET http://localhost:8000/health`

## Estructura
- app/core: config, db, security
- app/modules: auth, users, pets

## Endpoints v0
- POST /auth/register
- POST /auth/login
- GET /pets, POST /pets, PUT /pets/{id}, DELETE /pets/{id}
