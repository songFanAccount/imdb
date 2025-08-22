from typing import List
from pydantic import BaseModel, Field

class MovieIn(BaseModel):
  imdb_id: str = Field(..., description="IMDB ID, e.g. tt0111161")
  title: str
  year: int
  rating: float = Field(ge=9, le=10)
  synopsis: str
  genres: List[str] = []
  cast: List[str] = []