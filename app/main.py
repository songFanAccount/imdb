from fastapi import FastAPI

from app.routers import movies, scrape
app = FastAPI(title="IMDB Intelligence API")
app.include_router(movies.router)
app.include_router(scrape.router)
@app.get("/")
async def root():
  return {"ok": True}