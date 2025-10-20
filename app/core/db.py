from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None

async def init_db():
    """
    Inicializa el cliente y asegura índices mínimos.
    """
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo_uri)
        _db = _client[settings.mongo_db]

        # Índices mínimos
        await _db["users"].create_index("email", unique=True)
        await _db["pets"].create_index([("owner_id", 1)])

def get_db() -> AsyncIOMotorDatabase:
    assert _db is not None, "DB not initialized. Did you call init_db()?"
    return _db
