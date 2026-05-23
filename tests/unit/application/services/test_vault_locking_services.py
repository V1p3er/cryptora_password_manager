import uuid

import pytest

from application.exceptions.invalid_master_password_error import InvalidMasterPasswordError
from application.services.lock_vault import LockVaultService
from application.services.unlock_vault import UnlockVaultService, VaultSessionStore
from domain.entities.user import User
from domain.entities.vault import Vault
from domain.repositories.user_repository import UserRepository
from domain.repositories.vault_repository import VaultRepository
from domain.services.data_encryption_key_deriver import DataEncryptionKeyDeriver
from domain.services.master_password_verifier import MasterPasswordVerifier
from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.domain_name import DomainName
from domain.value_objects.encrypted_value import EncryptedValue
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}

    def save(self, user):
        self._users[user.user_id] = user

    def get(self, user_id):
        return self._users.get(user_id)

    def get_by_username(self, username):
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def exists(self, user_id):
        return user_id in self._users

    def exists_by_username(self, username):
        return any(user.username == username for user in self._users.values())

    def delete(self, user_id):
        self._users.pop(user_id, None)


class InMemoryVaultRepository(VaultRepository):
    def __init__(self):
        self._vaults = {}

    def save(self, vault):
        self._vaults[vault._user_id] = vault

    def get_for_user(self, user_id):
        return self._vaults.get(user_id)

    def exists(self, user_id):
        return user_id in self._vaults

    def delete(self, user_id):
        self._vaults.pop(user_id, None)


class FakeVerifier(MasterPasswordVerifier):
    def verify(self, raw_password, stored_hash):
        return stored_hash.value == f"h::{raw_password.value}"


class FakeDeriver(DataEncryptionKeyDeriver):
    def derive_key(self, master_password, salt):
        self._validate_salt(salt)
        return b"k" * 32


class FakeEncryption(VaultItemEncryptionService):
    def encrypt(self, plaintext, key):
        self._validate_plaintext(plaintext)
        self._validate_key(key)
        return EncryptedValue(f"enc::{plaintext}")

    def decrypt(self, encrypted, key):
        self._validate_key(key)
        return encrypted.value.replace("enc::", "", 1)


def test_unlock_and_lock_vault_flow():
    user_repo = InMemoryUserRepository()
    vault_repo = InMemoryVaultRepository()
    sessions = VaultSessionStore()
    svc = UnlockVaultService(
        user_repository=user_repo,
        vault_repository=vault_repo,
        password_verifier=FakeVerifier(),
        key_deriver=FakeDeriver(),
        encryption_service=FakeEncryption(),
        session_store=sessions,
    )

    user_id = UserId(uuid.uuid4())
    password = MasterPassword("ValidPassw0rd!")
    user = User.create(
        user_id=user_id,
        username=Username("lockuser"),
        password_hash=PasswordHash(f"h::{password.value}"),
        created_at=CreatedAt.now(),
    )
    user_repo.save(user)
    vault = Vault.create_for_user(user_id)
    vault.add_item(None, None, EncryptedValue("enc::my-pass"), DomainName("example.com"))
    vault_repo.save(vault)

    svc.execute(user_id, password)
    assert sessions.get_password(user_id, 0) == "my-pass"

    lock_svc = LockVaultService(sessions)
    lock_svc.execute(user_id)
    assert sessions.get_password(user_id, 0) is None


def test_unlock_invalid_password_raises():
    user_repo = InMemoryUserRepository()
    vault_repo = InMemoryVaultRepository()
    sessions = VaultSessionStore()
    svc = UnlockVaultService(
        user_repository=user_repo,
        vault_repository=vault_repo,
        password_verifier=FakeVerifier(),
        key_deriver=FakeDeriver(),
        encryption_service=FakeEncryption(),
        session_store=sessions,
    )

    user_id = UserId(uuid.uuid4())
    user = User.create(
        user_id=user_id,
        username=Username("lockuser2"),
        password_hash=PasswordHash("h::DifferentPassword1!"),
        created_at=CreatedAt.now(),
    )
    user_repo.save(user)
    vault_repo.save(Vault.create_for_user(user_id))

    with pytest.raises(InvalidMasterPasswordError):
        svc.execute(user_id, MasterPassword("ValidPassw0rd!"))
