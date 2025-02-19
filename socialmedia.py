
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.following = set()
        self.messages = []  # Messages sent to this user

    def follow(self, other_user):
        self.following.add(other_user.username)

    def send_message(self, to_user, message):
        if to_user.username in self.following and self.username in to_user.following:
            to_user.messages.append((self.username, message))
            return True
        return False


class SocialNetwork:
    def __init__(self):
        self.users = {}

    def signup(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            return True
        return False

    def login(self, username, password):
        return username in self.users and self.users[username].password == password

    def search_user(self, username):
        return username if username in self.users else None

    def follow_user(self, current_user, other_username):
        other_user = self.users.get(other_username)
        if other_user:
            current_user.follow(other_user)
            return True
        return False

    def get_mutual_connections(self, current_user):
        mutuals = [user for user in current_user.following if current_user.username in self.users[user].following]
        return mutuals

    def display_unread_messages(self, current_user):
        return current_user.messages


# Example usage
social_network = SocialNetwork()
social_network.signup("alice", "password123")
social_network.signup("bob", "password123")

# Logging in and performing actions
if social_network.login("alice", "password123"):
    alice = social_network.users["alice"]
    social_network.follow_user(alice, "bob")  # Alice follows Bob
    if social_network.login("bob", "password123"):
        bob = social_network.users["bob"]
        social_network.follow_user(bob, "alice")  # Bob follows Alice

        # Send message between mutual connections
        alice.send_message(bob, "Hello Bob!")
        print(bob.messages)  # [('alice', 'Hello Bob!')]

    alice_unread = social_network.display_unread_messages(alice)
    print(alice_unread)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.following = set()
        self.messages = []

    def follow(self, user):
        self.following.add(user)

    def can_message(self, user):
        return user in self.following and self in user.following

class Graph:
    def __init__(self):
        self.connections = []  # list of tuples (source, destination)

    def add_connection(self, source, destination):
        self.connections.append((source, destination))

    def get_mutual_connections(self, user):
        mutual_connections = []
        for source, destination in self.connections:
            if (destination, source) in self.connections:
                if source == user or destination == user:
                    mutual_connections.append((source, destination))
        return [u for u, v in mutual_connections if u == user] + [v for u, v in mutual_connections if v == user]

class Message:
    def __init__(self, sender, receiver, content):
        if sender.can_message(receiver):
            self.sender = sender
            self.receiver = receiver
            self.content = content
            receiver.messages.append(self)
        else:
            raise PermissionError("Users cannot message each other unless they are mutual followers.")

class SocialMediaApp:
    def __init__(self):
        self.users = {}
        self.graph = Graph()

    def sign_up(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            return self.users[username]
        else:
            raise Exception("Username already exists")

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            raise Exception("Invalid username or password")

    def follow(self, follower_username, followee_username):
        if follower_username in self.users and followee_username in self.users:
            follower = self.users[follower_username]
            followee = self.users[followee_username]
            follower.follow(followee)
            self.graph.add_connection(follower, followee)

    def send_message(self, sender_username, receiver_username, content):
        if sender_username in self.users and receiver_username in self.users:
            sender = self.users[sender_username]
            receiver = self.users[receiver_username]
            msg = Message(sender, receiver, content)
            return msg

    def get_unread_messages(self, username):
        user = self.users.get(username)
        if user:
            unread_messages = [msg.content for msg in user.messages]
            user.messages = []  # Mark all messages as read
            return unread_messages

    def get_mutual_friends(self, username):
        user = self.users.get(username)
        if user:
            return self.graph.get_mutual_connections(user)

# Example usage
app = SocialMediaApp()
alice = app.sign_up('alice', 'password123')
bob = app.sign_up('bob', 'password456')
app.follow('alice', 'bob')
app.follow('bob', 'alice')
message = app.send_message('alice', 'bob', 'Hello Bob!')

# Get unread messages for Bob
unread_messages_bob = app.get_unread_messages('bob')
print(unread_messages_bob)

# Get mutual friends for Alice
mutual_friends_alice = app.get_mutual_friends('alice')
print(mutual_friends_alice)

# Import necessary libraries
import json

# Define User class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.followers = set()     # Users that follow this user
        self.following = set()     # Users that this user follows
        self.messages = []         # Messages sent to this user

    def follow(self, other_user):
        self.following.add(other_user)
        other_user.followers.add(self)

    def send_message(self, to_user, message):
        if self in to_user.followers and to_user in self.followers:  # Check mutual connection
            to_user.messages.append((self.username, message))
            return True
        return False

    def unread_messages(self):
        unread_msgs = self.messages[:]
        self.messages.clear()  # Clear messages after displaying
        return unread_msgs

# Define Graph class
class Graph:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            return True
        return False

    def find_mutual_connections(self, username):
        user = self.users.get(username)
        if user:
            mutuals = user.followers.intersection(user.following)
            return [u.username for u in mutuals]
        return []

    def get_user(self, username):
        return self.users.get(username)

# Example function showing usage of Graph

def run_example_app():
    graph = Graph()
    graph.add_user('alice', 'alice_pass')
    graph.add_user('bob', 'bob_pass')
    graph.add_user('charlie', 'charlie_pass')

    alice = graph.get_user('alice')
    bob = graph.get_user('bob')
    charlie = graph.get_user('charlie')

    alice.follow(bob)   # Alice follows Bob
    bob.follow(alice)   # Bob follows Alice

    # Sending message
    alice.send_message(bob, "Hello Bob!")
    print(bob.unread_messages())  # Bob reads

    # Finding mutual connections
    print(graph.find_mutual_connections('alice'))  # ['bob']

run_example_app()

# Saving as Python script
with open('/mnt/data/social_media_app.py', 'w') as file:
    file.write(run_example_app.__code__.co_consts[0])