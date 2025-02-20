
from users import User, load_users, save_users

class SocialMediaApp:
    def __init__(self, user_file='users.json'):
        self.user_file = user_file
        self.users = load_users(self.user_file)

    def sign_up(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            self.save_data()
            return self.users[username]
        else:
            raise Exception("Username already exists")

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        else:
            raise Exception("Invalid username or password")

    def follow(self, follower_name, followee_name):
        follower = self.users.get(follower_name)
        followee = self.users.get(followee_name)
        if follower and followee:
            follower.follow(followee)
            self.save_data()

    def send_message(self, sender_name, receiver_name, content):
        sender = self.users.get(sender_name)
        receiver = self.users.get(receiver_name)
        if sender and receiver and sender.send_message(receiver, content):
            self.save_data()
        else:
            raise Exception("Message sending failed (mutual follow required)")

    def save_data(self):
        save_users(self.users, self.user_file)

# Example usage
if __name__ == "__main__":
    app = SocialMediaApp()
    alice = app.sign_up('alice', 'password123')
    bob = app.sign_up('bob', 'password456')
   
    app.follow('alice', 'bob')
    app.follow('bob', 'alice')
   
    try:
        app.send_message('alice', 'bob', 'Hello Bob!')
    except Exception as e:
        print(e)

    # Display messages
    print(bob.unread_messages())

    # Save final data
    app.save_data()

