import json
import os
import tempfile
import unittest
import sys

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import DataLoader
from src.laydown_map import LaydownMap


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        """Set up test variables and initialize DataLoader."""
        self.data_loader = DataLoader('../data')

    def test_load_data(self):
        """Test loading data."""
        # Add your test implementation here
        pass

    def test_process_data(self):
        """Test processing loaded data."""
        # Add your test implementation here
        pass

    def tearDown(self):
        """Clean up after tests."""
        self.data_loader = None


def _make_temp_geojson(features):
    geojson = {"type": "FeatureCollection", "features": features}
    with tempfile.NamedTemporaryFile(mode='w', suffix=".geojson", delete=False) as f:
        json.dump(geojson, f)
        return f.name


_POLYGON_FEATURE = {
    "type": "Feature",
    "properties": {"name": "TEST-ZONE"},
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]
    }
}


class TestDataLoaderGeoJSON(unittest.TestCase):

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for path in self.temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _make(self, features):
        path = _make_temp_geojson(features)
        self.temp_files.append(path)
        return path

    def test_load_geojson_laydown_data_returns_laydown_map(self):
        path = self._make([_POLYGON_FEATURE])
        result = DataLoader().load_geojson_laydown_data(path)
        self.assertIsInstance(result, LaydownMap)

    def test_load_geojson_laydown_data_zones_populated(self):
        path = self._make([_POLYGON_FEATURE])
        result = DataLoader().load_geojson_laydown_data(path)
        self.assertGreater(len(result.get_zones()), 0)

    def test_load_geojson_laydown_data_bad_file(self):
        result = DataLoader().load_geojson_laydown_data("/nonexistent/path/file.geojson")
        self.assertIsInstance(result, LaydownMap)
        self.assertEqual(len(result.get_zones()), 0)


if __name__ == '__main__':
    unittest.main()