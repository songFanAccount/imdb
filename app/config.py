from pydantic_settings import BaseSettings
class Settings(BaseSettings):
  mongo_uri: str = "mongodb://localhost:27017"
  mongo_db: str = "imdb"
settings = Settings()
