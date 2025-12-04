# src/data_structures/heap.py
import heapq
from typing import List, Tuple, Any

def top_k_items(pairs: List[Tuple[Any, int]], k: int):
    """
    pairs: list of (item, score)
    returns top-k items by score descending
    """
    if k <= 0:
        return []
    return [item for item, _ in heapq.nlargest(k, pairs, key=lambda x: x[1])]
