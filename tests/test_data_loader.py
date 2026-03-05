import unittest
import sys
import os
import tempfile

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ezdxf
from src.data_loader import DataLoader
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


PENTAGON = [(0, 0), (4, 0), (5, 3), (2, 5), (-1, 3)]


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self._temp_files = []

    def tearDown(self):
        for path in self._temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _make_dxf(self, points=None, layer="0"):
        path = make_temp_dxf(points or PENTAGON, layer)
        self._temp_files.append(path)
        return path

    def test_init_with_data_dir(self):
        loader = DataLoader('../data')
        self.assertEqual(loader.data_dir, '../data')

    def test_init_without_data_dir(self):
        loader = DataLoader()
        self.assertIsNone(loader.data_dir)

    def test_load_dxf_laydown_data_returns_laydown_map(self):
        path = self._make_dxf()
        loader = DataLoader()
        result = loader.load_dxf_laydown_data(path)
        self.assertIsInstance(result, LaydownMap)

    def test_load_dxf_laydown_data_zones_populated(self):
        path = self._make_dxf()
        loader = DataLoader()
        lm = loader.load_dxf_laydown_data(path)
        self.assertGreater(len(lm.zones), 0)

    def test_load_objects_returns_none(self):
        loader = DataLoader()
        result = loader.load_objects("dummy_path")
        self.assertIsNone(result)

    def test_load_schedule_returns_none(self):
        loader = DataLoader()
        result = loader.load_schedule("dummy_path")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()