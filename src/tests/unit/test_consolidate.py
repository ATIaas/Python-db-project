from src.modules import (set as s,
                         delete as dl,
                         consolidate as cl)

def test_consolidate(path, dataset):
    """Consolidating removes deleted keys and keeps the latest valid entries"""

    s.set("key1", "data1", dataset, path)
    s.set("key2", "data2", dataset, path)
    dl.delete("key1", dataset, path)

    cl.consolidate(path, dataset)

    with (open(path, 'r')) as f:
        text = f.readlines()

    assert text == ["key2:data2\n"], "The file should only have key2:data2"