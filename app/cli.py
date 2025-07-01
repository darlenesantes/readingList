#Here we can set up the command line interface - make sure we search for a book, add a book to the list, and retrieve the list from the db
import json
from pathlib import Path

import click

from app.config import DATABASE_URL
from app.google_books import get_top5_books
from app.genai import generate_summary
from app.book_list_db import set_up, add_book, get_all_books, delete_book, get_book_id



