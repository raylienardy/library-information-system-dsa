# src/data_structures/bst.py
from typing import Optional, List, Tuple, Generic, TypeVar, Callable

K = TypeVar("K")
V = TypeVar("V")

class BSTNode(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key: K = key
        self.value: V = value
        self.left: Optional['BSTNode[K, V]'] = None
        self.right: Optional['BSTNode[K, V]'] = None

    def __repr__(self) -> str:
        return f"BSTNode({self.key}:{self.value})"

class BST(Generic[K, V]):
    """Binary Search Tree with insert/find/inorder traversal."""
    def __init__(self, cmp: Optional[Callable[[K, K], int]] = None):
        # cmp: optional compare function; default uses built-in ordering
        self.root: Optional[BSTNode[K, V]] = None
        self._cmp = cmp

    def _compare(self, a: K, b: K) -> int:
        if self._cmp:
            return self._cmp(a, b)
        # type: ignore - rely on builtin comparison
        return (a > b) - (a < b)

    def insert(self, key: K, value: V) -> None:
        def _insert(node: Optional[BSTNode[K,V]], key: K, value: V) -> BSTNode[K,V]:
            if node is None:
                return BSTNode(key, value)
            if self._compare(key, node.key) < 0:
                node.left = _insert(node.left, key, value)
            elif self._compare(key, node.key) > 0:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value  # update
            return node
        self.root = _insert(self.root, key, value)

    def find(self, key: K) -> Optional[V]:
        node = self.root
        while node:
            cmp = self._compare(key, node.key)
            if cmp == 0:
                return node.value
            node = node.left if cmp < 0 else node.right
        return None

    def inorder(self) -> List[Tuple[K, V]]:
        res: List[Tuple[K,V]] = []
        def _in(node: Optional[BSTNode[K,V]]):
            if not node:
                return
            _in(node.left)
            res.append((node.key, node.value))
            _in(node.right)
        _in(self.root)
        return res

    def __repr__(self) -> str:
        return f"BST({self.inorder()})"
