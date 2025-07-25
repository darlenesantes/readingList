# File: app/book_list_db.py
# This file contains functions to interact with the SQLite database for
# managing a reading list.

import sqlite3

# DON'T FORGET TO CLOSE CONNECTION AFTER WE ARE DONE MAKING CHANGES TO DB !!!!
# Creating the db
BOOKS_DB = 'reading_list.db'


# Creating a connection to the database for testability
def create_connection(db_name=BOOKS_DB):
    '''
    Creates a connection to the SQLite database
    '''
    con = sqlite3.connect(db_name)
    return con


# Function for creating table name
def set_up(con):
    '''
    Sets up the database by creating a table to hold all book info
    '''
    # create connection cursor
    cursor = con.cursor()
    # create table if it does not already exist
    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS reading_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT DEFAULT 'TBR', -- status: 'TBR', 'Reading', 'Read'
            summary TEXT)
                    ''')
    con.commit()


# Function for adding a book
def add_book(con, title, author, desc):
    '''
    Adds book to reading list database if it does not already exist
    If the book already exists, it will not be added again.
    '''
    cursor = con.cursor()
    # Check if the book already exists
    cursor.execute(
        "SELECT 1 FROM reading_list WHERE title = ? AND author = ?",
        (title, author),
    )
    if cursor.fetchone() is not None:
        # Book already exists, do not add it again
        return False
    # Otherwise, insert the book into the database
    cursor.execute(
        "INSERT INTO reading_list (title, author, summary) VALUES (?, ?, ?)",
        (title, author, desc),
    )
    con.commit()
    return True


# Function for deleting a book
def delete_book(con, book_id):
    '''
    Deletes book from database by its unique ID (primary key)
    '''
    # Create cursor
    cursor = con.cursor()
    # Check if the book exists
    cursor.execute("SELECT 1 FROM reading_list WHERE id = ?", (book_id,))
    if cursor.fetchone() is None:
        return False
    cursor.execute("DELETE FROM reading_list WHERE id = ?", (book_id,))
    con.commit()
    return True


# Function to update book status
def update_book_status(con, book_id, status):
    '''
    Updates status of a book in the reading list database (only if it exists)
    Returns True if the book was updated, False if it was not found
    '''
    cursor = con.cursor()
    # Check existence
    cursor.execute(
        '''SELECT COUNT(1) FROM reading_list WHERE id = ?''',
        (book_id,),
    )
    exists = cursor.fetchone()[0]
    if not exists:
        return False

    # Perform update
    cursor.execute(
        '''UPDATE reading_list SET status = ? WHERE id = ?''',
        (status, book_id),
    )
    con.commit()
    return True


# Function to get book by title
def get_book_id(con, title):
    '''
    Returns book ID from database matching the given title
    '''
    # this could help maybe with error handling?
    # for example, if the return val is empty, we cannot delete the book
    # cursor
    cursor = con.cursor()
    # select from table where title=title
    cursor.execute('''SELECT id FROM reading_list WHERE title = ?''', (title,))
    # fetch one? fetch all?
    book_id = cursor.fetchone()

    # if book_id is None, return None
    if book_id is None:
        return None
    # otherwise, return the first element of the tuple
    return book_id[0]


# Function to get all books
def get_all_books(con):
    '''
    Returns all books stored in the reading list table
    '''
    # cursor
    cursor = con.cursor()
    # select all from table
    cursor.execute('''SELECT * FROM reading_list''')
    # fetchall
    books = cursor.fetchall()

    # return all
    return books


# Function to return books by status
def get_books_by_status(con, status):
    '''
    Returns all books with the given status from the reading list table
    '''
    # connection and cursor
    cursor = con.cursor()
    # select all from table where status=status
    cursor.execute('''SELECT *
                   FROM reading_list WHERE status = ?''',
                   (status,))
    # save to a variable
    books = cursor.fetchall()
    # return the books
    return books


# Function to display maybe? display in a pretty and readble way
def display_books(books):
    '''
    Displays the books in a readable format
    '''
    for book in books:
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, "
              f"Status: {book[3]}, Summary: {book[4]}")
