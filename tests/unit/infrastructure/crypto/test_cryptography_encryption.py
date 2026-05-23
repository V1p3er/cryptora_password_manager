import pytest

from domain.value_objects.encrypted_value import EncryptedValue
from infrastructure.crypto.cryptography_encryption import CryptographyEncryption


def test_encrypt_decrypt_roundtrip():
    service = CryptographyEncryption()
    key = b"k" * 32
    encrypted = service.encrypt("SuperSecret123!", key)
    assert isinstance(encrypted, EncryptedValue)
    assert service.decrypt(encrypted, key) == "SuperSecret123!"


def test_encrypt_same_plaintext_produces_different_payloads():
    service = CryptographyEncryption()
    key = b"k" * 32
    one = service.encrypt("same", key)
    two = service.encrypt("same", key)
    assert one != two


def test_decrypt_with_wrong_key_raises():
    service = CryptographyEncryption()
    encrypted = service.encrypt("payload", b"a" * 32)
    with pytest.raises(ValueError, match="Unable to decrypt"):
        service.decrypt(encrypted, b"b" * 32)
