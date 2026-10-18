import pytest

import initialize
import read_dataset as rd
import set_get as sg
import dic_convert as con
import delete as dl
import consolidate as cl

#print(sg.set("key2", "data2", dataset, FILE))
#print(sg.set("key3", "data3", dataset, FILE))
#print(dl.delete("key3", dataset, FILE))
#print(dataset)

FILE = 'data.txt'
initialize.init(FILE)

#Reset text file
def resetf():
    with (open(FILE, 'w')) as f:
        f.write("")

dataset = rd.getdata(FILE)

def test_init():
    """The dataset starts empty and the data file has no content"""
    assert dataset == [], "The dataset should be empty"
    assert (open(FILE, 'r')).read() == "", "The file should be empty"

def test_set():
    """Setting a key stores it in memory and appends it to the file"""

    sg.set("key1", "data1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert dataset[con.convert("key1")] == "data1", "key1 should be stored in memory"
    assert text[0] == "key1:data1\n", "The first line of the file should be key1:data1"
    
    resetf()

def test_get():
    """Getting a key returns the data stored under it"""
    
    sg.set("key1", "data1", dataset, FILE)
    get = sg.get("key1", dataset)

    assert get == "data1", "get should return data1"
    
    resetf()

def test_delete():
    """Deleting a key empties its position and appends a delete order to the file"""
        
    sg.set("key1", "data1", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[0] == "?key1\n", "The first line of the file should be the delete order for key1"
    assert dataset[con.convert("key1")] == "", "The position of key1 should be empty"
    
    resetf()

def test_delete_missing_key():
    """Deleting a key that does not exist raises KeyError"""

    with pytest.raises(KeyError):
        dl.delete("nokey", dataset, FILE)

def test_consolidate():
    """Consolidating removes deleted keys and keeps the latest valid entries"""
    
    sg.set("key1", "data1", dataset, FILE)
    sg.set("key2", "data2", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    cl.consolidate(FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[0] == "key2:data2\n", "The first line of the file should be key2:data2"
    
    resetf()