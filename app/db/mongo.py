from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client = None
def get_db():
  global _client
  if _client is None:
    _client = AsyncIOMotorClient(settings.mongo_uri)
    return _client[settings.mongo_db]
