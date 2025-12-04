# src/models/transaction.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    id: Optional[int]
    user_id: int
    book_id: int
    action: str  # 'borrow' | 'return' | 'reserve'
    timestamp: Optional[str] = None

    def to_row(self):
        return (self.user_id, self.book_id, self.action)
