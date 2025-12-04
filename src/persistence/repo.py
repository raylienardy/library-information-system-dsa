# src/persistence/repo.py
import json
from typing import List, Optional

from auth import hash_password, verify_password
from models.book import Book
from models.transaction import Transaction
from models.user import User

from .db import get_conn


class BookRepo:
    @staticmethod
    def add(book: Book) -> int:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, tags, copies) VALUES (?, ?, ?, ?)", book.to_row()
        )
        conn.commit()
        book_id = cur.lastrowid
        conn.close()
        return book_id

    @staticmethod
    def get_by_id(book_id: int) -> Optional[Book]:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cur.fetchone()
        conn.close()
        return Book.from_row(row)

    @staticmethod
    def update(book: Book) -> bool:
        if book.id is None:
            return False
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE books SET title=?, author=?, tags=?, copies=? WHERE id=?",
            (book.title, book.author, json.dumps(book.tags), book.copies, book.id),
        )
        conn.commit()
        changed = cur.rowcount > 0
        conn.close()
        return changed

    @staticmethod
    def delete(book_id: int) -> bool:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok

    @staticmethod
    def list_all() -> List[Book]:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        conn.close()
        return [Book.from_row(r) for r in rows]

    @staticmethod
    def search(term: str) -> List[Book]:
        # simple search over title or author or tags (LIKE)
        like = f"%{term}%"
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR tags LIKE ?",
            (like, like, like),
        )
        rows = cur.fetchall()
        conn.close()
        return [Book.from_row(r) for r in rows]


class UserRepo:
    @staticmethod
    def add(username: str, password_plain: str, role: str = "user") -> int:
        pw_hash = hash_password(password_plain)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, pw_hash, role),
        )
        conn.commit()
        uid = cur.lastrowid
        conn.close()
        return uid

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        return User.from_row(row)

    @staticmethod
    def verify_credentials(username: str, password_plain: str) -> bool:
        user = UserRepo.get_by_username(username)
        if user is None:
            return False
        return verify_password(user.password_hash, password_plain)


class TransactionRepo:
    @staticmethod
    def add(user_id: int, book_id: int, action: str) -> int:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions (user_id, book_id, action) VALUES (?, ?, ?)",
            (user_id, book_id, action),
        )
        conn.commit()
        tid = cur.lastrowid
        conn.close()
        return tid

    @staticmethod
    def list_for_user(user_id: int):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", (user_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return [
            Transaction(
                id=r["id"],
                user_id=r["user_id"],
                book_id=r["book_id"],
                action=r["action"],
                timestamp=r["timestamp"],
            )
            for r in rows
        ]

    @staticmethod
    def list_all():
        """Return all transactions as sqlite3.Row list (no model mapping)."""
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions")
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete(transaction_id: int) -> bool:
        """Delete transaction by id. Return True if deleted."""
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        ok = cur.rowcount > 0
        conn.close()
        return ok
