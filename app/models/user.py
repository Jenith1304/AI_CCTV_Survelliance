class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password = password_hash

    def to_dict(self):
        return {"username": self.username, "password": self.password}