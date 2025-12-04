# src/data_structures/hashtable.py
from typing import List, Tuple, Optional, TypeVar, Generic

K = TypeVar("K")
V = TypeVar("V")

class HashTable(Generic[K, V]):
    """Simple hash table with separate chaining. Not thread-safe."""
    def __init__(self, capacity: int = 101):
        self.capacity = max(3, capacity)
        self.buckets: List[List[Tuple[K, V]]] = [[] for _ in range(self.capacity)]
        self._size = 0

    def _index(self, key: K) -> int:
        return hash(key) % self.capacity

    def set(self, key: K, value: V) -> None:
        idx = self._index(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        idx = self._index(key)
        bucket = self.buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return default

    def remove(self, key: K) -> bool:
        idx = self._index(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def contains(self, key: K) -> bool:
        return self.get(key) is not None

    def size(self) -> int:
        return self._size

    def keys(self):
        for bucket in self.buckets:
            for k, _ in bucket:
                yield k

    def values(self):
        for bucket in self.buckets:
            for _, v in bucket:
                yield v

    def items(self):
        for bucket in self.buckets:
            for k,v in bucket:
                yield (k,v)

    def __repr__(self) -> str:
        items = list(self.items())
        return f"HashTable({items})"
