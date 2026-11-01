import os
import tempfile

import pytest

from src.modules import (initialize,
                           set as s,
                           get as g,
                           delete as dl,
                           consolidate as cl,
                           parse as p,
                           log_line as ll,
                           validate as v)

@pytest.fixture
def path():
    """Path of the data file, in a temporary directory"""
    with tempfile.TemporaryDirectory() as tmp:
        yield os.path.join(tmp, "testdata.txt")

@pytest.fixture
def dataset(path):
    """Dataset loaded from the data file"""
    return initialize.start_dataset(path)

def test_init(path, dataset):
    """The dataset starts empty and the data file has no content"""

    with open(path, 'r') as f:
        text = f.read()

    assert dataset == {}, "The dataset should be empty"
    assert text == "", "The file should be empty"

def test_set(path, dataset):
    """Setting a key stores it in memory and appends it to the file"""

    s.set("key1", "data1", dataset, path)

    with (open(path, 'r')) as f:
        text = f.readlines()

    assert dataset["key1"] == "data1", "key1 should be stored in memory"
    assert text == ["key1:data1\n"], "The file should have key1:data1"
    assert s.set("key1", "data1", dataset, path) == "Already exists", "Setting the same data again should not save it"

def test_set_overwrite(path, dataset):
    """Setting a key that already exists with other data keeps the new data, also after reloading"""

    s.set("key1", "data1", dataset, path)
    s.set("key1", "data2", dataset, path)

    assert dataset["key1"] == "data2", "key1 should have data2 in memory"
    assert initialize.start_dataset(path)["key1"] == "data2", "key1 should have data2 after reloading"

def test_get(path, dataset):
    """Getting a key returns the data stored under it"""

    s.set("key1", "data1", dataset, path)
    get = g.get("key1", dataset)

    assert get == "data1", "get should return data1"

def test_get_missing_key(dataset):
    """Getting a key that does not exist raises KeyError"""

    with pytest.raises(KeyError):
        g.get("nokey", dataset)

def test_get_deleted_key(path, dataset):
    """Getting a key that was deleted raises KeyError"""

    s.set("key1", "data1", dataset, path)
    dl.delete("key1", dataset, path)

    with pytest.raises(KeyError):
        g.get("key1", dataset)

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

def test_consolidate(path, dataset):
    """Consolidating removes deleted keys and keeps the latest valid entries"""

    s.set("key1", "data1", dataset, path)
    s.set("key2", "data2", dataset, path)
    dl.delete("key1", dataset, path)

    cl.consolidate(path, dataset)

    with (open(path, 'r')) as f:
        text = f.readlines()

    assert text == ["key2:data2\n"], "The file should only have key2:data2"

@pytest.mark.parametrize("key, data", [
    ("a:b", "data1"),
    ("?key1", "data1"),
    ("", "data1"),
    ("key1", "da\nta1"),
])
def test_set_invalid_input(path, dataset, key, data):
    """Setting an invalid key or data raises ValueError and writes nothing"""

    with pytest.raises(ValueError):
        s.set(key, data, dataset, path)

    with open(path, 'r') as f:
        text = f.read()

    assert dataset == {}, "Nothing should be saved in memory"
    assert text == "", "Nothing should be written to the file"

@pytest.mark.parametrize("line, db, expected", [
    ("key1:data1\n", {}, {"key1": "data1"}),
    ("key1:da:ta1\n", {}, {"key1": "da:ta1"}),
    ("key1:data2\n", {"key1": "data1"}, {"key1": "data2"}),
    ("?key1\n", {"key1": "data1"}, {}),
    ("?key1\n", {}, {}),
    ("\n", {}, {}),
    ("key1\n", {}, {}),
])
def test_parse(line, db, expected):
    """Parsing a line of the log applies it to db, invalid lines are ignored"""

    p.parse(line, db)

    assert db == expected, "db should have the expected content"

def test_init_reads_log(path):
    """Starting the dataset from a log keeps the latest value of each key and skips deleted keys"""

    with open(path, 'w') as f:
        f.write("key1:data1\nkey2:data2\nkey1:data3\n?key2\n\n")

    assert initialize.start_dataset(path) == {"key1": "data3"}, "Only key1 with its latest data should be loaded"

@pytest.mark.parametrize("key, data, line", [
    ("key1", "data1", "key1:data1\n"),
    ("key1", "da:ta1", "key1:da:ta1\n"),
    ("key1", "", "key1:\n"),
])
def test_set_line(key, data, line):
    """The set line of the log is key:data"""

    assert ll.set_line(key, data) == line, "The set line should be key:data"

def test_delete_line():
    """The delete line of the log is ?key"""

    assert ll.delete_line("key1") == "?key1\n", "The delete line should be ?key1"

@pytest.mark.parametrize("key", ["key1", "key 1", "k?y1", "城市"])
def test_validate_key_valid(key):
    """Validating a valid key does not raise"""

    assert v.validate_key(key) is None, "The key should be valid"

@pytest.mark.parametrize("key", ["", "a:b", "?key1", "key\n1"])
def test_validate_key_invalid(key):
    """Validating a key that would corrupt the log raises ValueError"""

    with pytest.raises(ValueError):
        v.validate_key(key)

@pytest.mark.parametrize("data", ["data1", "da:ta1", "?data1", "", "Москва"])
def test_validate_data_valid(data):
    """Validating data with ':', '?' or no characters does not raise"""

    assert v.validate_data(data) is None, "The data should be valid"

def test_validate_data_invalid():
    """Validating data with a line break raises ValueError"""

    with pytest.raises(ValueError):
        v.validate_data("da\nta1")