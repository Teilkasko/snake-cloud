import unittest
import math
import snake
from functools import partial
import operator

TOLLERANCE = 1e-5

class TestSnake(unittest.TestCase):

    # def test_coordinate(self):
    #     I = coordinate((2, 3), (38, 17, 30))
    #     self.assertEqual(I, (3, 2, 5))
    #     II = coordinate((2, 3), (70, 61, 50))
    #     self.assertEqual(II, (6, 5, 3))
    #     III = coordinate((4, 1), (38, 29, 30))
    #     self.assertEqual(III, (3, 2, 5))
    #     VI = coordinate((1, 1), (43, 50, 38))
    #     self.assertEqual(VI, (3, 5, -3))
    #
    #
    # def test_soundspeed(self):
    #     cI = sound_speed(20, 101000, 50)
    #     self.assertEqual(cI, 343.99)

    def compareValues (self, a, b):
        return math.isclose(a, b, rel_tol=TOLLERANCE)

    def comparePoint(self, a, b):
        return self.compareValues(a[snake.X], b[snake.X]) and self.compareValues(a[snake.Y], b[snake.Y])

    def comparePoints(self, a, b):
        return all(map(lambda x: self.comparePoint(x[0], x[1]), zip(a, b)))

    def test_move(self):
        s = snake.Snake(0, 'snake', [(-2, 0), (0, 0)], 0, 10)
        s.move(1)
        self.assertEqual((10,0), s.head())
        self.assertEqual((8,0), s.tail())

    def test_move_1(self):
        s = snake.Snake(0, 'snake', [(0, 0), (1, 0), (1, 1), (0, 1)], 90, 1)
        s.move(1)
        self.comparePoints([(1, 0), (1, 1), (0, 1), (0, 2)], s.points)


if __name__ == '__main__':
    unittest.main()