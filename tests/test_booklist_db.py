#Here we can test our boolist database to make sure it is correctly storing the updated reading list for our user with all of the right info
import unittest
from app.book_list_db import create_connection, set_up, add_book, delete_book, get_book_id, get_all_books, get_books_by_status

class TestBookListDB(unittest.TestCase):
    '''
    Test cases for book list database operations.
    '''
    def setUp(self):
        self.con = create_connection(':memory:')  # Use an in-memory database for testing
        set_up(self.con)

    def tearDown(self):
        self.con.close()

    def test_add_book(self):
        '''
        Test adding a book to the database and getting it back.
        '''
        add_book(self.con, "Book A", "Author A", "Summary A")
        books = get_all_books(self.con)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0][1], "Book A")
        self.assertEqual(books[0][2], "Author A")
        self.assertEqual(books[0][3], "TBR")
        self.assertEqual(books[0][4], "Summary A")

    def test_get_all_books(self):
        '''
        Test retrieving all books from the database.
        '''
        add_book(self.con, "Book A", "Author A", "Summary A")
        add_book(self.con, "Book B", "Author B", "Summary B")
        books = get_all_books(self.con)
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0][1], "Book A")
        self.assertEqual(books[1][1], "Book B")

    def test_delete_book(self):
        '''
        Test deleting a book from the database.
        '''
        add_book(self.con, "Book A", "Author A", "Summary A")
        book_id = get_book_id(self.con, "Book A")
        self.assertIsNotNone(book_id)
        delete_book(self.con, book_id)
        books = get_all_books(self.con)
        self.assertEqual(len(books), 0)

    def test_get_book_id(self):
        '''
        Test retrieving a book ID by title.
        '''
        add_book(self.con, "Book A", "Author A", "Summary A")
        book_id = get_book_id(self.con, "Book A")
        self.assertIsNotNone(book_id)
        self.assertEqual(book_id, 1)

    def test_get_books_by_status(self):
        '''
        Test retrieving books by status.
        '''
        add_book(self.con, "Book A", "Author A", "Summary A")
        add_book(self.con, "Book B", "Author B", "Summary B")
        books = get_books_by_status(self.con, "TBR")
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0][1], "Book A")
        self.assertEqual(books[1][1], "Book B")

    def test_get_books_by_status_empty(self):
        '''
        Test retrieving books by status when no books match.
        '''
        books = get_books_by_status(self.con, "TBR")
        self.assertEqual(len(books), 0)

    def test_update_book_status(self):
        '''
        Test updating the status of a book.
        '''
        add_book(self.con, "Book A", "Author A", "Summary A")
        book_id = get_book_id(self.con, "Book A")
        self.assertIsNotNone(book_id)