import pytest

from domain.value_objects.password_hash import PasswordHash


def test_create_from_plain_and_verify():
    password = "SuperStrong!Passw0rd"

    password_hash = PasswordHash.from_plain(password)

    assert isinstance(password_hash, PasswordHash)
    assert password_hash.value != password

    assert password_hash.verify(password) is True


def test_verify_wrong_password_returns_false():
    password = "correct-password"
    wrong = "wrong-password"

    password_hash = PasswordHash.from_plain(password)

    assert password_hash.verify(wrong) is False


def test_invalid_hash_format_rejected():
    with pytest.raises(ValueError):
        PasswordHash("not-a-valid-argon2-hash")


def test_empty_password_rejected_in_factory():
    with pytest.raises(ValueError):
        PasswordHash.from_plain("")


def test_non_string_password_rejected_in_factory():
    with pytest.raises(TypeError):
        PasswordHash.from_plain(123)


def test_non_string_hash_rejected_in_constructor():
    with pytest.raises(TypeError):
        PasswordHash(123)


def test_repr_hides_hash():
    password_hash = PasswordHash.from_plain("some-password")

    assert "<hidden>" in repr(password_hash)


def test_value_returns_raw_hash_string():
    password = "my-password"
    password_hash = PasswordHash.from_plain(password)

    stored = password_hash.value

    assert stored.startswith("$argon2")
    assert isinstance(stored, str)
