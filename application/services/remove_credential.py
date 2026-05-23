from application.exceptions.credential_not_found_error import CredentialNotFoundError
from domain.repositories.vault_repository import VaultRepository
from domain.value_objects.userid import UserId


class RemoveCredentialService:
    def __init__(self, vault_repository: VaultRepository) -> None:
        self._vault_repository = vault_repository

    def execute(self, user_id: UserId, item_id: int) -> None:
        vault = self._vault_repository.get_for_user(user_id)
        if vault is None:
            raise ValueError("Vault not found")

        if not any(item.item_id == item_id for item in vault.items):
            raise CredentialNotFoundError(f"Credential {item_id} not found")

        vault.remove_item(item_id)
        self._vault_repository.save(vault)
