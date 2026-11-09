import pytest

from src.modules.exceptions import DBKeyError

from src.modules import (initialize,
                         set as s,
                         get as g,
                         delete as dl)

def test_set_overwrite(path, dataset):
    """Setting a key that already exists with other data keeps the new data, also after reloading"""

    s.set("key1", "data1", dataset, path)
    s.set("key1", "data2", dataset, path)

    assert dataset["key1"] == "data2", "key1 should have data2 in memory"
    assert initialize.start_dataset(path)["key1"] == "data2", "key1 should have data2 after reloading"

def test_get_deleted_key(path, dataset):
    """Getting a key that was deleted raises KeyError"""

    s.set("key1", "data1", dataset, path)
    dl.delete("key1", dataset, path)

    with pytest.raises(DBKeyError):
        g.get("key1", dataset)