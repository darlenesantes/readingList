import json
import sqlite3
import pytest
from click.testing import CliRunner

import app.cli as cli_module
from app.cli import cli
from app.book_list_db import set_up

@pytest.fixture(autouse = True)
def isolate(tmp_path, monkeypatch):
    """ Isolate the test environment by creating a temporary database. """
    #Redirect the last search file to a temporary location
    cache = tmp_path / "last_search.json"
    monkeypatch.setattr(cli_module, "LAST_SEARCH", str(cache))

    #Use a temporary sqlite database
    db_path = tmp_path / "test.db"
    def get_db():
        return sqlite3.connect(str(db_path))
    monkeypatch.setattr(cli_module, "get_db_connection", get_db)
    
    #Create the database schema
    conn = get_db()
    set_up(conn)
    conn.close()
    
def test_search_and_cache(monkeypatch, tmp_path):
    """ Test the search command and ensure results are cached. """
    #Stub the APIs
    monkeypatch.setattr(cli_module, "get_top5_books", lambda q: [
        {"title": "Python Programming", "authors": ["Demi"]},])
    monkeypatch.setattr(cli_module, "generate_summary", lambda t, a: "AI Summary")

    runner = CliRunner()
    result = runner.invoke(cli, ["search", "Python programming"])
    assert result.exit_code == 0
    assert "Python Programming by Demi" in result.output
    assert "AI Summary" in result.output

    #Check if the last search was cached
    data = json.loads((tmp_path / "last_search.json").read_text())
    assert data == [{"title": "Python Programming", "author": "Demi", "summary": "AI Summary"}]

def test_list_status():
    #Insert entries with different statuses
    conn = cli_module.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reading_list (title, author, status, summary) VALUES (?, ?, ?, ?)",
                ("Book A","Author A","TBR","Summary A"))
    cursor.execute("INSERT INTO reading_list (title, author, status, summary) VALUES (?, ?, ?, ?)",
                ("Book B","Author B","Read","Summary B"))
    conn.commit(); conn.close()

    runner = CliRunner()
    result_all = runner.invoke(cli, ["list"])
    assert "Book A" in result_all.output and "Book B" in result_all.output

    result_filtered = runner.invoke(cli, ["list", "--status", "Read"])
    assert "Book A" not in result_filtered.output
    assert "Book B" in result_filtered.output

def test_update_status():
    #Insert a to be read book
    conn = cli_module.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reading_list (title, author, status, summary) VALUES (?, ?, ?, ?)",
                ("Book C","Author C","TBR","Summary C"))
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()

    runner = CliRunner()
    result = runner.invoke(cli, ["update-status", str(book_id), "Reading"])
    assert result.exit_code == 0
    assert f"Updated book ID {book_id} status to Reading" in result.output

    result_reading = runner.invoke(cli, ["list", "--status", "Reading"])
    assert "Book C" in result_reading.output
    result_tbr = runner.invoke(cli, ["list", "--status", "TBR"])
    assert "Book C" not in result_tbr.output

def test_delete_book():
    #Insert a book to delete
    conn = cli_module.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reading_list (title, author, status, summary) VALUES (?, ?, ?, ?)",
                ("Book D","Author D","TBR","Summary D"))
    conn.commit()
    book_id = cursor.lastrowid
    conn.close()

    runner = CliRunner()
    #Delete the book
    result = runner.invoke(cli, ["delete", str(book_id)])
    assert result.exit_code == 0
    assert f"Deleted book with ID {book_id} from your reading list." in result.output

    #Check if the book was actually deleted
    result_list = runner.invoke(cli, ["list"])
    assert f"Book D by Author D [TBR]" not in result_list.output