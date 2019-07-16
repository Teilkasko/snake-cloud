from operator import methodcaller
import math
import snake

class Arena:

    def __init__(self, referenceTimestamp):
        self.timestamp = referenceTimestamp
        self.snakes = []
        self.points = []
        self.obstacles = []

    def createNewSnake(self, id, username):
        length = 50
        direction = 0
        speed = 10

        points = [
            (- length * math.cos(math.radians(direction)), - length * math.sin(math.radians(direction))),
            (0, 0)
        ]

        newSnake = snake.Snake(id, username, points, direction, speed)
        return newSnake

    def addUser (self, id, username):
        self.snakes.append(self.createNewSnake(id, username))

    def update(self, newTimestamp):
        elapsedTime = newTimestamp - self.timestamp
        map(methodcaller('move', elapsedTime), self.snakes)
        self.timestamp = newTimestamp

    def toJSON(self):
        return {
            'timestamp': self.timestamp,
            'snakes': list(map(methodcaller('toJSON'), self.snakes)),
            'points': self.points,
            'obstacles': self.obstacles
        }