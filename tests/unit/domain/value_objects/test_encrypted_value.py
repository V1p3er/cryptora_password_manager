import pytest
from cryptography.fernet import Fernet
from domain.value_objects.encrypted_value import EncryptedValue


def test_encrypt_and_decrypt_roundtrip():
    key = Fernet.generate_key()
    plain = "ArmanTest123!"
    encrypted = EncryptedValue.from_plain(plain, key)
    decrypted = encrypted.decrypt(key)
    assert decrypted == plain
    assert encrypted.value != plain


def test_empty_plaintext_raises():
    key = Fernet.generate_key()
    with pytest.raises(ValueError):
        EncryptedValue.from_plain("", key)


def test_invalid_key_type_raises():
    with pytest.raises(TypeError):
        EncryptedValue.from_plain("data", "not_bytes_key")


def test_decrypt_with_wrong_key_fails():
    key1 = Fernet.generate_key()
    key2 = Fernet.generate_key()
    encrypted = EncryptedValue.from_plain("secret", key1)
    with pytest.raises(ValueError):
        encrypted.decrypt(key2)


def test_repr_and_str_hide_sensitive_data():
    key = Fernet.generate_key()
    val = EncryptedValue.from_plain("SecretPassword!", key)
    assert "SecretPassword" not in repr(val)
    assert "<encrypted>" in str(val)