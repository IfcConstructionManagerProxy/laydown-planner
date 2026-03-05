import unittest
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shapely.geometry import box
from src.objects import Object
from src.placement_optimizer import PlacementOptimizer


class TestPlacementOptimizer(unittest.TestCase):

    def _make_obj(self, name, length, width, weight=100):
        return Object(name, weight, (length, width, 1.0))

    def test_place_single_object_in_large_zone(self):
        zone = box(0, 0, 100, 100)
        obj = self._make_obj("A", 2.0, 2.0)
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, unplaced = optimizer.place_objects(zone, [obj])
        self.assertEqual(len(placements), 1)
        self.assertEqual(len(unplaced), 0)

    def test_place_multiple_objects(self):
        zone = box(0, 0, 100, 100)
        objects = [self._make_obj(f"Obj{i}", 2.0, 2.0) for i in range(3)]
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, unplaced = optimizer.place_objects(zone, objects)
        self.assertEqual(len(placements), 3)
        self.assertEqual(len(unplaced), 0)

    def test_object_too_large_to_fit(self):
        zone = box(0, 0, 5, 5)
        obj = self._make_obj("Big", 200.0, 200.0)
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, unplaced = optimizer.place_objects(zone, [obj])
        self.assertEqual(len(placements), 0)
        self.assertEqual(len(unplaced), 1)

    def test_no_overlap_between_placements(self):
        zone = box(0, 0, 100, 100)
        objects = [self._make_obj(f"Obj{i}", 5.0, 5.0) for i in range(4)]
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, _ = optimizer.place_objects(zone, objects)
        footprints = [p['object'].get_footprint(p['x'], p['y'], p['rotation']) for p in placements]
        for i, fp1 in enumerate(footprints):
            for j, fp2 in enumerate(footprints):
                if i != j:
                    self.assertFalse(fp1.intersects(fp2), f"Footprints {i} and {j} overlap")

    def test_all_placements_within_zone(self):
        zone = box(0, 0, 50, 50)
        objects = [self._make_obj(f"Obj{i}", 3.0, 3.0) for i in range(5)]
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, _ = optimizer.place_objects(zone, objects)
        for p in placements:
            fp = p['object'].get_footprint(p['x'], p['y'], p['rotation'])
            self.assertTrue(zone.contains(fp), "Footprint is not fully within zone")

    def test_bin_packing_legacy(self):
        optimizer = PlacementOptimizer()
        result = optimizer.bin_packing([3, 5, 2, 4], bin_size=6)
        # Every item must appear exactly once across all bins
        all_items = [item for b in result for item in b]
        self.assertEqual(sorted(all_items), sorted([3, 5, 2, 4]))
        # Each bin must not exceed bin_size
        for b in result:
            self.assertLessEqual(sum(b), 6)

    def test_custom_grid_step(self):
        zone = box(0, 0, 20, 20)
        obj = self._make_obj("Small", 1.0, 1.0)
        optimizer = PlacementOptimizer(grid_step=1.0)
        placements, unplaced = optimizer.place_objects(zone, [obj])
        self.assertEqual(len(placements), 1)
        self.assertEqual(len(unplaced), 0)

    def test_rotation_allows_placement(self):
        # Zone is 2 wide × 20 tall; object is 1.5 long × 18 wide.
        # At rotation=0 the object is 1.5 × 18 (too wide to fit in 2-unit width).
        # At rotation=90 the effective dimensions become 18 × 1.5, which fits.
        zone = box(0, 0, 2, 20)
        obj = self._make_obj("LongBeam", 1.5, 18.0)
        optimizer = PlacementOptimizer(grid_step=0.5)
        placements, unplaced = optimizer.place_objects(zone, [obj], rotations=(0, 90))
        self.assertEqual(len(placements), 1, "Object should fit with correct rotation")
        self.assertEqual(len(unplaced), 0)


if __name__ == '__main__':
    unittest.main()