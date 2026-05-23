import uuid

from domain.entities.user import User
from domain.entities.vault import Vault
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.domain_name import DomainName
from domain.value_objects.encrypted_value import EncryptedValue
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from infrastructure.persistence.file_vault_repository import (
    FileStorage,
    FileUserRepository,
    FileVaultRepository,
)


def test_file_user_repository_save_and_get(tmp_path):
    storage = FileStorage(str(tmp_path / "data.json"))
    repo = FileUserRepository(storage)
    user = User.create(
        user_id=UserId(uuid.uuid4()),
        username=Username("useralpha"),
        password_hash=PasswordHash("hash_value_123"),
        created_at=CreatedAt.now(),
    )
    repo.save(user)
    loaded = repo.get(user.user_id)
    assert loaded is not None
    assert loaded.username == user.username


def test_file_vault_repository_save_and_get(tmp_path):
    storage = FileStorage(str(tmp_path / "data.json"))
    repo = FileVaultRepository(storage)
    user_id = UserId(uuid.uuid4())
    vault = Vault.create_for_user(user_id)
    vault.add_item(None, None, EncryptedValue("enc1"), DomainName("example.com"))
    repo.save(vault)
    loaded = repo.get_for_user(user_id)
    assert loaded is not None
    assert len(loaded.items) == 1
    assert loaded.items[0].domain == DomainName("example.com")
