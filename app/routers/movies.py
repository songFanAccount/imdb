from fastapi import APIRouter, Depends

from app.db.mongo import get_db
from app.schemas.movie import MovieIn

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/")
async def list_movies(db = Depends(get_db)):
    doc = await db["movies"].find_one()
    if not doc:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc

@router.post("/add")
async def add_movie(movie: MovieIn, db = Depends(get_db)):
    result = await db["movies"].insert_one(movie.model_dump())
    return {"inserted_id": str(result.inserted_id)}