from fastapi import FastAPI

from app.routers import movies
app = FastAPI(title="IMDB Intelligence API")
app.include_router(movies.router)
@app.get("/")
async def root():
  return {"ok": True}