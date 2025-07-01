# Here we can set up booklist database to store the user's reading list w/ right info
import sqlite3

# DON'T FORGET TO CLOSE CONNECTION IN EACH FUNCTION !!!!
# Creating the db
BOOKS_DB = 'reading_list.db'

# Function for creating table name
def set_up():
    '''
    Sets up the database by creating a table to hold all book info
    '''
    # create connection
    con = sqlite3.connect(BOOKS_DB)
    # create connection cursor
    cursor = con.cursor()
    # create table if it does not already exist
    cursor.execute(''' CREATE TABLE IF NOT EXISTS reading_list (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   author TEXT NOT NULL,
                   summary TEXT)
                   ''') # maybe add reading status as field?
    con.commit()
    con.close()

# Function for adding a book
def add_book(title, author, desc):
    '''
    Adds book to reading list database
    '''
    # create connection
    # create cursor
    # cursor.execute: insert the information except for index

# Function for deleting a book
def delete_book(book_id):
    '''
    Deletes book from database by its unique ID (primary key)
    '''
    # create connection and cursor
    # delete from tablename where id=id
    # connection commit

# Function to get book by title
def get_book_id(title):
    '''
    Returns book ID from database matching the given title
    '''
    # this could help maybe with error handling?
    # for example, if the return val is empty, we cannot delete the book
    # connection and cursor
    # select from table where title=title
    # fetch one? fetch all?

# Function to get all books
def get_all_books():
    '''
    Returns all books stored in the reading list table
    '''
    # connection and cursor
    # select all from table
    # fetchall
    # return all

# Function to display maybe? display in a pretty and readble way
