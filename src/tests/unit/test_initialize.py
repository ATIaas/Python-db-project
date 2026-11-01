from src.modules import initialize

def test_init(path, dataset):
    """The dataset starts empty and the data file has no content"""

    with open(path, 'r') as f:
        text = f.read()

    assert dataset == {}, "The dataset should be empty"
    assert text == "", "The file should be empty"

def test_init_reads_log(path):
    """Starting the dataset from a log keeps the latest value of each key and skips deleted keys"""

    with open(path, 'w') as f:
        f.write("key1:data1\nkey2:data2\nkey1:data3\n?key2\n\n")

    assert initialize.start_dataset(path) == {"key1": "data3"}, "Only key1 with its latest data should be loaded"