import pytest
from dataclasses import FrozenInstanceError

from domain.value_objects.password_hash import PasswordHash


def test_should_create_password_hash_with_valid_string():
    ph = PasswordHash("hashed_value")

    assert ph.value == "hashed_value"


def test_should_strip_whitespace_from_hash():
    ph = PasswordHash("   hashed_value   ")

    assert ph.value == "hashed_value"


def test_should_raise_type_error_when_hash_is_not_string():
    with pytest.raises(TypeError):
        PasswordHash(123)


def test_should_raise_value_error_when_hash_is_empty():
    with pytest.raises(ValueError):
        PasswordHash("   ")


def test_password_hash_should_be_immutable():
    ph = PasswordHash("hashed_value")

    with pytest.raises(FrozenInstanceError):
        ph.value = "new_hash"


def test_str_should_return_hash_value():
    ph = PasswordHash("hashed_value")

    assert str(ph) == "hashed_value"


def test_repr_should_hide_hash_value():
    ph = PasswordHash("hashed_value")

    assert repr(ph) == "PasswordHash(<hidden>)"
