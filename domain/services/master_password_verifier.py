from abc import ABC, abstractmethod
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash


class MasterPasswordVerifier(ABC):
    @abstractmethod
    def verify(self, raw_password: MasterPassword, stored_hash: PasswordHash) -> bool:
        pass