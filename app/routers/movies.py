from fastapi import APIRouter, Depends

from app.db.mongo import get_db

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/movies")
async def list_movies(db = Depends(get_db)):
    return await db["movies"].find_one()