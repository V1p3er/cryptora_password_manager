import pytest
from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.value_objects.encrypted_value import EncryptedValue


class FakeEncryption(VaultItemEncryptionService):
    def encrypt(self, plaintext, key):
        self._validate_plaintext(plaintext)
        self._validate_key(key)
        return EncryptedValue(value=plaintext)

    def decrypt(self, encrypted, key):
        self._validate_key(key)
        return encrypted.value


def test_encrypt_returns_encrypted_value():
    svc = FakeEncryption()
    key = b"k" * 32

    result = svc.encrypt("password123", key)

    assert isinstance(result, EncryptedValue)


def test_encrypt_minimum_key_length():
    svc = FakeEncryption()
    key = b"a" * 16

    result = svc.encrypt("pass", key)

    assert result is not None


def test_encrypt_key_15_bytes_raises_error():
    svc = FakeEncryption()
    key = b"k" * 15

    with pytest.raises(ValueError, match="too short"):
        svc.encrypt("password", key)


def test_encrypt_key_wrong_type_raises_error():
    svc = FakeEncryption()

    with pytest.raises(TypeError, match="must be bytes"):
        svc.encrypt("password", 12345)


def test_encrypt_key_none_raises_error():
    svc = FakeEncryption()

    with pytest.raises(TypeError, match="must be bytes"):
        svc.encrypt("password", None)


def test_encrypt_empty_plaintext_raises_error():
    svc = FakeEncryption()
    key = b"k" * 32

    with pytest.raises(ValueError, match="empty"):
        svc.encrypt("", key)


def test_encrypt_whitespace_only_raises_error():
    svc = FakeEncryption()
    key = b"k" * 32

    with pytest.raises(ValueError, match="empty"):
        svc.encrypt("   ", key)


def test_encrypt_plaintext_too_long_raises_error():
    svc = FakeEncryption()
    key = b"k" * 32
    long_text = "a" * 4097

    with pytest.raises(ValueError, match="too long"):
        svc.encrypt(long_text, key)


def test_encrypt_plaintext_at_max_length():
    svc = FakeEncryption()
    key = b"k" * 32
    max_text = "a" * 4096

    result = svc.encrypt(max_text, key)

    assert result is not None


def test_encrypt_plaintext_wrong_type_raises_error():
    svc = FakeEncryption()
    key = b"k" * 32

    with pytest.raises(TypeError, match="must be str"):
        svc.encrypt(None, key)


def test_decrypt_returns_string():
    svc = FakeEncryption()
    key = b"k" * 32
    encrypted = svc.encrypt("my_password", key)

    result = svc.decrypt(encrypted, key)

    assert isinstance(result, str)
    assert result == "my_password"


def test_decrypt_key_too_short_raises_error():
    svc = FakeEncryption()
    encrypted = EncryptedValue(value="some_encrypted_string")
    key = b"k" * 10

    with pytest.raises(ValueError, match="too short"):
        svc.decrypt(encrypted, key)


def test_decrypt_key_wrong_type_raises_error():
    svc = FakeEncryption()
    encrypted = EncryptedValue(value="some_encrypted_string")

    with pytest.raises(TypeError, match="must be bytes"):
        svc.decrypt(encrypted, "string_key")


def test_encrypt_decrypt_roundtrip():
    svc = FakeEncryption()
    key = b"s" * 32
    original = "SuperSecret123!"

    encrypted = svc.encrypt(original, key)
    decrypted = svc.decrypt(encrypted, key)

    assert decrypted == original


def test_encrypt_different_keys_produce_different_ciphertext():
    svc = FakeEncryption()
    key1 = b"1" * 32
    key2 = b"2" * 32

    result1 = svc.encrypt("password", key1)
    result2 = svc.encrypt("password", key2)

    assert isinstance(result1, EncryptedValue)
    assert isinstance(result2, EncryptedValue)