import pytest

from _code.modules import (initialize,
                           read_dataset as rd,
                           set as s,
                           delete as dl,
                           consolidate as cl)

FILE = 'testdata.txt'
initialize.init(FILE)

#Reset text file
def resetf():
    with (open(FILE, 'w')) as f:
        f.write("")

dataset = rd.getdata(FILE)

def test_init():
    """The dataset starts empty and the data file has no content"""
    assert dataset == {}, "The dataset should be empty"
    assert (open(FILE, 'r')).read() == "", "The file should be empty"

def test_set():
    """Setting a key stores it in memory and appends it to the file"""

    s.set("key1", "data1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert dataset["key1"] == "data1", "key1 should be stored in memory"
    assert s.set("key1", "data1", dataset, FILE) == "Already exists"
    
    resetf()

def test_get():
    """Getting a key returns the data stored under it"""
    
    s.set("key1", "data1", dataset, FILE)
    get = dataset["key1"]

    assert get == "data1", "get should return data1"
    
    resetf()

def test_delete():
    """Deleting a key empties its position and appends a delete order to the file"""
        
    s.set("key1", "data1", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[-1] == "?key1\n", "The first line of the file should be the delete order for key1"
    assert "key1" not in dataset, "The position of key1 should be empty"
    
    resetf()

def test_delete_missing_key():
    """Deleting a key that does not exist raises KeyError"""

    with pytest.raises(KeyError):
        dl.delete("nokey", dataset, FILE)

def test_consolidate():
    """Consolidating removes deleted keys and keeps the latest valid entries"""
    
    s.set("key1", "data1", dataset, FILE)
    s.set("key2", "data2", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    cl.consolidate(FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[0] == "key2:data2\n", "The first line of the file should be key2:data2"
    
    resetf()
