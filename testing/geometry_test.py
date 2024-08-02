import math
import src.geometry as geo 
import unittest as ut


class TestGeometry(ut.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_distance(self):
        pos1 = (0, 1)
        pos2 = (1, 0)
        dist = geo.distance(pos1, pos2)
        self.assertAlmostEqual(dist, math.sqrt(2))

    def test_rotate1(self):
        pt = (1, 0)
        rotate = geo.rotate(pt, math.pi / 2)
        self.assertAlmostEqual(rotate[0], 0)
        self.assertAlmostEqual(rotate[1], 1)

    def test_rotate2(self):
        pt = (0, 2)
        rotate = geo.rotate(pt, math.pi / 2, (0, 1))
        self.assertAlmostEqual(rotate[0], -1)
        self.assertAlmostEqual(rotate[1], 1)

    def test_rotate3(self):
        pt = (1, 1)
        rotate = geo.rotate(pt, math.pi / 4)
        self.assertAlmostEqual(rotate[0], 0)
        self.assertAlmostEqual(rotate[1], math.sqrt(2))

if __name__ == "__main__":
    ut.main()