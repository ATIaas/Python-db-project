import pytest

from _code.modules import (initialize,
                           set as s,
                           delete as dl,
                           consolidate as cl)


@pytest.fixture
def FILE(tmp_path):
    """Path of the data file, in a temporary directory"""
    return str(tmp_path / "testdata.txt")


@pytest.fixture
def dataset(FILE):
    return initialize.start_dataset(FILE)


def test_init(FILE, dataset):
    """The dataset starts empty and the data file has no content"""
    assert dataset == {}, "The dataset should be empty"
    assert (open(FILE, 'r')).read() == "", "The file should be empty"

def test_set(FILE, dataset):
    """Setting a key stores it in memory and appends it to the file"""

    s.set("key1", "data1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert dataset["key1"] == "data1", "key1 should be stored in memory"
    assert s.set("key1", "data1", dataset, FILE) == "Already exists"

def test_get(FILE, dataset):
    """Getting a key returns the data stored under it"""
    
    s.set("key1", "data1", dataset, FILE)
    get = dataset["key1"]

    assert get == "data1", "get should return data1"

def test_delete(FILE, dataset):
    """Deleting a key empties its position and appends a delete order to the file"""
        
    s.set("key1", "data1", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[-1] == "?key1\n", "The first line of the file should be the delete order for key1"
    assert "key1" not in dataset, "The position of key1 should be empty"

def test_delete_missing_key(FILE, dataset):
    """Deleting a key that does not exist raises KeyError"""

    with pytest.raises(KeyError):
        dl.delete("nokey", dataset, FILE)

def test_consolidate(FILE, dataset):
    """Consolidating removes deleted keys and keeps the latest valid entries"""
    
    s.set("key1", "data1", dataset, FILE)
    s.set("key2", "data2", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    cl.consolidate(FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[0] == "key2:data2\n", "The first line of the file should be key2:data2"


def test_set_key_with_colon(FILE, dataset):
    """Setting a key that contains ':' raises ValueError"""

    with pytest.raises(ValueError):
        s.set("a:b", "data1", dataset, FILE)

def test_set_key_starting_with_question_mark(FILE, dataset):
    """Setting a key that starts with '?' raises ValueError"""

    with pytest.raises(ValueError):
        s.set("?key1", "data1", dataset, FILE)

def test_set_empty_key(FILE, dataset):
    """Setting an empty key raises ValueError"""

    with pytest.raises(ValueError):
        s.set("", "data1", dataset, FILE)

def test_set_key_with_line_break(FILE, dataset):
    """Setting a key that contains a line break raises ValueError"""

    with pytest.raises(ValueError):
        s.set("key\n1", "data1", dataset, FILE)

def test_set_data_with_line_break(FILE, dataset):
    """Setting data that contains a line break raises ValueError"""

    with pytest.raises(ValueError):
        s.set("key1", "da\nta1", dataset, FILE)
