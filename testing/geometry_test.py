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