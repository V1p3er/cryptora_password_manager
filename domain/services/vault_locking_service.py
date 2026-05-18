from abc import ABC, abstractmethod
from typing import List
from domain.value_objects.userid import UserId
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash


class VaultLockingService(ABC):

    @abstractmethod
    def unlock_vault(self, user_id: UserId, raw_master_password: MasterPassword, stored_password_hash: PasswordHash, vault_items: List) -> List:
        pass
    
    @abstractmethod
    def lock_vault(self, user_id: UserId) -> None:
        pass
    
    def _validate_vault_items(self, items: List) -> None:
        if not isinstance(items, list):
            raise TypeError(
                f"vault_items must be list, got {type(items).__name__}"
            )
        if not items:
            raise ValueError(
                "vault_items cannot be empty. "
                "Vault must have at least one item to unlock."
            )