from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
  mongo_uri: str
  mongo_db: str
  openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
  scrape_concurrency: int = Field(default=4, alias="SCRAPE_CONCURRENCY")
  model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore",
    populate_by_name=True
  )
settings = Settings()
