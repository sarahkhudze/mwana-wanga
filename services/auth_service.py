import json
import os
from hashlib import sha256
from pathlib import Path



class AuthService:
    def __init__(self):
        self.users_file = Path(__file__).parent / "users.json"  # Fixes Windows path issues

    def _ensure_data_dir(self):
        os.makedirs(Path(self.users_file).parent, exist_ok=True)

    def register_user(self, username, password, email):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}

        if username in users:
            return False, "Username already exists"

        hashed_password = sha256(password.encode()).hexdigest()
        users[username] = {
            'password': hashed_password,
            'email': email,
            'pregnancy_data': {}
        }

        with open(self.users_file, 'w') as f:
            json.dump(users, f)

        return True, "Registration successful"

    def login_user(self, username, password):
        if not os.path.exists(self.users_file):
            return False, "User not found"

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username not in users:
            return False, "User not found"

        hashed_password = sha256(password.encode()).hexdigest()
        if users[username]['password'] != hashed_password:
            return False, "Incorrect password"

        self.current_user = username
        return True, "Login successful"

    def get_current_user(self):
        return self.current_user

    def save_pregnancy_data(self, lmp_date, due_date, current_week):
        if not self.current_user:
            return False

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        users[self.current_user]['pregnancy_data'] = {
            'lmp_date': lmp_date.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'current_week': current_week
        }

        with open(self.users_file, 'w') as f:
            json.dump(users, f)

        return True