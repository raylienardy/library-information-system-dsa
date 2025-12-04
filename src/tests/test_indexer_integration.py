# src/tests/test_indexer_integration.py
import os
import unittest

from indexer import Indexer
from models.book import Book
from persistence.db import DB_PATH, init_db
from persistence.repo import BookRepo


class TestIndexerIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # fresh DB
        try:
            if DB_PATH.exists():
                os.remove(DB_PATH)
        except Exception:
            pass
        init_db()
        # create sample data
        BookRepo.add(Book(id=None, title="Alpha One", author="A", tags=["x"], copies=1))
        BookRepo.add(Book(id=None, title="Alpha Two", author="A", tags=["x", "y"], copies=2))
        BookRepo.add(Book(id=None, title="Beta Three", author="B", tags=["z"], copies=1))

    def test_indexer_search(self):
        idx = Indexer()
        idx.build()
        exact = idx.search_by_title_exact("Alpha One")
        self.assertTrue(len(exact) >= 1)
        prefix = idx.search_by_title_prefix("Alpha")
        self.assertTrue(len(prefix) >= 2)
        tags = idx.search_by_tag("x")
        self.assertTrue(len(tags) >= 2)
        authors = idx.search_by_author("A")
        self.assertTrue(len(authors) >= 2)
