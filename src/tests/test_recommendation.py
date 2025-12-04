# src/tests/test_recommendation.py
import unittest

from models.book import Book
from persistence.db import init_db
from persistence.repo import BookRepo, TransactionRepo, UserRepo
from services.recommendation import recommend


class TestRecommendation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.u1 = UserRepo.add("rec_user1", "pw")
        cls.u2 = UserRepo.add("rec_user2", "pw")
        cls.b1 = BookRepo.add(Book(id=None, title="R1", author="A", tags=[], copies=1))
        cls.b2 = BookRepo.add(Book(id=None, title="R2", author="B", tags=[], copies=1))
        cls.b3 = BookRepo.add(Book(id=None, title="R3", author="C", tags=[], copies=1))
        # user1 borrowed b1 and b2
        TransactionRepo.add(cls.u1, cls.b1, "borrow")
        TransactionRepo.add(cls.u1, cls.b2, "borrow")
        # user2 borrowed b1 and b3
        TransactionRepo.add(cls.u2, cls.b1, "borrow")
        TransactionRepo.add(cls.u2, cls.b3, "borrow")

    def test_recommend(self):
        recs = recommend(self.b1, k=2)
        # should recommend b2 and b3
        ids = [bid for bid, _ in recs]
        self.assertIn(self.b2, ids)
        self.assertIn(self.b3, ids)


if __name__ == "__main__":
    unittest.main()
