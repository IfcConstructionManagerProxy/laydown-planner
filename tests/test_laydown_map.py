import unittest
import sys
import os
import tempfile

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ezdxf
from shapely.geometry import Polygon
from src.laydown_map import LaydownMap


def make_temp_dxf(points, layer="0"):
    """Create a temporary DXF file with a single LWPOLYLINE and return its path."""
    doc = ezdxf.new()
    msp = doc.modelspace()
    polyline = msp.add_lwpolyline(points)
    polyline.dxf.layer = layer
    with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as f:
        path = f.name
    doc.saveas(path)
    return path


class TestLaydownMap(unittest.TestCase):

    def setUp(self):
        self._temp_files = []

    def tearDown(self):
        for path in self._temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _make_dxf(self, points, layer="0"):
        path = make_temp_dxf(points, layer)
        self._temp_files.append(path)
        return path

    # Pentagon points for a simple closed polygon
    PENTAGON = [(0, 0), (4, 0), (5, 3), (2, 5), (-1, 3)]

    def test_parse_dxf_returns_polygons(self):
        path = self._make_dxf(self.PENTAGON)
        lm = LaydownMap(path)
        self.assertEqual(len(lm.zones), 1)
        zone = list(lm.zones.values())[0]
        self.assertIsInstance(zone, Polygon)

    def test_parse_dxf_uses_layer_name(self):
        path = self._make_dxf(self.PENTAGON, layer="LAYDOWN-NORTH")
        lm = LaydownMap(path)
        self.assertIn("LAYDOWN-NORTH", lm.zones)

    def test_parse_dxf_skips_short_polylines(self):
        # Only 2 points — should not produce a zone
        path = self._make_dxf([(0, 0), (1, 1)])
        lm = LaydownMap(path)
        self.assertEqual(len(lm.zones), 0)

    def test_parse_dxf_bad_file_returns_empty(self):
        lm = LaydownMap("/nonexistent/path/to/file.dxf")
        self.assertEqual(lm.zones, {})

    def test_add_zone(self):
        path = self._make_dxf(self.PENTAGON)
        lm = LaydownMap(path)
        poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
        lm.add_zone("test", poly)
        self.assertIn("test", lm.zones)
        self.assertIsInstance(lm.zones["test"], Polygon)

    def test_remove_zone(self):
        path = self._make_dxf(self.PENTAGON)
        lm = LaydownMap(path)
        poly = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
        lm.add_zone("test", poly)
        lm.remove_zone("test")
        self.assertNotIn("test", lm.zones)

    def test_get_zone_area(self):
        path = self._make_dxf(self.PENTAGON)
        lm = LaydownMap(path)
        square = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
        lm.add_zone("square", square)
        self.assertAlmostEqual(lm.get_zone_area("square"), 100.0, places=6)

    def test_get_zone_area_missing(self):
        path = self._make_dxf(self.PENTAGON)
        lm = LaydownMap(path)
        self.assertEqual(lm.get_zone_area("does_not_exist"), 0.0)


if __name__ == '__main__':
    unittest.main()
