from app.db.mongo import get_movies_collection
from app.schemas.movie import MovieIn

async def add_movies(movies: list[MovieIn]):
  movies_db = get_movies_collection()
  docs = [m.model_dump() for m in movies]
  if not docs:
    return 0
  result = await movies_db.insert_many(docs, ordered=False)
  return len(result.inserted_ids)