#Here we can test the Google books API to make sure it is correctly retrieving the top 5 book matches based off of the user's search query
import requests
import pytest

from app.google_books import get_top5_books
#from app.config import GOOGLE_BOOKS_KEY

#First we make a dummy response object to simulate the API response

class DummyResponse:
    def __init__ (self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP Error: {self.status_code} Error")
   
    def test_returns_five_books_when_available(monkeypatch):

        #make 6 fake book items and then make sure only the top 5 are returned
        dummy_data = [{"id": f"id_{i}", "volumeInfo": {"title": f"title_{i}", "authors": [f"Author_{i}"]}} for i in range(1,7)]
      
        dummy_response = {"items": dummy_data}

        def dummy_get(url, params):
            #make sure params are correct
            assert params['q'] == 'test query'
            assert params["maxResults"] == 5
            return DummyResponse(dummy_response, status_code=200)

        #Patch the requests.get method to return our dummy response
        monkeypatch.setattr("app.google_books.requests.get", dummy_get)

        results = get_top5_books("test query")
        assert isinstance(results, list)
        assert len(results) == 5
        #Check content of first and last book
        assert results[0]['title'] == {"volume_id": "id_1", "title": "title_1", "authors": ["Author_1"]}
        assert results[-1]['volume_id'] == 'id_5'
    
    def test_returns_all_books_when_less_than_five(monkeypatch):
        dummy_data = [{"id": f"id_{i}", "volumeInfo": {"title": f"title_{i}", "authors": [f"Author_{i}"]}} for i in range(1, 4)]
        dummy_response = {"items": dummy_data}

        def dummy_get(url, params):
            return DummyResponse(dummy_response, status_code=200)

        monkeypatch.setattr("app.google_books.requests.get", dummy_get)

        results = get_top5_books("short list query")
        assert isinstance(results, list)
        assert len(results) == 3
        for i, book in enumerate(results):
            assert book["volume_id"] == f"id_{i}"
    
    def test_defaults_for_missing_fields(monkeypatch):
        dummy_data = [{"id": "no_info", "volumeInfo": {}}]
        dummy_response = {"items": dummy_data}

        def dummy_get(url, params):
            return DummyResponse(dummy_response, status_code=200)
        
        monkeypatch.setattr("app.google_books.requests.get", dummy_get)

        results = get_top5_books("missing fields query")
        assert isinstance(results, list)
        assert len(results) == 1
        book = results[0]
        assert book["volume_id"] == "no_info"
        assert book["title"] == "No title available"
        assert book["authors"] == []
    
    def test_raises_http_error_on_bad_response(monkeypatch):

        # Simulate a bad response from the API
        def dummy_get(url, params):
            return DummyResponse({}, status_code=500)

        monkeypatch.setattr("app.google_books.requests.get", dummy_get)

        with pytest.raises(requests.HTTPError):
            get_top5_books("bad response query")
