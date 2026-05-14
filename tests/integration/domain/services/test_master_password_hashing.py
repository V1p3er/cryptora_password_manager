import pytest

from domain.services.master_password_hasher import MasterPasswordHasher
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash


def test_hash_returns_password_hash():
    password = MasterPassword("strong-secret123SS")

    result = MasterPasswordHasher.hash(password)

    assert isinstance(result, PasswordHash)
    assert result.value != password.value


def test_verify_returns_true_for_correct_password():
    password = MasterPassword("strong-secret123SS")

    password_hash = MasterPasswordHasher.hash(password)

    result = MasterPasswordHasher.verify(password, password_hash)

    assert result is True


def test_verify_returns_false_for_wrong_password():
    password = MasterPassword("strong-secret123SS")
    wrong_password = MasterPassword("wrong-strong-secret123SS")

    password_hash = MasterPasswordHasher.hash(password)

    result = MasterPasswordHasher.verify(wrong_password, password_hash)

    assert result is False


def test_hashing_same_password_produces_different_hashes():
    password = MasterPassword("strong-secret123SS")

    hash1 = MasterPasswordHasher.hash(password)
    hash2 = MasterPasswordHasher.hash(password)

    assert hash1.value != hash2.value


def test_verify_returns_false_for_invalid_hash():
    password = MasterPassword("strong-secret123SS")

    invalid_hash = PasswordHash("invalid-hash-format")

    result = MasterPasswordHasher.verify(password, invalid_hash)

    assert result is False
