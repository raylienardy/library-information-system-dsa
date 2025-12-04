# src/tests/test_transaction_integration.py
import os
import unittest

from models.book import Book
from persistence.db import DB_PATH, init_db
from persistence.repo import BookRepo, UserRepo
from services.recommendation import recommend
from services.transaction_service import clear_queue, enqueue_request, process_next, undo_last


class TestTransactionIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            if DB_PATH.exists():
                os.remove(DB_PATH)
        except Exception:
            pass
        init_db()
        # create users and books
        cls.u1 = UserRepo.add("int_user1", "pw")
        cls.b1 = BookRepo.add(Book(id=None, title="Int Book 1", author="X", tags=["t1"], copies=1))
        cls.b2 = BookRepo.add(Book(id=None, title="Int Book 2", author="Y", tags=["t2"], copies=1))

    def test_enqueue_process_undo_and_recommendation(self):
        # clear queue if any
        clear_queue()
        enqueue_request(self.u1, self.b1)
        tid = process_next()
        self.assertIsNotNone(tid)
        # enqueue second and process
        enqueue_request(self.u1, self.b2)
        tid2 = process_next()
        self.assertIsNotNone(tid2)
        # now recommend for b1 should include b2
        recs = recommend(self.b1, k=5)
        ids = [bid for bid, _ in recs]
        self.assertIn(self.b2, ids)
        # undo last (should remove tid2)
        ok = undo_last()
        self.assertTrue(ok)
