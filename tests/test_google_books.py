import requests
import pytest

from app.google_books import get_top5_books

# First we make a DummyResponse class to simulate "requests" responses for testing
class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP Error: {self.status_code} Error")


def test_returns_five_books_when_available(monkeypatch):
    """ If more than five items are returned, only the top five should be returned """
    dummy_items = [
        {"id": f"id_{i}", "volumeInfo": {"title": f"title_{i}", "authors": [f"Author_{i}"]}}
        for i in range(1, 7)
    ]
    dummy_payload = {"items": dummy_items}

    def dummy_get(url, params):
        # Make sure request parameters include intitle prefix
        assert params['q'] == 'intitle:test query'
        assert params['maxResults'] == 5
        return DummyResponse(dummy_payload, status_code=200)

    monkeypatch.setattr("app.google_books.requests.get", dummy_get)

    results = get_top5_books("test query")
    assert isinstance(results, list)
    assert len(results) == 5
    # Check the first and last items
    expected_first = {"volume_id": "id_1", "title": "title_1", "authors": ["Author_1"]}
    expected_last = {"volume_id": "id_5", "title": "title_5", "authors": ["Author_5"]}
    assert results[0] == expected_first
    assert results[-1] == expected_last


def test_returns_all_books_when_less_than_five(monkeypatch):
    """ If less than five items are available, return them all in order """
    dummy_items = [
        {"id": f"id_{i}", "volumeInfo": {"title": f"title_{i}", "authors": [f"Author_{i}"]}}
        for i in range(1, 4)
    ]
    dummy_payload = {"items": dummy_items}

    def dummy_get(url, params):
        assert params['q'] == 'intitle:short list query'
        return DummyResponse(dummy_payload, status_code=200)

    monkeypatch.setattr("app.google_books.requests.get", dummy_get)

    results = get_top5_books("short list query")
    assert isinstance(results, list)
    assert len(results) == 3
    for idx, book in enumerate(results, start=1):
        assert book["volume_id"] == f"id_{idx}"


def test_defaults_for_missing_fields(monkeypatch):
    """ Default values should apply when volumeInfo fields are missing """
    dummy_items = [{"id": "no_info", "volumeInfo": {}}]
    dummy_payload = {"items": dummy_items}

    def dummy_get(url, params):
        assert params['q'] == 'intitle:missing fields query'
        return DummyResponse(dummy_payload, status_code=200)

    monkeypatch.setattr("app.google_books.requests.get", dummy_get)

    results = get_top5_books("missing fields query")
    assert isinstance(results, list)
    assert len(results) == 1
    book = results[0]
    assert book["volume_id"] == "no_info"
    assert book["title"] == "No title available"
    assert book["authors"] == []


def test_returns_empty_list_on_bad_response(monkeypatch):
    """ On HTTP errors, the function should return an empty list"""
    def dummy_get(url, params):
        assert params['q'] == 'intitle:bad response query'
        return DummyResponse({}, status_code=500)

    monkeypatch.setattr("app.google_books.requests.get", dummy_get)

    results = get_top5_books("bad response query")
    assert isinstance(results, list)
    assert results == []
