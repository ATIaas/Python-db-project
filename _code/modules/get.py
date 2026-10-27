def get(key, dataset):
    """Returns the data stored under the key. Raises KeyError if it doesn't exist."""
    return dataset[key]