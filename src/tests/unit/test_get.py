import pytest

from src.modules import (set as s,
                         get as g)

def test_get(path, dataset):
    """Getting a key returns the data stored under it"""

    s.set("key1", "data1", dataset, path)
    get = g.get("key1", dataset)

    assert get == "data1", "get should return data1"

def test_get_missing_key(dataset):
    """Getting a key that does not exist raises KeyError"""

    with pytest.raises(KeyError):
        g.get("nokey", dataset)