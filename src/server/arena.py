from operator import methodcaller
import math
import random
import snake

class Arena:

    def __init__(self, referenceTimestamp):
        self.width = 400
        self.height = 400
        self.timestamp = referenceTimestamp
        self.snakes = []
        self.points = []
        for i in range(0, 50):
            self.points.append((random.randint(0, self.width), random.randint(0, self.height)))
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
        if (self.__getSnakeById__(id) is None):
            self.snakes.append(self.createNewSnake(id, username))

    def removeUser(self, id):
        s = self.__getSnakeById__(id)
        if (not s is None):
            self.snakes.remove(s)

    def update(self, newTimestamp):
        elapsedTime = newTimestamp - self.timestamp
        for s in self.snakes:
            s.move(elapsedTime)
        # map(methodcaller('move', elapsedTime), self.snakes)
        self.timestamp = newTimestamp

    def changeSnakeDirection(self, id, direction, newTimestamp):
        s = self.__getSnakeById__(id)
        if (not s is None):
            if (direction == 'right'):
                s.direction = s.direction + 10
            elif (direction == 'left'):
                s.direction = s.direction - 10
        self.update(newTimestamp)


    def toJSON(self):
        return {
            'timestamp': self.timestamp,
            'snakes': list(map(methodcaller('toJSON'), self.snakes)),
            'points': self.points,
            'obstacles': self.obstacles
        }

    def __getSnakeById__(self, id):
        for s in self.snakes:
            if (s.id == id):
                return s
        return