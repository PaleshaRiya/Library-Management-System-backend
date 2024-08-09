class User:
    def __init__(self, id, name, username, email, active, password, role, currentBooks=None):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.active = active
        self.password = password
        self.role = role
        self.currentBooks = currentBooks

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'role': self.role,
            'currentBooks': self.currentBooks
        }
