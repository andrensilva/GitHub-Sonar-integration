"""
user_manager.py - Basic user management module (dummy file for SonarQube analysis)
"""

# CODE SMELL: unused imports
import hashlib
import json
import sys


# SECURITY HOTSPOT: sensitive data stored in a plain dict (in-memory, no hashing)
USERS_DB = {
    "admin": "admin123",      # SECURITY: plain-text password
    "john":  "password1",
    "jane":  "qwerty",
}


class UserManager:
    def __init__(self):
        # CODE SMELL: mutable default would be dangerous; here it's fine but
        # the class doesn't encapsulate properly
        self.users = USERS_DB

    def create_user(self, username, password):
        # BUG: no validation on username or password strength
        if username in self.users:
            print("User already exists")  # CODE SMELL: should use logging
            return False
        self.users[username] = password  # SECURITY: storing plain-text password
        return True

    def authenticate(self, username, password):
        # SECURITY HOTSPOT: timing attack possible (direct string comparison)
        if username in self.users:
            return self.users[username] == password
        return False

    def delete_user(self, username):
        # BUG: no authentication check before deleting
        if username in self.users:
            del self.users[username]

    def list_users(self):
        # SECURITY: exposes all usernames AND passwords
        return self.users

    def update_password(self, username, old_password, new_password):
        # CODE SMELL: deeply nested logic
        if username in self.users:
            if self.users[username] == old_password:
                if len(new_password) > 0:   # CODE SMELL: use truthiness check
                    self.users[username] = new_password
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


def reset_all_users():
    # SECURITY HOTSPOT: destructive operation with no auth or confirmation
    USERS_DB.clear()


# CODE SMELL: script-level code not guarded by if __name__ == "__main__"
manager = UserManager()
manager.create_user("test_user", "test123")