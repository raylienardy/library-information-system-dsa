# src/data_structures/queue.py
from collections import deque
from typing import Deque, Generic, TypeVar, Optional

T = TypeVar("T")

class Queue(Generic[T]):
    """FIFO queue using collections.deque."""
    def __init__(self) -> None:
        self._dq: Deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._dq.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._dq.popleft()

    def peek(self) -> Optional[T]:
        return self._dq[0] if self._dq else None

    def is_empty(self) -> bool:
        return len(self._dq) == 0

    def size(self) -> int:
        return len(self._dq)

    def __repr__(self) -> str:
        return f"Queue({list(self._dq)})"
