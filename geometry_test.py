import unittest
import geometry
import math

EPSILON = 1e-4

class CartesianTest(unittest.TestCase):
    def test_add(self):
        p = geometry.Cartesian(5.0, 3.0)
        p2 = geometry.Cartesian(10, -5)
        p3 = p.add(p2)
        self.assertEqual(p3.get_x(), 5 + 10)
        self.assertEqual(p3.get_y(), 3 + (-5))

    def test_length(self):
        p = geometry.Cartesian(1.0, 0.0)
        self.assertEqual(p.get_length(), 1.0)

    def test_length2(self):
        p = geometry.Cartesian(1.0, 1.0)
        self.assertTrue(p.get_length() - math.sqrt(2.0) < EPSILON)


class PolarTest(unittest.TestCase):
    def test_length(self):
        v = geometry.Polar(35.3, 15.7)
        self.assertEqual(v.get_length(), 35.3)

    def test_omega(self):
        v = geometry.Polar(35.3, 15.7)
        self.assertEqual(v.get_omega(), 15.7)

    def test_to_cartesian1(self):
        v = geometry.Polar(1.0, math.pi/2)
        pt = v.to_cartesian()
        self.assertTrue(pt.get_y() - 1.0 < EPSILON)
        self.assertTrue(pt.get_x() - 0.0 < EPSILON)

    def test_to_cartesian2(self):
        v = geometry.Polar(1.0, math.pi/4)
        pt = v.to_cartesian()
        c = math.sqrt(0.5)
        self.assertTrue(pt.get_y() - c < EPSILON)
        self.assertTrue(pt.get_x() - c < EPSILON)

    def test_to_cartesian3(self):
        v = geometry.Polar(1.0, -math.pi/2)
        pt = v.to_cartesian()
        self.assertTrue(pt.get_y() - (- 1.0) < EPSILON)
        self.assertTrue(pt.get_x() - 0.0 < EPSILON)

    def test_scale(self):
        v = geometry.Polar(1.0, math.pi/4)
        v.scale(3.73)
        self.assertEqual(v.get_length(), 3.73)
        self.assertEqual(v.get_omega(), math.pi/4)

    def test_copy(self):
        v = geometry.Polar(1.0, math.pi/4)
        v2 = v.copy()
        self.assertEqual(v.get_length(), v2.get_length())
        self.assertEqual(v.get_omega(), v2.get_omega())

    def test_add(self):
        v = geometry.Polar(1.0, math.pi/4)
        v2 = v.copy()
        v3 = v.add(v2)
        self.assertEqual(v3.get_length(), 2.0)
        self.assertEqual(v3.get_omega(), math.pi/4)

    def test_add2(self):
        v = geometry.Polar(1.0, math.pi/4)
        v2 = geometry.Polar(1.0, -math.pi/4)
        v3 = v.add(v2)
        c = 2 * math.sqrt(0.5)
        self.assertTrue(v3.get_length() - c < EPSILON)
        self.assertTrue(v3.get_omega() - 0.0 < EPSILON)

    def test_scale2(self):
        v = geometry.Polar(3.73, math.pi/4)
        v.scale(1 / 3.73)
        self.assertTrue(v.get_length() - 1.0 < EPSILON)
        self.assertEqual(v.get_omega(), math.pi/4)
