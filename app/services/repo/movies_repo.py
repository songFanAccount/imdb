from app.db.mongo import get_movies_collection
from app.schemas.movie import MovieIn
import logging
logger = logging.getLogger(__name__)
async def add_movies(movies: list[MovieIn]):
  movies_db = get_movies_collection()
  docs = [m.model_dump() for m in movies]
  if not docs:
    return 0
  result = await movies_db.insert_many(docs, ordered=False)
  logger.info(f"Added {len(movies)} movies")
  return len(result.inserted_ids)