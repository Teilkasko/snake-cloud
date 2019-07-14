from operator import methodcaller
import snake

class Arena:

    def __init__(self, referenceTimestamp):
        self.timestamp = referenceTimestamp
        self.snakes = []
        self.points = []
        self.obstacles = []

    def addUser (self, id, username):
        s = snake.Snake(id, username)
        self.snakes.append(s)

    def update(self, referenceTimestamp):
        print("updating arena")
        self.timestamp = referenceTimestamp

    def toJSON(self):
        return {
            'timestamp': self.timestamp,
            'snakes': list(map(methodcaller('toJSON'), self.snakes)),
            'points': self.points,
            'obstacles': self.obstacles
        }