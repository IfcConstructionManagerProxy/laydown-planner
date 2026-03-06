import json
from shapely.geometry import Polygon


class LaydownMap:
    def __init__(self, dxf_file_path=None):
        self.dxf_file_path = dxf_file_path
        self.zones = self.parse_dxf() if dxf_file_path else {}

    def parse_dxf(self):
        # Implement DXF parsing logic here
        # Return a dictionary or list of zones parsed from the DXF file.
        return {}

    @classmethod
    def from_geojson(cls, geojson_file_path):
        """Load GeoJSON laydown data from a file and return a LaydownMap."""
        instance = cls()
        try:
            with open(geojson_file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to read GeoJSON: {e}")
            return instance

        zone_count = 0
        for feature in data.get("features", []):
            geometry = feature.get("geometry")
            if geometry is None or geometry.get("type") != "Polygon":
                continue
            coords = geometry.get("coordinates", [])
            if not coords:
                continue
            exterior = coords[0]
            if len(exterior) < 3:
                continue
            properties = feature.get("properties") or {}
            name = properties.get("name") or properties.get("layer") or f"zone_{zone_count}"
            instance.zones[name] = Polygon(exterior)
            zone_count += 1

        return instance

    def get_zones(self):
        return self.zones

    def add_zone(self, zone_name, zone_data):
        self.zones[zone_name] = zone_data

    def remove_zone(self, zone_name):
        if zone_name in self.zones:
            del self.zones[zone_name]

    def get_zone_area(self, zone_name):
        return self.zones[zone_name].area if zone_name in self.zones else 0.0