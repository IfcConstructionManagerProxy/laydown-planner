import unittest
import sys
import os

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import DataLoader


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

if __name__ == '__main__':
    unittest.main()