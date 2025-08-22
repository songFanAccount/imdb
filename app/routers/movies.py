from fastapi import APIRouter, Depends

from app.db.mongo import get_db

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/")
async def list_movies(db = Depends(get_db)):
    doc = await db["movies"].find_one()
    if not doc:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc