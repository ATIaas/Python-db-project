import pytest

from src.modules import log_line as ll

@pytest.mark.parametrize("key, data, line", [
    ("key1", "data1", "key1:data1\n"),
    ("key1", "da:ta1", "key1:da:ta1\n"),
    ("key1", "", "key1:\n"),
])
def test_set_line(key, data, line):
    """The set line of the log is key:data"""

    assert ll.set_line(key, data) == line, "The set line should be key:data"

def test_delete_line():
    """The delete line of the log is ?key"""

    assert ll.delete_line("key1") == "?key1\n", "The delete line should be ?key1"