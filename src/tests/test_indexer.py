# src/tests/test_indexer.py
import unittest
from indexer import Indexer
from persistence.db import init_db
from persistence.repo import BookRepo
from models.book import Book

class TestIndexer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        # ensure there are some books
        BookRepo.add(Book(id=None, title="Alpha Book", author="A", tags=["x"], copies=1))
        BookRepo.add(Book(id=None, title="Beta Book", author="B", tags=["y"], copies=1))

    def test_build_and_search(self):
        idx = Indexer()
        idx.build()
        self.assertTrue(len(idx.search_by_title_prefix("Al"))>0)
        self.assertTrue(len(idx.search_by_tag("x"))>0)

if __name__ == "__main__":
    unittest.main()
