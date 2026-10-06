import Initialize
import ReadDataset as rd
import SetGet as sg
import Delete as dl
import Consolidate as cs

FILE = 'data.txt'

# Testing
Initialize.init(FILE)
dataset = rd.getdata(FILE)
print(sg.set("key1", "data1", dataset, FILE))
print(sg.set("key2", "data2", dataset, FILE))
print(sg.set("key3", "data3", dataset, FILE))
print(dl.delete("key3", dataset, FILE))

print(cs.consolidate(dataset, FILE))
data = rd.getdata(FILE)
print("Data after consolidation:")
print(data)