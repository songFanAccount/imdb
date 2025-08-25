from fastapi import FastAPI
import logging


from app.routers import movies, scrape, summarize

app = FastAPI(title="IMDB Intelligence API")
app.include_router(movies.router)
app.include_router(scrape.router)
app.include_router(summarize.router)

# One-time setup at program start
logging.basicConfig(
    level=logging.INFO,  # minimum level to show
    format="%(asctime)s [%(levelname)s] %(message)s"
)
@app.get("/")
async def root():
  return {"ok": True}