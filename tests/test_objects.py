import unittest
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shapely.geometry import Polygon
from src.objects import Object, Stack


class TestObject(unittest.TestCase):

    def test_object_creation(self):
        obj = Object("Pipe", 500, (3.0, 1.5, 1.0))
        self.assertEqual(obj.name, "Pipe")
        self.assertEqual(obj.weight, 500)
        self.assertEqual(obj.dimensions, (3.0, 1.5, 1.0))

    def test_get_footprint_default(self):
        obj = Object("Box", 100, (4.0, 2.0, 1.0))
        fp = obj.get_footprint()
        self.assertAlmostEqual(fp.area, 4.0 * 2.0, places=6)

    def test_get_footprint_positioned(self):
        obj = Object("Crate", 200, (5.0, 3.0, 2.0))
        fp = obj.get_footprint(x=5.0, y=3.0)
        minx, miny, maxx, maxy = fp.bounds
        self.assertGreaterEqual(minx, 5.0 - 1e-9)
        self.assertGreaterEqual(miny, 3.0 - 1e-9)

    def test_get_footprint_rotated_90(self):
        obj = Object("Beam", 300, (10.0, 2.0, 1.0))
        fp = obj.get_footprint(rotation=90)
        minx, miny, maxx, maxy = fp.bounds
        effective_width = maxx - minx
        effective_height = maxy - miny
        # After 90° rotation the long dimension should be along y-axis
        self.assertAlmostEqual(effective_width, 2.0, delta=0.01)
        self.assertAlmostEqual(effective_height, 10.0, delta=0.01)

    def test_get_footprint_returns_polygon(self):
        obj = Object("Tank", 1000, (6.0, 4.0, 3.0))
        fp = obj.get_footprint()
        self.assertIsInstance(fp, Polygon)


class TestStack(unittest.TestCase):

    def test_stack_add(self):
        stack = Stack()
        obj1 = Object("A", 100, (1.0, 1.0, 1.0))
        obj2 = Object("B", 250, (1.0, 1.0, 1.0))
        stack.add(obj1)
        stack.add(obj2)
        self.assertEqual(stack.total_weight, 350)

    def test_stack_can_stack(self):
        stack = Stack()
        obj = Object("C", 50, (1.0, 1.0, 1.0))
        self.assertTrue(stack.can_stack(obj))

    def test_stack_raises_on_invalid(self):
        class NoStackStack(Stack):
            def can_stack(self, obj):
                return False

        stack = NoStackStack()
        obj = Object("D", 75, (1.0, 1.0, 1.0))
        with self.assertRaises(ValueError):
            stack.stack(obj)


if __name__ == '__main__':
    unittest.main()