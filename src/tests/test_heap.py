# src/tests/test_heap.py
import unittest

from data_structures.heap import top_k_items


class TestHeapHelper(unittest.TestCase):
    def test_top_k(self):
        pairs = [("a", 5), ("b", 1), ("c", 10), ("d", 7)]
        top2 = top_k_items(pairs, 2)
        self.assertEqual(top2, ["c", "d"])


if __name__ == "__main__":
    unittest.main()
