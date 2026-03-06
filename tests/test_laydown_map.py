import json
import os
import tempfile
import unittest

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shapely.geometry import Polygon
from src.laydown_map import LaydownMap


def make_temp_geojson(features):
    """Write a GeoJSON FeatureCollection to a temp file and return the path."""
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix=".geojson", delete=False) as f:
        json.dump(geojson, f)
        return f.name


SQUARE_COORDS = [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]

SIMPLE_POLYGON_FEATURE = {
    "type": "Feature",
    "properties": {"name": "TEST-ZONE"},
    "geometry": {
        "type": "Polygon",
        "coordinates": [SQUARE_COORDS]
    }
}


class TestLaydownMapGeoJSON(unittest.TestCase):

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for path in self.temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

    def _make(self, features):
        path = make_temp_geojson(features)
        self.temp_files.append(path)
        return path

    def test_from_geojson_returns_laydown_map(self):
        path = self._make([SIMPLE_POLYGON_FEATURE])
        result = LaydownMap.from_geojson(path)
        self.assertIsInstance(result, LaydownMap)

    def test_from_geojson_zones_populated(self):
        path = self._make([SIMPLE_POLYGON_FEATURE])
        result = LaydownMap.from_geojson(path)
        self.assertGreater(len(result.get_zones()), 0)

    def test_from_geojson_uses_name_property(self):
        feature = {
            "type": "Feature",
            "properties": {"name": "NORTH-COMPOUND"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [SQUARE_COORDS]
            }
        }
        path = self._make([feature])
        result = LaydownMap.from_geojson(path)
        self.assertIn("NORTH-COMPOUND", result.get_zones())

    def test_from_geojson_uses_layer_property_fallback(self):
        feature = {
            "type": "Feature",
            "properties": {"layer": "SOUTH-ZONE"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [SQUARE_COORDS]
            }
        }
        path = self._make([feature])
        result = LaydownMap.from_geojson(path)
        self.assertIn("SOUTH-ZONE", result.get_zones())

    def test_from_geojson_falls_back_to_auto_name(self):
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [SQUARE_COORDS]
            }
        }
        path = self._make([feature])
        result = LaydownMap.from_geojson(path)
        self.assertIn("zone_0", result.get_zones())

    def test_from_geojson_skips_non_polygon(self):
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": [[0, 0], [10, 0], [10, 10]]
            }
        }
        path = self._make([feature])
        result = LaydownMap.from_geojson(path)
        self.assertEqual(len(result.get_zones()), 0)

    def test_from_geojson_skips_null_geometry(self):
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": None
        }
        path = self._make([feature])
        result = LaydownMap.from_geojson(path)
        self.assertEqual(len(result.get_zones()), 0)

    def test_from_geojson_bad_file_returns_empty(self):
        result = LaydownMap.from_geojson("/nonexistent/path/file.geojson")
        self.assertIsInstance(result, LaydownMap)
        self.assertEqual(len(result.get_zones()), 0)

    def test_from_geojson_polygon_is_shapely(self):
        path = self._make([SIMPLE_POLYGON_FEATURE])
        result = LaydownMap.from_geojson(path)
        zone = list(result.get_zones().values())[0]
        self.assertIsInstance(zone, Polygon)

    def test_from_geojson_polygon_area(self):
        feature = {
            "type": "Feature",
            "properties": {"name": "SQUARE"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]
            }
        }
        path = self._make([feature])
        result = LaydownMap.from_geojson(path)
        self.assertAlmostEqual(result.get_zones()["SQUARE"].area, 100.0)


if __name__ == '__main__':
    unittest.main()
