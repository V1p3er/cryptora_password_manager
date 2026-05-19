from abc import ABC, abstractmethod
from typing import Optional
from domain.value_objects.userid import UserId
from domain.entities.vault import Vault


class VaultRepository(ABC):

    @abstractmethod
    def save(self, vault: Vault) -> None:
        pass

    @abstractmethod
    def get_for_user(self, user_id: UserId) -> Optional[Vault]:
        pass

    @abstractmethod
    def exists(self, user_id: UserId) -> bool:
        pass

    @abstractmethod
    def delete(self, user_id: UserId) -> None:
        pass