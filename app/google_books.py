#Here we'll call the Google Books API to retrieve book information based on a search query.
import requests
from typing import List, Dict

from app.config import GOOGLE_BOOKS_KEY

BASE_URL = 'https://www.googleapis.com/books/v1/volumes?q=search+terms'

#Get the top 5 books that match the search query
def get_top5_books(query: str) -> List[Dict]:
    """ 
    Fetches the top 5 books from Google Books API based on the search query.
    """
    params = {
        'q': query,
        'key': GOOGLE_BOOKS_KEY,
        'maxResults': 5,
    }
    qResponse = requests.get(BASE_URL, params=params)
    qResponse.raise_for_status()  # Raise an error for bad response
    qData = qResponse.json()

    #separate results into a list of dictionaries
    items = qData.get('items', [])[:5]
    results = []
    for item in items:
        book_info = item.get("volumeInfo", {})
        results.append({
            "volume_id": item.get("id"),
            "title": book_info.get("title", "No title available"),
            "authors": book_info.get("authors", []),
        })
    
    return results