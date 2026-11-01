import pytest

from src.modules import parse as p

@pytest.mark.parametrize("line, db, expected", [
    ("key1:data1\n", {}, {"key1": "data1"}),
    ("key1:da:ta1\n", {}, {"key1": "da:ta1"}),
    ("key1:data2\n", {"key1": "data1"}, {"key1": "data2"}),
    ("?key1\n", {"key1": "data1"}, {}),
    ("?key1\n", {}, {}),
    ("\n", {}, {}),
    ("key1\n", {}, {}),
])
def test_parse(line, db, expected):
    """Parsing a line of the log applies it to db, invalid lines are ignored"""

    p.parse(line, db)

    assert db == expected, "db should have the expected content"