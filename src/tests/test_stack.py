# src/tests/test_stack.py
import unittest

from data_structures.stack import Stack


class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack[int]()
        s.push(1)
        s.push(2)
        self.assertEqual(s.size(), 2)
        self.assertEqual(s.peek(), 2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())

    def test_pop_empty(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()


if __name__ == "__main__":
    unittest.main()
