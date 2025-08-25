from typing import List, Optional
from pydantic import BaseModel, Field

class MovieIn(BaseModel):
  imdb_id: str = Field(..., description="IMDB ID, e.g. tt0111161")
  title: str
  year: Optional[int] = None
  rating: float = Field(ge=9, le=10)
  synopsis: Optional[str] = None
  genres: List[str] = []
  cast: List[str] = []

class MovieSummaryDetails(BaseModel):
  title: str
  year: Optional[int] = None
  synopsis: Optional[str] = None
  genres: List[str] = []