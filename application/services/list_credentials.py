from application.dto.credential_dto import CredentialDTO
from application.exceptions.vault_locked_error import VaultLockedError
from application.services.unlock_vault import VaultSessionStore
from domain.repositories.vault_repository import VaultRepository
from domain.value_objects.userid import UserId


class ListCredentialsService:
    def __init__(
        self, vault_repository: VaultRepository, session_store: VaultSessionStore
    ) -> None:
        self._vault_repository = vault_repository
        self._session_store = session_store

    def execute(self, user_id: UserId) -> list[CredentialDTO]:
        if not self._session_store.is_unlocked(user_id):
            raise VaultLockedError("Vault is locked")

        vault = self._vault_repository.get_for_user(user_id)
        if vault is None:
            raise ValueError("Vault not found")

        output: list[CredentialDTO] = []
        for item in vault.items:
            password = self._session_store.get_password(user_id, item.item_id)
            if password is None:
                raise VaultLockedError("Vault is locked")
            output.append(
                CredentialDTO(
                    item_id=item.item_id,
                    title=item.title.value if item.title else None,
                    username=item.username.value if item.username else None,
                    password=password,
                    domain=item.domain.value,
                )
            )
        return output
