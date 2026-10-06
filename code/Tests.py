import pytest

import Initialize
import ReadDataset as rd
import SetGet as sg
import DicConvert as con
import Delete as dl
import Consolidate as cl

#print(sg.set("key2", "data2", dataset, FILE))
#print(sg.set("key3", "data3", dataset, FILE))
#print(dl.delete("key3", dataset, FILE))
#print(dataset)

FILE = 'data.txt'
Initialize.init(FILE)

#Reset text file
def resetf():
    with (open(FILE, 'w')) as f:
        f.write("")

dataset = rd.getdata(FILE)

def test_init():
    assert dataset == []
    assert (open(FILE, 'r')).read() == ""

def test_set():

    sg.set("key1", "data1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert dataset[con.convert("key1")] == "data1"
    assert text[0] == "key1:data1\n"
    
    resetf()

def test_get():
    
    sg.set("key1", "data1", dataset, FILE)
    get = sg.get("key1", dataset)

    assert get == "data1"
    
    resetf()

def test_delete():
        
    sg.set("key1", "data1", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[0] == "?key1\n"
    assert dataset[con.convert("key1")] == ""
    
    resetf()

def test_consolidate():
    
    sg.set("key1", "data1", dataset, FILE)
    sg.set("key2", "data2", dataset, FILE)
    dl.delete("key1", dataset, FILE)

    cl.consolidate(FILE)

    with (open(FILE, 'r')) as f:
        text = f.readlines()

    assert text[0] == "key2:data2\n"
    
    resetf()