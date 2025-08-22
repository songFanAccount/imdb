from fastapi import FastAPI
app = FastAPI(title="IMDB Intelligence API")
@app.get("/")
async def root():
  return {"ok": True}