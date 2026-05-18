from abc import ABC, abstractmethod
from domain.value_objects.encrypted_value import EncryptedValue


class VaultItemEncryptionService(ABC):
    
    MAX_PLAINTEXT_LENGTH = 4096
    MIN_KEY_LENGTH = 16
    
    @abstractmethod
    def encrypt(self, plaintext: str, key: bytes) -> EncryptedValue:
        pass
    
    @abstractmethod
    def decrypt(self, encrypted: EncryptedValue, key: bytes) -> str:
        pass
    
    def _validate_plaintext(self, plaintext: str) -> None:
        if not isinstance(plaintext, str):
            raise TypeError(
                f"plaintext must be str, got {type(plaintext).__name__}"
            )
        if not plaintext.strip():
            raise ValueError("plaintext cannot be empty or only whitespace")
        if len(plaintext) > self.MAX_PLAINTEXT_LENGTH:
            raise ValueError(
                f"plaintext too long: {len(plaintext)} chars. "
                f"Maximum {self.MAX_PLAINTEXT_LENGTH} allowed."
            )
    
    def _validate_key(self, key: bytes) -> None:
        if not isinstance(key, bytes):
            raise TypeError(
                f"key must be bytes, got {type(key).__name__}"
            )
        if len(key) < self.MIN_KEY_LENGTH:
            raise ValueError(
                f"key too short: {len(key)} bytes. "
                f"Minimum {self.MIN_KEY_LENGTH} required."
            )