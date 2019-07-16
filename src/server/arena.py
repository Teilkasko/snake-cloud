from operator import methodcaller
import snake

class Arena:

    def __init__(self, referenceTimestamp):
        self.timestamp = referenceTimestamp
        self.snakes = []
        self.points = []
        self.obstacles = []

    def createNewSnake(self, id, username):
        position = (0, 0)
        length = 50
        direction = 0
        speed = 10

        newSnake = snake.Snake(id, username, position, length, direction, speed)
        return newSnake

    def addUser (self, id, username):
        self.snakes.append(self.createNewSnake(id, username))

    def update(self, newTimestamp):
        elapsedTime = newTimestamp - self.timestamp
        for s in self.snakes:
            s.move(elapsedTime)
        # map(methodcaller('move', elapsedTime), self.snakes)
        self.timestamp = newTimestamp

    def changeSnakeDirection(self, id, direction, newTimestamp):
        pass

    def toJSON(self):
        return {
            'timestamp': self.timestamp,
            'snakes': list(map(methodcaller('toJSON'), self.snakes)),
            'points': self.points,
            'obstacles': self.obstacles
        }