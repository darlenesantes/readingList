# BookBase
A command-line interface (CLI) tool to search for books, generate AI-powered summaries, and manage your personal reading list with status tracking.

Built with Python, the Google Books API, Google GenAI, and SQLite for local data storage.

## Features
- Search for books via Google Books API and view the top 5 results with AI-generated summaries

- Add selected books from search results to your personal reading list

- List all books in your reading list, with optional filtering by reading status (TBR, Reading, Read)

- Update the reading status of books in your list

- Delete books from your reading list

- Local persistence using SQLite

## Installation
1. Clone the repository and navigate into it.

2. Create and activate a Python virtual environment (recommended):

### macOS:
```
source venv/bin/activate
```

### Windows:
```
venv\Scripts\activate
```

3. Install the package in editable mode. This will install your package and all required dependencies:

```
pip install -e .
```
After this step, all dependencies are installed and you can start using the CLI commands.

## Usage
Run the CLI command bookclub:

```
python -m bookclub <command> [arguments]
```

Or, if installed as a script:

```
bookclub <command> [arguments]
```

## Commands

### search \<query>
Search for books matching \<query> using the Google Books API. Shows top 5 results with AI-generated summaries.

#### Example:

```
bookclub search harry potter
```

### add \<number>

Add one of the last search results to your reading list by its index number.

#### Example:

```
bookclub add 2
```

### list [--status \<status>]
List all books in your reading list, optionally filtered by status (TBR, Reading, Read).

#### Examples:

```
bookclub list
bookclub list --status TBR
```

### update-status \<book_id> \<status>
Update the reading status of a book in your reading list by its database ID.

#### Example:

```
bookclub update-status 3 Reading
```
### delete \<index>
Delete a book from your reading list by its position index in the current list.

#### Example:

```
bookclub delete 4
```

## How It Works
- Search: Queries Google Books API for top 5 matching books, generates AI summaries per book.

- Add: Saves selected book from last search to SQLite database along with its summary.

- List: Retrieves and displays stored books with optional filtering by reading status.

- Update-status: Updates the reading status (TBR, Reading, or Read) of a specific book by its ID.

- Delete: Removes a book from the list based on its position in the current displayed list.

### Requirements
- click for CLI commands

- API keys/configuration for Google Books and AI summary generation (stored in app/config.py)

- SQLite (bundled with Python)

### Development
- Database management functions in app/book_list_db.py

- Google Books API integration in app/google_books.py

- AI summary generation in app/genai.py

- Configuration and API keys in app/config.py
