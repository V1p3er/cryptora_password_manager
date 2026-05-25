import uuid

import pytest

from application.exceptions.credential_not_found_error import CredentialNotFoundError
from application.exceptions.invalid_master_password_error import InvalidMasterPasswordError
from application.exceptions.vault_locked_error import VaultLockedError
from application.services.add_credential import AddCredentialService
from application.services.create_vault import CreateVaultService
from application.services.get_credential import GetCredentialService
from application.services.list_credentials import ListCredentialsService
from application.services.lock_vault import LockVaultService
from application.services.remove_credential import RemoveCredentialService
from application.services.unlock_vault import UnlockVaultService, VaultSessionStore
from application.services.update_credential import UpdateCredentialService
from domain.entities.user import User
from domain.services.password_strength_calculator import PasswordStrengthCalculator
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


def test_full_application_e2e(tmp_path):
    storage = FileStorage(str(tmp_path / "cryptora_e2e.json"))
    user_repo = FileUserRepository(storage)
    vault_repo = FileVaultRepository(storage)
    session_store = VaultSessionStore()

    key_deriver = Argon2KeyDerivation()
    encryption = CryptographyEncryption()
    verifier = Argon2PasswordVerifier()

    create_vault = CreateVaultService(vault_repo)
    add_credential = AddCredentialService(vault_repo, encryption)
    list_credentials = ListCredentialsService(vault_repo, session_store)
    get_credential = GetCredentialService(vault_repo, session_store)
    update_credential = UpdateCredentialService(vault_repo, encryption)
    remove_credential = RemoveCredentialService(vault_repo)
    unlock_vault = UnlockVaultService(
        user_repository=user_repo,
        vault_repository=vault_repo,
        password_verifier=verifier,
        key_deriver=key_deriver,
        encryption_service=encryption,
        session_store=session_store,
    )
    lock_vault = LockVaultService(session_store)

    user_id = UserId(uuid.uuid4())
    raw_password = MasterPassword("VeryStrongP@ssword1")
    assert PasswordStrengthCalculator.calculate(raw_password.value).is_strong() is True

    user = User.create(
        user_id=user_id,
        username=Username("e2euser"),
        password_hash=Argon2PasswordHasher.hash(raw_password),
        created_at=CreatedAt.now(),
    )
    user_repo.save(user)

    create_vault.execute(user_id)

    salt = str(user_id.value).encode("utf-8")[:16]
    key = key_deriver.derive_key(raw_password, salt)

    first = add_credential.execute(
        user_id=user_id,
        password_key=key,
        password_plaintext="mail-secret-1",
        domain="gmail.com",
        title="gmail",
        username="me.user",
    )
    second = add_credential.execute(
        user_id=user_id,
        password_key=key,
        password_plaintext="bank-secret-2",
        domain="bank.com",
        title="bank",
        username="bank.user",
    )
    assert first.item_id == 0
    assert second.item_id == 1

    with pytest.raises(VaultLockedError):
        list_credentials.execute(user_id)

    with pytest.raises(InvalidMasterPasswordError):
        unlock_vault.execute(user_id, MasterPassword("WrongPassword!1"))

    unlock_vault.execute(user_id, raw_password)

    all_items = list_credentials.execute(user_id)
    assert len(all_items) == 2
    assert all_items[0].password == "mail-secret-1"
    assert all_items[1].password == "bank-secret-2"

    item = get_credential.execute(user_id, 1)
    assert item.title == "bank"
    assert item.password == "bank-secret-2"

    updated = update_credential.execute(
        user_id=user_id,
        item_id=1,
        password_key=key,
        new_title="primary bank",
        new_password_plaintext="bank-secret-2-updated",
        new_domain="secure.bank.com",
    )
    assert updated.title == "primary bank"
    assert updated.password == "bank-secret-2-updated"

    unlock_vault.execute(user_id, raw_password)
    after_update = get_credential.execute(user_id, 1)
    assert after_update.password == "bank-secret-2-updated"
    assert after_update.domain == "secure.bank.com"

    remove_credential.execute(user_id, 0)
    unlock_vault.execute(user_id, raw_password)
    remaining = list_credentials.execute(user_id)
    assert len(remaining) == 1
    assert remaining[0].item_id == 0

    with pytest.raises(CredentialNotFoundError):
        get_credential.execute(user_id, 1)

    lock_vault.execute(user_id)
    with pytest.raises(VaultLockedError):
        get_credential.execute(user_id, 0)
