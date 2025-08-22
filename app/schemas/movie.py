from typing import List
from pydantic import BaseModel, Field

class MovieIn(BaseModel):
  imdb_id: str = Field(..., description="IMDB ID, e.g. tt0111161")
  title: str
  year: int
  rating: float = Field(ge=9, le=10)
  genre: str
  synopsis: str
  cast: List[str] = []