import requests

API_URL = "http://127.0.0.1:8000/movies/add"

payload = {
    "imdb_id": "tt0111161",
    "title": "The Shawshank Redemption",
    "year": 1994,
    "rating": 9.3,
    "genre": "Drama",
    "synopsis": "Two imprisoned men bond over a number of years...",
    "cast": [
      "Example name1",
      "Name example 2"
    ]
}

if __name__ == "__main__":
    res = requests.post(API_URL, json=payload)
    print("Status:", res.status_code)
    print("Response:", res.json())