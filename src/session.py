# src/session.py
"""
Session manager in-memory sederhana.
Menyimpan hanya 1 session aktif (cukup untuk aplikasi desktop sederhana).
Jika ingin multi-session / token, bisa dikembangkan.
"""

from typing import Optional


class SessionManager:
    def __init__(self):
        self._current_user_id: Optional[int] = None
        self._current_username: Optional[str] = None

    def login(self, user_id: int, username: str) -> None:
        self._current_user_id = user_id
        self._current_username = username

    def logout(self) -> None:
        self._current_user_id = None
        self._current_username = None

    def is_authenticated(self) -> bool:
        return self._current_user_id is not None

    def get_user_id(self) -> Optional[int]:
        return self._current_user_id

    def get_username(self) -> Optional[str]:
        return self._current_username


# singleton instance
session_manager = SessionManager()
