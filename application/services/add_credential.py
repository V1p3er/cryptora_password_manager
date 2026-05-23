from application.dto.credential_dto import CredentialDTO
from domain.repositories.vault_repository import VaultRepository
from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.value_objects.domain_name import DomainName
from domain.value_objects.service_name import ServiceName
from domain.value_objects.userid import UserId
from domain.value_objects.vault_item_username import VaultItemUsername


class AddCredentialService:
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
        password_key: bytes,
        password_plaintext: str,
        domain: str,
        title: str | None = None,
        username: str | None = None,
    ) -> CredentialDTO:
        vault = self._vault_repository.get_for_user(user_id)
        if vault is None:
            raise ValueError("Vault not found")

        encrypted = self._encryption_service.encrypt(password_plaintext, password_key)
        title_vo = ServiceName(title) if title is not None else None
        username_vo = VaultItemUsername(username) if username is not None else None
        domain_vo = DomainName(domain)

        vault.add_item(
            title=title_vo,
            username=username_vo,
            password=encrypted,
            domain_name=domain_vo,
        )
        self._vault_repository.save(vault)
        added = vault.items[-1]
        return CredentialDTO(
            item_id=added.item_id,
            title=added.title.value if added.title else None,
            username=added.username.value if added.username else None,
            password=password_plaintext,
            domain=added.domain.value,
        )
