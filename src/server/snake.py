import math

def segmentLength(a, b):
    return math.sqrt(
        math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2)
    )

X = 0
Y = 1

class Snake:


    def __init__(self, id, username, points, direction, speed):
        self.id = id
        self.username = username
        self.direction = direction
        self.speed = speed
        self.points = points


    def head (self):
        return self.points[-1]

    def tail (self):
        return self.points[0]

    def tailLength (self):
        return segmentLength(self.points[0], self.points[1])

    def move(self, elapsedTime):
        lengthToMove = self.speed * elapsedTime
        h = self.head()
        self.points.append((
            h[X] + (lengthToMove * math.cos(math.radians(self.direction))),
            h[Y] + (lengthToMove * math.sin(math.radians(self.direction)))
        ))
        while (self.tailLength() <= lengthToMove):
            lengthToMove = lengthToMove - segmentLength(self.points[0], self.points[1])
            self.points.pop(0)
        ratio = lengthToMove / self.tailLength()
        self.points[0] = (
            self.points[0][X] + ratio * (self.points[1][X] - self.points[0][X]),
            self.points[0][Y] + ratio * (self.points[1][Y] - self.points[0][Y])
        )

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'direction': self.direction,
            'head': self.head(),
            'points': self.points,
            'end': 0
        }

