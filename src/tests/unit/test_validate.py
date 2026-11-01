import pytest

from src.modules import validate as v

@pytest.mark.parametrize("key", ["key1", "key 1", "k?y1", "城市"])
def test_validate_key_valid(key):
    """Validating a valid key does not raise"""

    assert v.validate_key(key) is None, "The key should be valid"

@pytest.mark.parametrize("key", ["", "a:b", "?key1", "key\n1"])
def test_validate_key_invalid(key):
    """Validating a key that would corrupt the log raises ValueError"""

    with pytest.raises(ValueError):
        v.validate_key(key)

@pytest.mark.parametrize("data", ["data1", "da:ta1", "?data1", "", "Москва"])
def test_validate_data_valid(data):
    """Validating data with ':', '?' or no characters does not raise"""

    assert v.validate_data(data) is None, "The data should be valid"

def test_validate_data_invalid():
    """Validating data with a line break raises ValueError"""

    with pytest.raises(ValueError):
        v.validate_data("da\nta1")