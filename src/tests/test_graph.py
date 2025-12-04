# src/tests/test_graph.py
import unittest

from data_structures.graph import Graph


class TestGraph(unittest.TestCase):
    def test_add_edge_neighbors(self):
        g = Graph()
        g.add_edge("A", "B", weight=2)
        g.add_edge("A", "C", weight=3)
        self.assertEqual(g.edge_weight("A", "B"), 2)
        self.assertEqual(g.edge_weight("B", "A"), 2)
        self.assertEqual(set(g.neighbors("A").keys()), {"B", "C"})
        self.assertIn("A", g.nodes())


if __name__ == "__main__":
    unittest.main()
