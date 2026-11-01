import os
import tempfile

import pytest

from src.modules import initialize

@pytest.fixture
def path():
    """Path of the data file, in a temporary directory"""
    with tempfile.TemporaryDirectory() as tmp:
        yield os.path.join(tmp, "testdata.txt")

@pytest.fixture
def dataset(path):
    """Dataset loaded from the data file"""
    return initialize.start_dataset(path)