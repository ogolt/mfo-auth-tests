import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth_service import AuthenticationService
from src.user import UserRole


class TestAuthenticationService(unittest.TestCase):

    def setUp(self):
        self.service = AuthenticationService()

    def test_register_user_success(self):
        user = self.service.register_user("testuser", "TestPass1!", UserRole.CLIENT)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")

    def test_register_duplicate_username(self):
        self.service.register_user("testuser", "TestPass1!", UserRole.CLIENT)
        user = self.service.register_user("testuser", "TestPass1!", UserRole.CLIENT)
        self.assertIsNone(user)

    def test_login_success(self):
        self.service.register_user("testuser", "TestPass1!", UserRole.CLIENT)
        token = self.service.login("testuser", "TestPass1!")
        self.assertIsNotNone(token)

    def test_login_wrong_password(self):
        self.service.register_user("testuser", "TestPass1!", UserRole.CLIENT)
        token = self.service.login("testuser", "WrongPass1!")
        self.assertIsNone(token)

    def test_login_nonexistent_user(self):
        token = self.service.login("nouser", "TestPass1!")
        self.assertIsNone(token)

    def test_change_role_by_admin(self):
        self.service.register_user("admin", "AdminPass1!", UserRole.ADMIN)
        self.service.register_user("client", "ClientPass1!", UserRole.CLIENT)
        token = self.service.login("admin", "AdminPass1!")
        result = self.service.change_user_role(token, 2, UserRole.OPERATOR)
        self.assertTrue(result)
        user = self.service.get_user_by_id(2)
        self.assertEqual(user.role, UserRole.OPERATOR)

    def test_change_role_by_non_admin(self):
        self.service.register_user("client1", "ClientPass1!", UserRole.CLIENT)
        self.service.register_user("client2", "Client2Pass1!", UserRole.CLIENT)
        token = self.service.login("client1", "ClientPass1!")
        result = self.service.change_user_role(token, 2, UserRole.OPERATOR)
        self.assertFalse(result)

    def test_is_password_strong_true(self):
        self.assertTrue(self.service.is_password_strong("StrongPass1"))

    def test_is_password_strong_short(self):
        self.assertFalse(self.service.is_password_strong("short"))

    def test_is_password_strong_no_digit(self):
        self.assertFalse(self.service.is_password_strong("NoDigitPass"))

    def test_is_password_strong_none(self):
        self.assertFalse(self.service.is_password_strong(None))


if __name__ == '__main__':
    unittest.main()