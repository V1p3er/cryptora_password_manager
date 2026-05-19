# tests/unit/domain/repositories/test_vault_repository.py
import pytest
import uuid
from domain.repositories.vault_repository import VaultRepository
from domain.value_objects.userid import UserId
from domain.value_objects.domain_name import DomainName
from domain.value_objects.encrypted_value import EncryptedValue
from domain.entities.vault import Vault


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


def make_user_id() -> UserId:
    return UserId(value=uuid.uuid4())


def test_save_and_retrieve_vault():
    repo = InMemoryVaultRepository()
    user_id = make_user_id()
    vault = Vault.create_for_user(user_id)
    vault.add_item(
        title=None,
        username=None,
        password=EncryptedValue(value="encrypted_pass"),
        domain_name=DomainName(value="example.com"),
    )

    repo.save(vault)
    retrieved = repo.get_for_user(user_id)

    assert retrieved is not None
    assert len(retrieved.items) == 1
    assert retrieved.items[0].domain == DomainName(value="example.com")


def test_get_for_user_returns_none_for_missing():
    repo = InMemoryVaultRepository()
    result = repo.get_for_user(make_user_id())
    assert result is None


def test_exists_returns_true_for_saved_vault():
    repo = InMemoryVaultRepository()
    user_id = make_user_id()
    vault = Vault.create_for_user(user_id)
    repo.save(vault)

    assert repo.exists(user_id) is True


def test_exists_returns_false_for_missing():
    repo = InMemoryVaultRepository()
    assert repo.exists(make_user_id()) is False


def test_delete_removes_vault():
    repo = InMemoryVaultRepository()
    user_id = make_user_id()
    vault = Vault.create_for_user(user_id)
    repo.save(vault)

    repo.delete(user_id)

    assert repo.exists(user_id) is False


def test_delete_nonexistent_does_not_raise():
    repo = InMemoryVaultRepository()
    repo.delete(make_user_id())


def test_save_persists_multiple_items():
    repo = InMemoryVaultRepository()
    user_id = make_user_id()
    vault = Vault.create_for_user(user_id)
    vault.add_item(None, None, EncryptedValue(value="pass1"), DomainName(value="a.com"))
    vault.add_item(None, None, EncryptedValue(value="pass2"), DomainName(value="b.com"))

    repo.save(vault)
    retrieved = repo.get_for_user(user_id)

    assert len(retrieved.items) == 2


def test_save_updates_existing_vault_with_removed_item():
    repo = InMemoryVaultRepository()
    user_id = make_user_id()
    vault = Vault.create_for_user(user_id)
    vault.add_item(None, None, EncryptedValue(value="pass1"), DomainName(value="a.com"))
    vault.add_item(None, None, EncryptedValue(value="pass2"), DomainName(value="b.com"))
    repo.save(vault)

    vault.remove_item(0)
    repo.save(vault)

    retrieved = repo.get_for_user(user_id)
    assert len(retrieved.items) == 1
    assert retrieved.items[0].item_id == 0