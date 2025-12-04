# src/tests/test_bst.py
import unittest
from data_structures.bst import BST

class TestBST(unittest.TestCase):
    def test_insert_find_inorder(self):
        bst = BST[int, str]()
        bst.insert(10, "ten")
        bst.insert(5, "five")
        bst.insert(15, "fifteen")
        self.assertEqual(bst.find(10), "ten")
        self.assertEqual(bst.find(5), "five")
        self.assertEqual(bst.find(15), "fifteen")
        self.assertIsNone(bst.find(999))
        self.assertEqual([k for k,_ in bst.inorder()], [5,10,15])

if __name__ == "__main__":
    unittest.main()
