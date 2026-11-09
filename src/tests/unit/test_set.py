import pytest

from src.modules.exceptions import DBError

from src.modules import set as s

def test_set(path, dataset):
    """Setting a key stores it in memory and appends it to the file"""

    s.set("key1", "data1", dataset, path)

    with (open(path, 'r')) as f:
        text = f.readlines()

    assert dataset["key1"] == "data1", "key1 should be stored in memory"
    assert text == ["key1:data1\n"], "The file should have key1:data1"
    assert s.set("key1", "data1", dataset, path) == "Already exists", "Setting the same data again should not save it"

@pytest.mark.parametrize("key, data", [
    ("a:b", "data1"),
    ("?key1", "data1"),
    ("", "data1"),
    ("key1", "da\nta1"),
])
def test_set_invalid_input(path, dataset, key, data):
    """Setting an invalid key or data raises ValueError and writes nothing"""

    with pytest.raises(DBError):
        s.set(key, data, dataset, path)

    with open(path, 'r') as f:
        text = f.read()

    assert dataset == {}, "Nothing should be saved in memory"
    assert text == "", "Nothing should be written to the file"