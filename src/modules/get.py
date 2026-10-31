def get(key: str, dataset: dict[str, str]) -> str:
    """Returns the data stored under the key. Raises KeyError if it doesn't exist."""
    if key in dataset and dataset[key] is not None:
         return dataset[key]
    else:
        raise KeyError

