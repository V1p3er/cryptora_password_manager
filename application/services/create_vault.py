from application.dto.vault_dto import VaultDTO
from domain.entities.vault import Vault
from domain.repositories.vault_repository import VaultRepository
from domain.value_objects.userid import UserId


class CreateVaultService:
    def __init__(self, vault_repository: VaultRepository) -> None:
        self._vault_repository = vault_repository

    def execute(self, user_id: UserId) -> VaultDTO:
        if self._vault_repository.exists(user_id):
            raise ValueError("Vault already exists")

        vault = Vault.create_for_user(user_id)
        self._vault_repository.save(vault)
        return VaultDTO(vault_id=vault.vault_id, user_id=str(user_id.value), items=[])
