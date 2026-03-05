from shapely.geometry import box, Polygon
from shapely.affinity import rotate, translate


class Object:
    def __init__(self, name, weight, dimensions):
        self.name = name
        self.weight = weight  # in kilograms
        self.dimensions = dimensions  # (length, width, height)

    def get_footprint(self, x=0.0, y=0.0, rotation=0.0) -> Polygon:
        """Return the 2D footprint as a Shapely Polygon at position (x, y) with rotation (degrees)."""
        length, width, _ = self.dimensions
        fp = box(0, 0, length, width)
        fp = rotate(fp, rotation, origin=(0, 0))
        fp = translate(fp, x, y)
        return fp

class Stack:
    def __init__(self):
        self.items = []
        self.total_weight = 0

    def add(self, obj):
        self.items.append(obj)
        self.total_weight += obj.weight

    def can_stack(self, obj):
        # Implement stackability rules and constraints here
        # Example: Check weight limit or dimension compatibility
        return True  # Placeholder for actual logic

    def stack(self, obj):
        if self.can_stack(obj):
            self.add(obj)
        else:
            raise ValueError("Cannot stack object: violates stackability rules")
