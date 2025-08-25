from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from app.db.mongo import get_db

router = APIRouter(prefix="/movies", tags=["movies"])
logger = logging.getLogger("__name__")
@router.get("/")
async def list_movies(db: AsyncIOMotorDatabase = Depends(get_db)):
    cursor = db["movies"].find({})
    movies = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        movies.append(doc)
    return movies

@router.get("/names")
async def list_movie_names(db: AsyncIOMotorDatabase = Depends(get_db)):
    cursor = db["movies"].find({})
    numMovies = 0
    movieNames = []
    async for doc in cursor:
        movieNames.append(doc["title"])
        numMovies += 1
    return {"numMovies": numMovies, "movieNames": movieNames}
@router.get("/reset")
async def clear_movies_db(db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["movies"].delete_many({})
    logger.info(f"Movies db reset: Deleted {result.deleted_count} movies")