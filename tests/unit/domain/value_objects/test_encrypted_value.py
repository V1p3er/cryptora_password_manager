import pytest
from cryptography.fernet import Fernet
from domain.value_objects.encrypted_value import EncryptedValue

@pytest.fixture
def key():
    return Fernet.generate_key()

def test_create_from_plain_and_decrypt(key):
    secret = "super-secret"
    encrypted = EncryptedValue.from_plain(secret, key)
    decrypted = encrypted.decrypt(key)
    assert decrypted == secret

def test_value_is_ciphertext_not_plaintext(key):
    secret = "very-secret"
    encrypted = EncryptedValue.from_plain(secret, key)
    assert encrypted.value != secret
    assert isinstance(encrypted.value, str)

def test_wrong_key_cannot_decrypt(key):
    encrypted = EncryptedValue.from_plain("secret", key)
    wrong_key = Fernet.generate_key()
    with pytest.raises(ValueError):
        encrypted.decrypt(wrong_key)

def test_invalid_token_rejected():
    with pytest.raises(ValueError):
        EncryptedValue("not-a-valid-token")

def test_str_returns_ciphertext(key):
    encrypted = EncryptedValue.from_plain("secret", key)
    assert str(encrypted) == encrypted.value

def test_repr_hides_value(key):
    encrypted = EncryptedValue.from_plain("secret", key)
    assert "<hidden>" in repr(encrypted)