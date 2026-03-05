import unittest
import sys
import os
import tempfile

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib
matplotlib.use('Agg')

import ezdxf
from src.data_loader import DataLoader
from src.objects import Object
from src.placement_optimizer import PlacementOptimizer
from src.visualization import plot_laydown_zone


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


# A simple 100×100 square encoded as a polyline
SQUARE_100 = [(0, 0), (100, 0), (100, 100), (0, 100)]


class TestPolygonPipeline(unittest.TestCase):

    def setUp(self):
        self._temp_files = []

    def tearDown(self):
        for path in self._temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _make_dxf(self, points=None, layer="LAYDOWN-ZONE"):
        path = make_temp_dxf(points or SQUARE_100, layer)
        self._temp_files.append(path)
        return path

    def _make_objects(self, n=3, length=5.0, width=3.0):
        return [Object(f"Item{i}", 100 * (i + 1), (length, width, 1.0)) for i in range(n)]

    def test_full_pipeline_dxf_to_placements(self):
        dxf_path = self._make_dxf()
        loader = DataLoader()
        lm = loader.load_dxf_laydown_data(dxf_path)
        zone_name = list(lm.zones.keys())[0]
        zone = lm.zones[zone_name]

        objects = self._make_objects(n=3)
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, unplaced = optimizer.place_objects(zone, objects)

        self.assertGreater(len(placements), 0, "At least one object should be placed")

    def test_full_pipeline_visualization_does_not_raise(self):
        dxf_path = self._make_dxf()
        loader = DataLoader()
        lm = loader.load_dxf_laydown_data(dxf_path)
        zone_name = list(lm.zones.keys())[0]
        zone = lm.zones[zone_name]

        objects = self._make_objects(n=2)
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, _ = optimizer.place_objects(zone, objects)

        try:
            plot_laydown_zone(zone, placements, title="Test Plan")
        except Exception as e:
            self.fail(f"plot_laydown_zone raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()