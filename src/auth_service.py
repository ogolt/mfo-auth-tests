from typing import Dict, Optional
from src.user import User, UserRole


class AuthenticationService:

    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1
        self._sessions: Dict[str, int] = {}

    def register_user(self, username: str, password: str,
                      role: UserRole = UserRole.CLIENT) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return None
        temp_user = User(0, username, "TempPass1!")
        if not temp_user.validate_password(password):
            return None
        user = User(self._next_id, username, password, role)
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def login(self, username: str, password: str) -> Optional[str]:
        for user in self._users.values():
            if user.username == username and user.check_password(password):
                token = f"token_{user.id}_{hash(username)}"
                self._sessions[token] = user.id
                return token
        return None

    def change_user_role(self, admin_token: str, user_id: int,
                         new_role: UserRole) -> bool:
        admin_id = self._sessions.get(admin_token)
        if not admin_id:
            return False
        admin_user = self._users.get(admin_id)
        if not admin_user or admin_user.role != UserRole.ADMIN:
            return False
        target_user = self._users.get(user_id)
        if not target_user:
            return False
        target_user.change_role(new_role)
        return True

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def get_all_users(self) -> list:
        return list(self._users.values())

    def check_permission(self, token: str, required_role: UserRole) -> bool:
        user_id = self._sessions.get(token)
        if not user_id:
            return False
        user = self._users.get(user_id)
        if not user:
            return False
        roles_order = [UserRole.CLIENT, UserRole.OPERATOR, UserRole.ADMIN]
        return roles_order.index(user.role) >= roles_order.index(required_role)

    def is_password_strong(self, password: str) -> bool:
        if not password:
            return False
        if len(password) < 8:
            return False
        return any(char.isdigit() for char in password)