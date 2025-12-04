# src/tests/test_persistence.py
import unittest
import os
from persistence.db import init_db, DB_PATH, get_conn
from persistence.repo import BookRepo, UserRepo, TransactionRepo
from models.book import Book

class TestPersistence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ensure fresh DB by removing if exists
        try:
            if os.path.exists(DB_PATH):
                os.remove(DB_PATH)
        except Exception:
            pass
        init_db()

    def test_user_crud_and_auth(self):
        uid = UserRepo.add("testuser", "secret123")
        self.assertIsInstance(uid, int)
        user = UserRepo.get_by_username("testuser")
        self.assertIsNotNone(user)
        self.assertTrue(UserRepo.verify_credentials("testuser", "secret123"))
        self.assertFalse(UserRepo.verify_credentials("testuser", "wrong"))

    def test_book_crud_search(self):
        book = Book(id=None, title="Belajar Python", author="Admin", tags=["python","pemrograman"], copies=2)
        bid = BookRepo.add(book)
        self.assertIsInstance(bid, int)
        got = BookRepo.get_by_id(bid)
        self.assertIsNotNone(got)
        self.assertEqual(got.title, "Belajar Python")
        got.title = "Belajar Python Lanjutan"
        self.assertTrue(BookRepo.update(got))
        found = BookRepo.search("Lanjutan")
        self.assertTrue(any(b.id == bid for b in found))
        self.assertTrue(BookRepo.delete(bid))
        self.assertIsNone(BookRepo.get_by_id(bid))

    def test_transaction(self):
        uid = UserRepo.add("txuser", "pw")
        book = Book(id=None, title="Tx Book", author="A", tags=[], copies=1)
        bid = BookRepo.add(book)
        tid = TransactionRepo.add(uid, bid, "borrow")
        self.assertIsInstance(tid, int)
        trans = TransactionRepo.list_for_user(uid)
        self.assertTrue(len(trans) >= 1)

if __name__ == "__main__":
    unittest.main()
