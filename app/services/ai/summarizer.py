from app.schemas.movie import MovieSummaryDetails
from app.deps import openai_client

async def summarize_movie_openai(movieMetadata: MovieSummaryDetails):
  prompt = f"Generate a summary for the movie '{movieMetadata.title}', released in {movieMetadata.year}. This movie belongs in the genres {','.join(movieMetadata.genres)}, and here is its imdb synopsis: '{movieMetadata.synopsis}'. Include all the metadata naturally."
  resp = openai_client.responses.create(model="gpt-5", input=prompt)
  summary = resp.output_text.strip()
  return { "summary": summary }