import pytest
from domain.services.data_encryption_key_deriver import DataEncryptionKeyDeriver
from domain.value_objects.master_password import MasterPassword


class FakeKeyDeriver(DataEncryptionKeyDeriver):
    def derive_key(self, master_password, salt):
        self._validate_salt(salt)
        return b"derived_key_" + salt[:4]


def test_derive_key_returns_bytes():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="StrongP@ssword1")
    salt = b"s" * 16

    result = deriver.derive_key(mp, salt)

    assert isinstance(result, bytes)


def test_derive_key_minimum_salt_length():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="MinimumSalt12!")
    salt = b"a" * 16

    result = deriver.derive_key(mp, salt)

    assert len(result) > 0


def test_derive_key_maximum_salt_length():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="MaximumSalt12@")
    salt = b"b" * 64

    result = deriver.derive_key(mp, salt)

    assert len(result) > 0


def test_derive_key_salt_15_bytes_raises_error():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="ShortSaltErr1!")
    salt = b"s" * 15

    with pytest.raises(ValueError, match="too short"):
        deriver.derive_key(mp, salt)


def test_derive_key_salt_65_bytes_raises_error():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="LongSaltErr12@")
    salt = b"s" * 65

    with pytest.raises(ValueError, match="too long"):
        deriver.derive_key(mp, salt)


def test_derive_key_empty_salt_raises_error():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="EmptySalt12!!")

    with pytest.raises(ValueError, match="too short"):
        deriver.derive_key(mp, b"")


def test_derive_key_salt_wrong_type_raises_error():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="WrongTypeSal1!")

    with pytest.raises(TypeError, match="must be bytes"):
        deriver.derive_key(mp, "not_bytes")


def test_derive_key_salt_none_raises_error():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="NoneSaltErr1@")

    with pytest.raises(TypeError, match="must be bytes"):
        deriver.derive_key(mp, None)


def test_derive_key_different_salts_produce_different_keys():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="DifferentKey1@")

    result1 = deriver.derive_key(mp, b"1" * 16)
    result2 = deriver.derive_key(mp, b"2" * 16)

    assert result1 != result2


def test_derive_key_same_inputs_produce_same_key():
    deriver = FakeKeyDeriver()
    mp = MasterPassword(value="SameKeyTest1@")
    salt = b"c" * 16

    result1 = deriver.derive_key(mp, salt)
    result2 = deriver.derive_key(mp, salt)

    assert result1 == result2