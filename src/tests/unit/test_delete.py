import pytest

from src.modules import (set as s,
                         delete as dl)

def test_delete(path, dataset):
    """Deleting a key removes it from memory and appends a delete order to the file"""

    s.set("key1", "data1", dataset, path)
    dl.delete("key1", dataset, path)

    with (open(path, 'r')) as f:
        text = f.readlines()

    assert text[-1] == "?key1\n", "The last line of the file should be the delete order for key1"
    assert "key1" not in dataset, "key1 should not be in memory"

def test_delete_missing_key(path, dataset):
    """Deleting a key that does not exist raises KeyError"""

    with pytest.raises(KeyError):
        dl.delete("nokey", dataset, path)