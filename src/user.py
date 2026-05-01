import hashlib
import re
from enum import Enum


class UserRole(Enum):
    CLIENT = "client"
    OPERATOR = "operator"
    ADMIN = "admin"


class User:

    def __init__(self, user_id: int, username: str, password: str,
                 role: UserRole = UserRole.CLIENT):
        self.id = user_id
        self.username = username
        self._password_hash = self._hash_password(password)
        self.role = role

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password: str) -> bool:
        return self._password_hash == self._hash_password(password)

    def validate_password(self, password: str) -> bool:
        if len(password) < 6:
            return False
        if not re.search(r'[A-ZА-Я]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*]', password):
            return False
        return True

    def change_password(self, old_password: str, new_password: str) -> bool:
        if not self.check_password(old_password):
            return False
        if not self.validate_password(new_password):
            return False
        self._password_hash = self._hash_password(new_password)
        return True

    def change_role(self, new_role: UserRole) -> bool:
        self.role = new_role
        return True

    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}', role={self.role.value})"