# src/controllers/app_controller.py
from typing import List, Optional

from indexer import Indexer
from models.book import Book
from persistence.repo import BookRepo
from services.recommendation import recommend
from services.transaction_service import enqueue_request, process_next, queue_size, undo_last
from services.user_service import AuthError, login_user, register_user
from session import session_manager

# single indexer instance for the app lifetime
_indexer = Indexer()


def init_app():
    """Call at startup to build indexes (after DB init)."""
    _indexer.build()


# --- Auth / user ---
def do_register(username: str, password: str):
    return register_user(username, password)


def do_login(username: str, password: str):
    user = login_user(username, password)
    session_manager.login(user.id, user.username)
    return user


def do_logout():
    session_manager.logout()


def current_username() -> Optional[str]:
    return session_manager.get_username()


def current_user_id() -> Optional[int]:
    return session_manager.get_user_id()


# --- Books / CRUD ---
def list_books():
    return BookRepo.list_all()


def add_book(title: str, author: str, tags: List[str], copies: int = 1) -> int:
    b = Book(id=None, title=title, author=author, tags=tags, copies=copies)
    bid = BookRepo.add(b)
    _indexer.build()
    return bid


def edit_book(book_id: int, title: str, author: str, tags: List[str], copies: int) -> bool:
    b = BookRepo.get_by_id(book_id)
    if not b:
        return False
    b.title = title
    b.author = author
    b.tags = tags
    b.copies = copies
    ok = BookRepo.update(b)
    _indexer.build()
    return ok


def delete_book(book_id: int) -> bool:
    ok = BookRepo.delete(book_id)
    if ok:
        _indexer.build()
    return ok


# --- Search ---
def search(title: str = None, author: str = None, tag: str = None):
    # return list of Book objects
    ids = _indexer.search_multi(title=title, author=author, tag=tag)
    # If no criteria, return all
    if not ids and not (title or author or tag):
        return BookRepo.list_all()
    # If index returned empty but title provided, try fallback scanning
    books = []
    for bid in ids:
        b = BookRepo.get_by_id(bid)
        if b:
            books.append(b)
    return books


# --- Transactions: queue & undo through transaction_service ---
def enqueue_borrow(book_id: int):
    uid = current_user_id()
    if not uid:
        raise AuthError("Harus login untuk meminjam")
    enqueue_request(uid, book_id)


def process_next_request():
    return process_next()


def undo_last_transaction():
    return undo_last()


def get_queue_size():
    return queue_size()


# --- Recommendation ---
def recommend_for(book_id: int, k: int = 5):
    recs = recommend(book_id, k)
    # return list of (Book, score)
    results = []
    for bid, score in recs:
        b = BookRepo.get_by_id(bid)
        if b:
            results.append((b, score))
    return results
