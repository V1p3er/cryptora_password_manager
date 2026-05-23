import uuid

from application.services.add_credential import AddCredentialService
from application.services.create_vault import CreateVaultService
from application.services.get_credential import GetCredentialService
from application.services.list_credentials import ListCredentialsService
from application.services.lock_vault import LockVaultService
from application.services.remove_credential import RemoveCredentialService
from application.services.unlock_vault import UnlockVaultService, VaultSessionStore
from application.services.update_credential import UpdateCredentialService
from domain.entities.user import User
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from infrastructure.crypto.argon2_key_derivation import Argon2KeyDerivation
from infrastructure.crypto.cryptography_encryption import CryptographyEncryption
from infrastructure.persistence.file_vault_repository import (
    FileStorage,
    FileUserRepository,
    FileVaultRepository,
)
from infrastructure.security.password_hasher import Argon2PasswordHasher, Argon2PasswordVerifier


def test_application_flow_with_real_infrastructure(tmp_path):
    storage = FileStorage(str(tmp_path / "app_flow.json"))
    user_repo = FileUserRepository(storage)
    vault_repo = FileVaultRepository(storage)
    sessions = VaultSessionStore()

    raw_password = MasterPassword("ValidPassw0rd!")
    user_id = UserId(uuid.uuid4())
    user = User.create(
        user_id=user_id,
        username=Username("appflowuser"),
        password_hash=Argon2PasswordHasher.hash(raw_password),
        created_at=CreatedAt.now(),
    )
    user_repo.save(user)

    create_vault = CreateVaultService(vault_repo)
    create_vault.execute(user_id)

    salt = str(user_id.value).encode("utf-8")[:16]
    key = Argon2KeyDerivation().derive_key(raw_password, salt)

    add = AddCredentialService(vault_repo, CryptographyEncryption())
    first = add.execute(
        user_id=user_id,
        password_key=key,
        password_plaintext="first-secret",
        domain="gmail.com",
        title="gmail",
        username="me.user",
    )
    assert first.item_id == 0

    unlock = UnlockVaultService(
        user_repository=user_repo,
        vault_repository=vault_repo,
        password_verifier=Argon2PasswordVerifier(),
        key_deriver=Argon2KeyDerivation(),
        encryption_service=CryptographyEncryption(),
        session_store=sessions,
    )
    unlock.execute(user_id, raw_password)

    list_svc = ListCredentialsService(vault_repo, sessions)
    credentials = list_svc.execute(user_id)
    assert len(credentials) == 1
    assert credentials[0].password == "first-secret"

    update = UpdateCredentialService(vault_repo, CryptographyEncryption())
    update.execute(
        user_id=user_id,
        item_id=0,
        new_password_plaintext="updated-secret",
        password_key=key,
        new_domain="google.com",
    )

    unlock.execute(user_id, raw_password)
    get_svc = GetCredentialService(vault_repo, sessions)
    credential = get_svc.execute(user_id, 0)
    assert credential.password == "updated-secret"
    assert credential.domain == "google.com"

    remove = RemoveCredentialService(vault_repo)
    remove.execute(user_id, 0)
    assert len(vault_repo.get_for_user(user_id).items) == 0

    lock = LockVaultService(sessions)
    lock.execute(user_id)
