import uuid

from domain.entities.user import User
from domain.entities.vault import Vault
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.domain_name import DomainName
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.service_name import ServiceName
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.vault_item_username import VaultItemUsername
from infrastructure.crypto.argon2_key_derivation import Argon2KeyDerivation
from infrastructure.crypto.cryptography_encryption import CryptographyEncryption
from infrastructure.persistence.file_vault_repository import (
    FileStorage,
    FileUserRepository,
    FileVaultRepository,
)
from infrastructure.security.password_hasher import Argon2PasswordHasher, Argon2PasswordVerifier


def test_full_flow_with_real_infrastructure(tmp_path):
    storage = FileStorage(str(tmp_path / "cryptora.json"))
    users = FileUserRepository(storage)
    vaults = FileVaultRepository(storage)
    password = MasterPassword("ValidPassw0rd!")

    user = User.create(
        user_id=UserId(uuid.uuid4()),
        username=Username("infrauser"),
        password_hash=Argon2PasswordHasher.hash(password),
        created_at=CreatedAt.now(),
    )
    users.save(user)

    verifier = Argon2PasswordVerifier()
    assert verifier.verify(password, user.password_hash) is True

    deriver = Argon2KeyDerivation()
    salt = b"s" * 16
    key = deriver.derive_key(password, salt)

    encryption = CryptographyEncryption()
    vault = Vault.create_for_user(user.user_id)
    vault.add_item(
        title=ServiceName("gmail"),
        username=VaultItemUsername("my.user"),
        password=encryption.encrypt("my_mail_password", key),
        domain_name=DomainName("gmail.com"),
    )
    vaults.save(vault)

    loaded_vault = vaults.get_for_user(user.user_id)
    assert loaded_vault is not None
    decrypted = encryption.decrypt(loaded_vault.items[0].password, key)
    assert decrypted == "my_mail_password"
