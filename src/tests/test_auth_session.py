# src/tests/test_auth_session.py
import unittest
from services.user_service import register_user, login_user, UserExistsError, AuthError
from session import session_manager

class TestAuthSession(unittest.TestCase):
    def test_register_and_login(self):
        # create a unique user for test
        uname = "test_auto"
        try:
            u = register_user(uname, "pw123")
        except UserExistsError:
            # already exists, ignore
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
