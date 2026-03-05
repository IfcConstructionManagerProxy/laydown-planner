import ezdxf
from shapely.geometry import Polygon


class LaydownMap:
    def __init__(self, dxf_file_path):
        self.dxf_file_path = dxf_file_path
        self.zones = self.parse_dxf()

    def parse_dxf(self):
        """Parse LWPOLYLINE/POLYLINE entities from DXF as named Shapely Polygons."""
        zones = {}
        try:
            doc = ezdxf.readfile(self.dxf_file_path)
        except Exception as e:
            print(f"Failed to read DXF: {e}")
            return zones

        msp = doc.modelspace()
        zone_count = 0
        for entity in msp:
            if entity.dxftype() in ("LWPOLYLINE", "POLYLINE"):
                points = [(p[0], p[1]) for p in entity.get_points()]
                if len(points) >= 3:
                    name = entity.dxf.layer if entity.dxf.layer else f"zone_{zone_count}"
                    zones[name] = Polygon(points)
                    zone_count += 1
        return zones

    def get_zones(self):
        return self.zones

    def add_zone(self, zone_name, polygon: Polygon):
        """Add a zone with a Shapely Polygon as its geometry."""
        self.zones[zone_name] = polygon

    def remove_zone(self, zone_name):
        if zone_name in self.zones:
            del self.zones[zone_name]

    def get_zone_area(self, zone_name):
        """Return the area of a named zone in m²."""
        return self.zones[zone_name].area if zone_name in self.zones else 0.0