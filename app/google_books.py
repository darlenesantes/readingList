#Here we'll call the Google Books API to retrieve book information based on a search query.
import requests
from typing import List, Dict

from app.config import GOOGLE_BOOKS_KEY

BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

#Get the top 5 books that match the search query
def get_top5_books(query: str) -> List[Dict]:
    """ 
    Fetches the top 5 books from Google Books API based on the search query.
    """
    if not query:
        return []
    
    results = []
    seen_ids = set()  # To avoid duplicates

    #Helper to process API responses
    def fetch_and_add(params: Dict):
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            items = response.json().get('items', [])
        except Exception:
            return
        for item in items:
            volume_id = item.get('id')
            if volume_id and volume_id not in seen_ids:
                seen_ids.add(volume_id)
                book_info = item.get("volumeInfo", {})
                results.append({
                    "volume_id": volume_id,
                    "title": book_info.get("title", "No title available"),
                    "authors": book_info.get("authors", []),
                })
    
    #Search by title first
    fetch_and_add({
        'q': f'intitle:{query}',
        'key': GOOGLE_BOOKS_KEY,
        'maxResults': 5,
    })

    #If we don't have enough results, search by author
    if len(results) < 5:
        fetch_and_add({
            'q': f'inauthor:{query}',
            'key': GOOGLE_BOOKS_KEY,
            'maxResults': 5 - len(results),
        })
    
    return results[:5]