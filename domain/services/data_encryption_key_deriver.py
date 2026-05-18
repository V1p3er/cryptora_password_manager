from abc import ABC, abstractmethod
from domain.value_objects.master_password import MasterPassword


class DataEncryptionKeyDeriver(ABC):
    
    MIN_SALT_LENGTH = 16
    MAX_SALT_LENGTH = 64
    
    @abstractmethod
    def derive_key(
        self, master_password: MasterPassword, salt: bytes) -> bytes:
        pass
    
    def _validate_salt(self, salt: bytes) -> None:
        if not isinstance(salt, bytes):
            raise TypeError(
                f"salt must be bytes, got {type(salt).__name__}"
            )
        if len(salt) < self.MIN_SALT_LENGTH:
            raise ValueError(
                f"salt too short: {len(salt)} bytes. "
                f"Minimum {self.MIN_SALT_LENGTH} required."
            )
        if len(salt) > self.MAX_SALT_LENGTH:
            raise ValueError(
                f"salt too long: {len(salt)} bytes. "
                f"Maximum {self.MAX_SALT_LENGTH} allowed."
            )