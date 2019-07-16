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
        deltaX = self.speed * math.cos(math.radians((self.direction))) * elapsedTime
        deltaY = self.speed * math.sin(math.radians((self.direction))) * elapsedTime
        self.position = (self.position[0] + deltaX, self.position[1] + deltaY)
        if (len(self.points) > 1):
            delta = math.sqrt(deltaX ** 2 + deltaY ** 2)
            lastSegment = math.sqrt(
                (self.points[0][0] - self.points[1][0]) ** 2 + (self.points[0][1] - self.points[1][1]) ** 2)
            while (delta > 0 and delta >= lastSegment and len(self.points) > 1):
                if (len(self.points) >= 1):
                    self.points.remove(self.points[0])
                delta = delta - lastSegment
                if (len(self.points) > 1):
                    lastSegment = math.sqrt(
                        (self.points[0][0] - self.points[1][0]) ** 2 + (self.points[0][1] - self.points[1][1]) ** 2)
            if (delta > 0 and delta < lastSegment):
                if (len(self.points) > 1):
                    dir = math.acos((self.points[1][0] - self.points[0][0]) / lastSegment)
                    newX = self.points[1][0] - math.cos(dir) * (lastSegment - delta)
                    newY = self.points[1][1] - math.sin(dir) * (lastSegment - delta)
                    self.points[0] = (newX, newY)
                else:
                    self.points = [(
                        - delta * math.cos(math.radians(self.direction)),
                        - delta * math.sin(math.radians(self.direction))
                    )]
        else:
            self.points[0] = (self.points[0][0] + deltaX, self.points[0][1] + deltaY)

    # first element of the list is the tail of snake
    # degrees increase clockwise
    def changeDirection(self, deltaDirection, elapsedTime):
        self.points.insert(len(self.points), self.position)
        self.direction = self.direction + deltaDirection
        if (self.direction < 0):
            self.direction = 360 + self.direction
        else:
            self.direction = self.direction % 360
        print(self.direction)
        self.move(elapsedTime)

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'direction': self.direction,
            'position': self.position,
            'points': self.points,
            'end': 0
        }

