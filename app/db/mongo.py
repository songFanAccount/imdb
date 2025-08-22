from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

_client: Optional[AsyncIOMotorClient] = None

def get_client():
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo_uri)
    return _client[settings.mongo_db]

def get_db():
  return get_client()[settings.mongo_db]
  
def get_movies_collection():
  return get_db()["movies"]