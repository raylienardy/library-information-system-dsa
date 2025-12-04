# src/tests/test_hashtable.py
import unittest

from data_structures.hashtable import HashTable


class TestHashTable(unittest.TestCase):
    def test_set_get_remove(self):
        ht = HashTable[str, int](capacity=5)
        ht.set("a", 1)
        ht.set("b", 2)
        self.assertEqual(ht.get("a"), 1)
        self.assertEqual(ht.get("b"), 2)
        self.assertTrue(ht.contains("a"))
        self.assertTrue(ht.remove("a"))
        self.assertFalse(ht.contains("a"))
        self.assertIsNone(ht.get("a"))


if __name__ == "__main__":
    unittest.main()
