import pytest

from infrastructure.crypto.secure_random import SecureRandom


def test_bytes_returns_requested_length():
    value = SecureRandom.bytes(16)
    assert isinstance(value, bytes)
    assert len(value) == 16


def test_bytes_invalid_length_type_raises():
    with pytest.raises(TypeError):
        SecureRandom.bytes("16")


def test_bytes_non_positive_raises():
    with pytest.raises(ValueError):
        SecureRandom.bytes(0)
