from fastapi import APIRouter

from app.services.scraper.imdb_scraper import scrape_imdb

router = APIRouter(prefix="/scrape", tags=["scrape"])

@router.get("/")
async def scrape_IMDB():
  return await scrape_imdb()