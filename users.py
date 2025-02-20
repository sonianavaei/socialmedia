
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.followers = set()
        self.following = set()
        self.messages = []

    def follow(self, other_user):
        self.following.add(other_user.username)
        other_user.followers.add(self.username)

    def send_message(self, to_user, message):
        if self.username in to_user.followers and to_user.username in self.followers:
            to_user.messages.append((self.username, message))
            return True
        return False

    def unread_messages(self):
        unread = self.messages[:]
        self.messages.clear()
        return unread

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "followers": list(self.followers),
            "following": list(self.following),
            "messages": self.messages
        }

def load_users(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return {username: User(**info) for username, info in data.items()}
    except FileNotFoundError:
        return {}

def save_users(users, file_path):
    with open(file_path, 'w') as file:
        json.dump({u: user.to_dict() for u, user in users.items()}, file, indent=2)

