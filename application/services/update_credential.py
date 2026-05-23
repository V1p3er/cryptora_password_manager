from application.dto.credential_dto import CredentialDTO
from application.exceptions.credential_not_found_error import CredentialNotFoundError
from domain.repositories.vault_repository import VaultRepository
from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.value_objects.domain_name import DomainName
from domain.value_objects.service_name import ServiceName
from domain.value_objects.userid import UserId
from domain.value_objects.vault_item_username import VaultItemUsername


class UpdateCredentialService:
    def __init__(
        self,
        vault_repository: VaultRepository,
        encryption_service: VaultItemEncryptionService,
    ) -> None:
        self._vault_repository = vault_repository
        self._encryption_service = encryption_service

    def execute(
        self,
        *,
        user_id: UserId,
        item_id: int,
        password_key: bytes | None = None,
        new_title: str | None = None,
        new_username: str | None = None,
        new_password_plaintext: str | None = None,
        new_domain: str | None = None,
    ) -> CredentialDTO:
        vault = self._vault_repository.get_for_user(user_id)
        if vault is None:
            raise ValueError("Vault not found")

        item_exists = any(item.item_id == item_id for item in vault.items)
        if not item_exists:
            raise CredentialNotFoundError(f"Credential {item_id} not found")

        if new_title is not None:
            vault.update_item_title(item_id, ServiceName(new_title))
        if new_username is not None:
            vault.update_item_username(item_id, VaultItemUsername(new_username))
        if new_domain is not None:
            vault.update_item_domain(item_id, DomainName(new_domain))
        if new_password_plaintext is not None:
            if password_key is None:
                raise ValueError("password_key is required to update password")
            encrypted = self._encryption_service.encrypt(new_password_plaintext, password_key)
            vault.update_item_password(item_id, encrypted)

        self._vault_repository.save(vault)

        updated_item = vault.items[item_id]
        return CredentialDTO(
            item_id=updated_item.item_id,
            title=updated_item.title.value if updated_item.title else None,
            username=updated_item.username.value if updated_item.username else None,
            password=new_password_plaintext or updated_item.password.value,
            domain=updated_item.domain.value,
        )
