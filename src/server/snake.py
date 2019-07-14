import math

class Snake:

    def __init__(self, id, username, position, length, direction, speed):
        self.id = id
        self.username = username
        self.position = position
        self.direction = direction
        self.speed = speed
        self.points = [(
            - length * math.cos(math.radians(direction)),
            - length * math.sin(math.radians(direction))
        )]

    def move(self, elapsedTime):
        pass

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'direction': self.direction,
            'position': self.position,
            'points': self.points,
            'end': 0
        }

