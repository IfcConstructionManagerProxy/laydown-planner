# test_data_loader.py

import pytest
from data_loader import load_data


def test_load_data_success():
    """ Test successful data loading """
    data = load_data('valid_file_path.csv')
    assert data is not None
    assert len(data) > 0


def test_load_data_file_not_found():
    """ Test loading data from a non-existent file """
    with pytest.raises(FileNotFoundError):
        load_data('invalid_file_path.csv')


def test_load_data_empty_file():
    """ Test loading data from an empty file """
    data = load_data('empty_file.csv')
    assert data == []
