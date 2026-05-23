import uuid

import pytest

from application.exceptions.credential_not_found_error import CredentialNotFoundError
from application.exceptions.vault_locked_error import VaultLockedError
from application.services.add_credential import AddCredentialService
from application.services.get_credential import GetCredentialService
from application.services.list_credentials import ListCredentialsService
from application.services.remove_credential import RemoveCredentialService
from application.services.unlock_vault import VaultSessionStore
from application.services.update_credential import UpdateCredentialService
from domain.entities.vault import Vault
from domain.repositories.vault_repository import VaultRepository
from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.value_objects.domain_name import DomainName
from domain.value_objects.encrypted_value import EncryptedValue
from domain.value_objects.userid import UserId


class InMemoryVaultRepository(VaultRepository):
    def __init__(self):
        self._vaults = {}

    def save(self, vault: Vault) -> None:
        self._vaults[vault._user_id] = vault

    def get_for_user(self, user_id: UserId) -> Vault | None:
        return self._vaults.get(user_id)

    def exists(self, user_id: UserId) -> bool:
        return user_id in self._vaults

    def delete(self, user_id: UserId) -> None:
        self._vaults.pop(user_id, None)


class FakeEncryption(VaultItemEncryptionService):
    def encrypt(self, plaintext: str, key: bytes) -> EncryptedValue:
        self._validate_plaintext(plaintext)
        self._validate_key(key)
        return EncryptedValue(f"enc::{plaintext}")

    def decrypt(self, encrypted: EncryptedValue, key: bytes) -> str:
        self._validate_key(key)
        return encrypted.value.replace("enc::", "", 1)


def test_add_and_update_and_remove_credential():
    user_id = UserId(uuid.uuid4())
    repo = InMemoryVaultRepository()
    repo.save(Vault.create_for_user(user_id))
    encryption = FakeEncryption()

    add_svc = AddCredentialService(repo, encryption)
    created = add_svc.execute(
        user_id=user_id,
        password_key=b"k" * 32,
        password_plaintext="secret123",
        domain="gmail.com",
        title="gmail",
        username="me.user",
    )
    assert created.item_id == 0

    update_svc = UpdateCredentialService(repo, encryption)
    updated = update_svc.execute(
        user_id=user_id,
        item_id=0,
        new_title="google mail",
        new_password_plaintext="newsecret123",
        password_key=b"k" * 32,
    )
    assert updated.title == "google mail"
    assert updated.password == "newsecret123"

    remove_svc = RemoveCredentialService(repo)
    remove_svc.execute(user_id, 0)
    assert len(repo.get_for_user(user_id).items) == 0


def test_get_and_list_require_unlock():
    user_id = UserId(uuid.uuid4())
    repo = InMemoryVaultRepository()
    vault = Vault.create_for_user(user_id)
    vault.add_item(None, None, EncryptedValue("enc::my-password"), domain_name=DomainName("example.com"))
    repo.save(vault)
    sessions = VaultSessionStore()

    get_svc = GetCredentialService(repo, sessions)
    list_svc = ListCredentialsService(repo, sessions)

    with pytest.raises(VaultLockedError):
        get_svc.execute(user_id, 0)
    with pytest.raises(VaultLockedError):
        list_svc.execute(user_id)

    sessions.set_password(user_id, 0, "my-password")
    dto = get_svc.execute(user_id, 0)
    all_items = list_svc.execute(user_id)
    assert dto.password == "my-password"
    assert len(all_items) == 1


def test_remove_missing_credential_raises():
    user_id = UserId(uuid.uuid4())
    repo = InMemoryVaultRepository()
    repo.save(Vault.create_for_user(user_id))
    svc = RemoveCredentialService(repo)
    with pytest.raises(CredentialNotFoundError):
        svc.execute(user_id, 10)
