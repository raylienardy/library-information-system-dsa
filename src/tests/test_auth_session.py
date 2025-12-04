# src/tests/test_auth_session.py
import os
import unittest

from persistence.db import DB_PATH, init_db
from services.user_service import AuthError, UserExistsError, login_user, register_user
from session import session_manager


class TestAuthSession(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ensure fresh DB for tests (optional)
        try:
            if DB_PATH.exists():
                os.remove(DB_PATH)
        except Exception:
            pass
        init_db()

    def test_register_and_login(self):
        uname = "test_auto_user"
        # ensure no prior user
        try:
            register_user(uname, "pw123")
        except UserExistsError:
            # if exists, continue
            pass
        user = login_user(uname, "pw123")
        self.assertIsNotNone(user)
        session_manager.login(user.id, user.username)
        self.assertTrue(session_manager.is_authenticated())
        session_manager.logout()
        self.assertFalse(session_manager.is_authenticated())

    def test_login_wrong(self):
        with self.assertRaises(AuthError):
            login_user("nonexistuser_zz", "pw")
