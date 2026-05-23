import uuid

from domain.entities.vault import Vault
from domain.value_objects.userid import UserId
from infrastructure.persistence.postgresql_vault_repository import PostgreSQLVaultRepository


def test_save_and_get():
    repo = PostgreSQLVaultRepository()
    user_id = UserId(uuid.uuid4())
    vault = Vault.create_for_user(user_id)
    repo.save(vault)
    assert repo.get_for_user(user_id) is not None


def test_delete():
    repo = PostgreSQLVaultRepository()
    user_id = UserId(uuid.uuid4())
    repo.save(Vault.create_for_user(user_id))
    repo.delete(user_id)
    assert repo.exists(user_id) is False
