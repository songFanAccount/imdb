from fastapi import APIRouter
from app.services.ai.summarizer import summarize_movie_openai
from app.services.repo.movies_repo import get_movie_by_name

import logging
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/summarize", tags=["summaries"])

@router.post("/{title}")
async def summarize_movie(title: str):
  logger.info(f"Summarising {title}")
  movie = await get_movie_by_name(title)
  summary = await summarize_movie_openai(movie)
  return summary