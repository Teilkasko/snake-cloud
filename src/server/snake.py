class Snake:

    def __init__(self, id, username):
        self.id = id
        self.username = username

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username
        }