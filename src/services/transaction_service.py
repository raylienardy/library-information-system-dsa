# src/services/transaction_service.py
"""
Transaction queue & undo stack.
- enqueue_request(user_id, book_id)
- process_next() -> create TransactionRepo entry and push transaction id to undo stack
- undo_last() -> pop last transaction id and delete it
"""
from typing import Optional, Tuple

from data_structures.queue import Queue
from data_structures.stack import Stack
from persistence.repo import TransactionRepo

_request_queue = Queue()
_undo_stack = Stack()


def enqueue_request(user_id: int, book_id: int) -> None:
    _request_queue.enqueue((user_id, book_id))


def queue_size() -> int:
    return _request_queue.size()


def process_next() -> Optional[int]:
    """Process single queued request. Return transaction id or None if queue empty."""
    if _request_queue.is_empty():
        return None
    user_id, book_id = _request_queue.dequeue()
    # You may want to check book availability here (copies) - omitted for simplicity.
    tid = TransactionRepo.add(user_id, book_id, "borrow")
    if tid:
        _undo_stack.push(tid)
    return tid


def undo_last() -> bool:
    """Undo most recent processed transaction (delete entry)."""
    if _undo_stack.is_empty():
        return False
    tid = _undo_stack.pop()
    return TransactionRepo.delete(tid)


def peek_next() -> Optional[Tuple[int, int]]:
    if _request_queue.is_empty():
        return None
    return _request_queue.peek()


def clear_queue():
    while not _request_queue.is_empty():
        _request_queue.dequeue()
