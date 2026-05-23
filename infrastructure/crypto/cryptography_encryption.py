import base64

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.value_objects.encrypted_value import EncryptedValue
from infrastructure.crypto.secure_random import SecureRandom


class CryptographyEncryption(VaultItemEncryptionService):
    NONCE_LENGTH = 12

    def encrypt(self, plaintext: str, key: bytes) -> EncryptedValue:
        self._validate_plaintext(plaintext)
        self._validate_key(key)

        nonce = SecureRandom.bytes(self.NONCE_LENGTH)
        ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
        payload = base64.urlsafe_b64encode(nonce + ciphertext).decode("ascii")

        return EncryptedValue(payload)

    def decrypt(self, encrypted: EncryptedValue, key: bytes) -> str:
        self._validate_key(key)
        if not isinstance(encrypted, EncryptedValue):
            raise TypeError("encrypted must be EncryptedValue")

        try:
            combined = base64.urlsafe_b64decode(encrypted.value.encode("ascii"))
            nonce = combined[: self.NONCE_LENGTH]
            ciphertext = combined[self.NONCE_LENGTH :]
            plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
        except Exception as exc:  # cryptographic decode/decrypt failures
            raise ValueError("Unable to decrypt value") from exc

        return plaintext.decode("utf-8")
