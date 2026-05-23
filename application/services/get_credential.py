from application.dto.credential_dto import CredentialDTO
from application.exceptions.credential_not_found_error import CredentialNotFoundError
from application.exceptions.vault_locked_error import VaultLockedError
from application.services.unlock_vault import VaultSessionStore
from domain.repositories.vault_repository import VaultRepository
from domain.value_objects.userid import UserId


class GetCredentialService:
    def __init__(
        self, vault_repository: VaultRepository, session_store: VaultSessionStore
    ) -> None:
        self._vault_repository = vault_repository
        self._session_store = session_store

    def execute(self, user_id: UserId, item_id: int) -> CredentialDTO:
        if not self._session_store.is_unlocked(user_id):
            raise VaultLockedError("Vault is locked")

        vault = self._vault_repository.get_for_user(user_id)
        if vault is None:
            raise ValueError("Vault not found")

        for item in vault.items:
            if item.item_id == item_id:
                password = self._session_store.get_password(user_id, item_id)
                if password is None:
                    raise VaultLockedError("Vault is locked")
                return CredentialDTO(
                    item_id=item.item_id,
                    title=item.title.value if item.title else None,
                    username=item.username.value if item.username else None,
                    password=password,
                    domain=item.domain.value,
                )

        raise CredentialNotFoundError(f"Credential {item_id} not found")
