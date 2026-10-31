import pytest

from src.modules import (initialize,
                           set as s,
                           get as g,        # NUEVO
                           delete as dl,
                           consolidate as cl,
                           parse as p)

@pytest.fixture
def path(tmp_path):
    """Path of the data file, in a temporary directory"""
    return str(tmp_path / "testdata.txt")

@pytest.fixture
def dataset(path):
    return initialize.start_dataset(path)

def test_init(path, dataset):
    """The dataset starts empty and the data file has no content"""
    assert dataset == {}, "The dataset should be empty"
    assert (open(path, 'r')).read() == "", "The file should be empty"

def test_set(path, dataset):
    """Setting a key stores it in memory and appends it to the file"""

    s.set("key1", "data1", dataset, path)

    with (open(path, 'r')) as f:
        text = f.readlines()

    assert dataset["key1"] == "data1", "key1 should be stored in memory"
    assert s.set("key1", "data1", dataset, path) == "Already exists"

def test_get(path, dataset):
    """Getting a key returns the data stored under it"""

    s.set("key1", "data1", dataset, path)
    get = g.get("key1", dataset)            # CAMBIADO: antes dataset["key1"]

    assert get == "data1", "get should return data1"

def test_get_missing_key(dataset):          # NUEVO
    """Getting a key that does not exist raises KeyError"""

    with pytest.raises(KeyError):
        g.get("nokey", dataset)

def test_delete(path, dataset):
    """Deleting a key empties its position and appends a delete order to the file"""

    s.set("key1", "data1", dataset, path)
    dl.delete("key1", dataset, path)

    with (open(path, 'r')) as f:
        text = f.readlines()

    assert text[-1] == "?key1\n", "The first line of the file should be the delete order for key1"
    assert "key1" not in dataset, "The position of key1 should be empty"

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

    assert text[0] == "key2:data2\n", "The first line of the file should be key2:data2"

def test_set_key_with_colon(path, dataset):
    """Setting a key that contains ':' raises ValueError"""

    with pytest.raises(ValueError):
        s.set("a:b", "data1", dataset, path)

def test_set_key_starting_with_question_mark(path, dataset):
    """Setting a key that starts with '?' raises ValueError"""

    with pytest.raises(ValueError):
        s.set("?key1", "data1", dataset, path)

def test_set_empty_key(path, dataset):
    """Setting an empty key raises ValueError"""

    with pytest.raises(ValueError):
        s.set("", "data1", dataset, path)

def test_set_key_with_line_break(path, dataset):
    """Setting a key that contains a line break raises ValueError"""

    with pytest.raises(ValueError):
        s.set("key\n1", "data1", dataset, path)

def test_set_data_with_line_break(path, dataset):
    """Setting data that contains a line break raises ValueError"""

    with pytest.raises(ValueError):
        s.set("key1", "da\nta1", dataset, path)

def test_parse_set_line():
    """Parsing a key:data line saves the data under the key"""

    db: dict[str, str] = {}
    p.parse("key1:data1\n", db)

    assert db == {"key1": "data1"}, "key1 should be saved with data1"

def test_parse_data_with_colon():
    """Parsing splits only on the first ':' so the data can contain ':'"""

    db: dict[str, str] = {}
    p.parse("key1:da:ta1\n", db)

    assert db == {"key1": "da:ta1"}, "The ':' should be kept in the data"

def test_parse_delete_line():
    """Parsing a delete order removes the key"""

    db: dict[str, str] = {"key1": "data1"}
    p.parse("?key1\n", db)

    assert db == {}, "key1 should be deleted"

def test_parse_invalid_line():
    """Parsing a line without ':' or '?' does nothing"""

    db: dict[str, str] = {}
    p.parse("\n", db)
    p.parse("key1\n", db)

    assert db == {}, "Invalid lines should be ignored"

def test_init_reads_log(path):
    """Starting the dataset from a log keeps the latest value of each key and skips deleted keys"""

    with open(path, 'w') as f:
        f.write("key1:data1\nkey2:data2\nkey1:data3\n?key2\n\n")

    assert initialize.start_dataset(path) == {"key1": "data3"}, "Only key1 with its latest data should be loaded"