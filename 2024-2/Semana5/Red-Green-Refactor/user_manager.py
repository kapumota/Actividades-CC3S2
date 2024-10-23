""""
class UserAlreadyExistsError(Exception):
    pass

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        if username in self.users:
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        self.users[username] = password
    
    def user_exists(self, username):
        return username in self.users 
"""
import hashlib

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password
    
    def authenticate_user(self, username, password):
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        hashed_password = self._hash_password(password)
        return self.users[username] == hashed_password
    
    def user_exists(self, username):
        return username in self.users
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
