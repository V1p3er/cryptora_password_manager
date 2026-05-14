import pytest

from domain.value_objects.encrypted_value import EncryptedValue

### Happy path test ###
def test_create_valid_encrypted_value():
    value = EncryptedValue("abc123")
    assert value.value == "abc123"

def test_strip_whitespace_on_creation():
    value = EncryptedValue("   abc123   ")
    assert value.value == "abc123"

def test_repr_does_not_leak_value():
    value = EncryptedValue("secret_data")
    assert "secret_data" not in repr(value)
    assert repr(value) == "EncryptedValue(<hidden>)"

def test_value_object_is_immutable():
    value = EncryptedValue("abc123")
    with pytest.raises(AttributeError):
        value.value = "new_value"

### failures test ###

def test_empty_string_raises_error():
    with pytest.raises(ValueError):
        EncryptedValue("")

def test_whitespace_only_raises_error():
    with pytest.raises(ValueError):
        EncryptedValue("     ")

def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        EncryptedValue(123)