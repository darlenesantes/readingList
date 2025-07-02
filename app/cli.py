#Getting rid of weird warnings in the terminal
import warnings
from urllib3.exceptions import NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

#Here we can set up the command line interface - make sure we search for a book, add a book to the list, and retrieve the list from the db
import json
from pathlib import Path

import click

from app.config import DATABASE_URL
from app.google_books import get_top5_books
from app.genai import generate_summary
from app.book_list_db import create_connection, set_up, add_book, get_all_books, get_books_by_status, update_book_status, get_book_id, delete_book

#Store the last search so that the 'add_book' command knows which book to add
LAST_SEARCH = Path('last_search.json')

def get_db_connection():
    """ Create and return new sqlite database connection """
    conn = create_connection()
    return conn

def initialize():
    """ Make sure the database table exists """
    conn = get_db_connection()
    set_up(conn)
    conn.close()

@click.group()
def cli():
    """ Command line interface for managing your reading list! """
    initialize()

@cli.command()
@click.argument('query', type=str, nargs=-1)

def search(query):
    """ Search the Google Books API for the query and show the top 5 results with AI summaries """
    q = ' '.join(query).strip()
    if not q:
        click.echo("Please provide a search query!")
        return
    
    #Get top 5 query results
    try:
        books = get_top5_books(q)
    except Exception as e:
        click.echo(f"Error fetching books: {e}")
        return
    
    if not books:
        click.echo(f"No results found for '{q}'. Please try a different query!")
        return
    
    data = []
    click.echo(f"Top {len(books)} results for \'{q}\':\n")
    #Get ai summaries for each book
    for index, book in enumerate(books, start = 1):
        title = book["title"]
        if book.get("authors"):
            authors = book["authors"]
        elif book.get("author"):
            authors = book["author"]
        else:
            authors = ["Unknown"]
        first_author = authors[0]
        try:
            summary = generate_summary(title, first_author)
        except Exception as e:
            click.echo(f"Error generating summary for {title}: {e}")
            summary = "No summary available."
        #Display resulting book info
        click.echo(f"[{index}] {title} by {', '.join(authors)}")
        click.echo(f"Summary: {summary}\n")

        #Store book info for later
        data.append({
            "title": title,
            "author": ", ".join(authors),
            "summary": summary
        })

    #Store the last search results to a file
    with open(LAST_SEARCH, 'w') as file:
        json.dump(data, file, indent=4)
    
    click.echo("Run 'bookclub add <number>' to save one of these books to your reading list!")

@cli.command()
@click.argument('index', type=int)

def add(index):
    """ Add one of the last search results (by its index) to your reading list """
    if not LAST_SEARCH.exists():
        click.echo("No previous search results found. Please run 'bookclub search <query>' first!")
        return
    
    data = json.loads(LAST_SEARCH.read_text())
    if index < 1 or index > len(data):
        click.echo(f"Invalid index. Please choose a number between 1 and {len(data)}.")
        return
    
    table_entry = data[index - 1]
    conn = get_db_connection()

    try:
        was_inserted = add_book(
            conn, 
            table_entry["title"], 
            table_entry["author"], 
            table_entry["summary"]
            )
    finally: 
        conn.close()
    
    if was_inserted:
        click.echo(f"Added {table_entry['title']} by {table_entry['author']} to your reading list.")
    else:
        click.echo(f"{table_entry['title']} by {table_entry['author']} is already in your reading list.")

@cli.command(name = "list")
@click.option(
    "--status",
    type = click.Choice(["TBR", "Reading", "Read"], case_sensitive=False),
    help = "Filter books by their status (TBR, Reading, Read)."
)


def list_books(status):
    """ List all books in reading list along with their ai summaries - optionally filtered by status"""
    conn = get_db_connection()

    try:
        if status:
            rows = get_books_by_status(conn, status)
        else:
            rows = get_all_books(conn)
    except Exception as e:
        click.echo(f"Error retrieving books: {e}")
        return
    finally:
        conn.close()
    
    if not rows:
        click.echo("Your reading list is empty!")
        return
    
    click.echo("Your reading list:\n")
    for index, (_db_id, title, author, status, summary) in enumerate(rows, start=1):
        click.echo(f"{index}. {title} by {author} [{status}]")
        click.echo(f"Summary: {summary}\n")

@cli.command(name = "update-status")
@click.argument('book_id', type = int)
@click.argument('status', type = click.Choice(["TBR", "Reading", "Read"], case_sensitive = False))

def update_status(book_id, status):
    """ Update the reading status of a book in your reading list by id """
    conn = get_db_connection()
    try:
        ok = update_book_status(conn, book_id, status)
    finally:
        conn.close()
    
    if not ok:
        click.echo(f"Book with ID {book_id} not found.")
        raise SystemExit(1)
    click.echo(f"Updated book ID {book_id} status to {status}.")

@cli.command(name = "delete")
@click.argument("index", type = int)

def delete(index):
    "Delete a book from your reading list by its position index in your current list"
    conn = get_db_connection()
    rows = get_all_books(conn)
    #Make sure index is in range
    if index < 1 or index > len(rows):
        click.echo(f"Invalid index. Please choose a number between 1 and {len(rows)}.")
        conn.close()
        return
    #Map the books to their real PK ids
    db_id = rows[index - 1][0]

    #Try to delete the book
    deleted = delete_book(conn, db_id)
    conn.close()

    if not deleted:
        click.echo(f"No book with ID {db_id} found in your reading list.")
    else:
        click.echo(f"Deleted book with ID {index} from your reading list.")
    conn.close()

def get_attr(name):
    """ Dynamic attribute access for tests """
    if name == "LAST_SEARCH":
        return LAST_SEARCH
    raise AttributeError(f"Unknown attribute: {name}")

if __name__ == "__main__":
    cli(prog_name="bookclub")



