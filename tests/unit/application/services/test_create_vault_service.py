import uuid

import pytest

from application.services.create_vault import CreateVaultService
from domain.entities.vault import Vault
from domain.repositories.vault_repository import VaultRepository
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


def test_create_vault():
    repo = InMemoryVaultRepository()
    svc = CreateVaultService(repo)
    user_id = UserId(uuid.uuid4())
    dto = svc.execute(user_id)
    assert dto.user_id == str(user_id.value)
    assert repo.exists(user_id) is True


def test_create_vault_when_exists_raises():
    repo = InMemoryVaultRepository()
    user_id = UserId(uuid.uuid4())
    repo.save(Vault.create_for_user(user_id))
    svc = CreateVaultService(repo)
    with pytest.raises(ValueError, match="already exists"):
        svc.execute(user_id)
