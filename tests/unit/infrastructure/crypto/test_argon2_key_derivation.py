import pytest

from domain.value_objects.master_password import MasterPassword
from infrastructure.crypto.argon2_key_derivation import Argon2KeyDerivation


def test_derive_key_returns_bytes():
    deriver = Argon2KeyDerivation()
    key = deriver.derive_key(MasterPassword("ValidPassw0rd!"), b"s" * 16)
    assert isinstance(key, bytes)
    assert len(key) == 32


def test_derive_key_is_deterministic_for_same_input():
    deriver = Argon2KeyDerivation()
    password = MasterPassword("ValidPassw0rd!")
    salt = b"s" * 16
    assert deriver.derive_key(password, salt) == deriver.derive_key(password, salt)


def test_derive_key_rejects_invalid_salt():
    deriver = Argon2KeyDerivation()
    with pytest.raises(ValueError, match="too short"):
        deriver.derive_key(MasterPassword("ValidPassw0rd!"), b"x" * 8)
