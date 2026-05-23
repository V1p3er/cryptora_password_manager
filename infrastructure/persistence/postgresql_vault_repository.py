from domain.repositories.vault_repository import VaultRepository
from domain.value_objects.userid import UserId
from domain.entities.vault import Vault


class PostgreSQLVaultRepository(VaultRepository):
    """
    PostgreSQL adapter seam.
    Backed by in-memory storage for now until DB session wiring is added.
    """

    def __init__(self) -> None:
        self._vaults: dict[UserId, Vault] = {}

    def save(self, vault: Vault) -> None:
        self._vaults[vault._user_id] = vault

    def get_for_user(self, user_id: UserId) -> Vault | None:
        return self._vaults.get(user_id)

    def exists(self, user_id: UserId) -> bool:
        return user_id in self._vaults

    def delete(self, user_id: UserId) -> None:
        self._vaults.pop(user_id, None)
