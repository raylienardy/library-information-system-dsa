# src/data_structures/graph.py
from typing import Dict, Optional, Set


class Graph:
    """
    Undirected weighted graph using adjacency dict:
        {node: {neighbor: weight, ...}, ...}
    Nodes can be any hashable object (e.g., book id).
    """

    def __init__(self):
        self._adj: Dict[object, Dict[object, float]] = {}

    def add_node(self, node: object) -> None:
        self._adj.setdefault(node, {})

    def add_edge(self, a: object, b: object, weight: float = 1.0) -> None:
        self.add_node(a)
        self.add_node(b)
        # undirected: store both directions
        self._adj[a][b] = self._adj[a].get(b, 0) + weight
        self._adj[b][a] = self._adj[b].get(a, 0) + weight

    def neighbors(self, node: object) -> Dict[object, float]:
        return dict(self._adj.get(node, {}))

    def nodes(self) -> Set[object]:
        return set(self._adj.keys())

    def degree(self, node: object) -> int:
        return len(self._adj.get(node, {}))

    def edge_weight(self, a: object, b: object) -> Optional[float]:
        return self._adj.get(a, {}).get(b)

    def __repr__(self) -> str:
        return f"Graph(nodes={len(self._adj)})"
