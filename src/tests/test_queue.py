# src/tests/test_queue.py
import unittest

from data_structures.queue import Queue


class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = Queue[int]()
        q.enqueue(10)
        q.enqueue(20)
        self.assertEqual(q.size(), 2)
        self.assertEqual(q.peek(), 10)
        self.assertEqual(q.dequeue(), 10)
        self.assertEqual(q.dequeue(), 20)
        self.assertTrue(q.is_empty())

    def test_dequeue_empty(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()


if __name__ == "__main__":
    unittest.main()
