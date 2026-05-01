import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.user import User, UserRole


class TestUser(unittest.TestCase):

    def test_create_user(self):
        user = User(1, "testuser", "TestPass1!", UserRole.CLIENT)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, UserRole.CLIENT)

    def test_password_hashing_creates_hash(self):
        user = User(1, "user1", "TestPass1!")
        self.assertIsNotNone(user._password_hash)
        self.assertNotEqual(user._password_hash, "TestPass1!")
        self.assertEqual(len(user._password_hash), 64)

    def test_check_password_correct(self):
        user = User(1, "testuser", "TestPass1!")
        self.assertTrue(user.check_password("TestPass1!"))

    def test_check_password_incorrect(self):
        user = User(1, "testuser", "TestPass1!")
        self.assertFalse(user.check_password("WrongPass1!"))

    def test_validate_password_valid(self):
        user = User(1, "testuser", "TempPass1!")
        self.assertTrue(user.validate_password("TestPass1!"))

    def test_validate_password_short(self):
        user = User(1, "testuser", "TempPass1!")
        self.assertFalse(user.validate_password("shrt"))

    def test_validate_password_no_uppercase(self):
        user = User(1, "testuser", "TempPass1!")
        self.assertFalse(user.validate_password("testpass1!"))

    def test_validate_password_no_digit(self):
        user = User(1, "testuser", "TempPass1!")
        self.assertFalse(user.validate_password("TestPass!"))

    def test_validate_password_no_special(self):
        user = User(1, "testuser", "TempPass1!")
        self.assertFalse(user.validate_password("TestPass1"))

    def test_change_password_success(self):
        user = User(1, "testuser", "OldPass1!")
        result = user.change_password("OldPass1!", "NewPass1!")
        self.assertTrue(result)
        self.assertTrue(user.check_password("NewPass1!"))

    def test_change_password_wrong_old(self):
        user = User(1, "testuser", "OldPass1!")
        result = user.change_password("WrongOld1!", "NewPass1!")
        self.assertFalse(result)

    def test_change_role(self):
        user = User(1, "testuser", "TestPass1!", UserRole.CLIENT)
        user.change_role(UserRole.OPERATOR)
        self.assertEqual(user.role, UserRole.OPERATOR)


if __name__ == '__main__':
    unittest.main()