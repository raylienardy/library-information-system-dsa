# src/data_structures/stack.py
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class Stack(Generic[T]):
    """Simple LIFO stack backed by Python list."""
    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, item: T) -> None:
        """Push item onto stack."""
        self._data.append(item)

    def pop(self) -> T:
        """Pop and return top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Optional[T]:
        """Return top item without removing, or None if empty."""
        return self._data[-1] if self._data else None

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"
