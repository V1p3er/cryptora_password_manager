from dataclasses import dataclass, field

from application.exceptions.invalid_master_password_error import InvalidMasterPasswordError
from domain.repositories.user_repository import UserRepository
from domain.repositories.vault_repository import VaultRepository
from domain.services.data_encryption_key_deriver import DataEncryptionKeyDeriver
from domain.services.master_password_verifier import MasterPasswordVerifier
from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.userid import UserId


@dataclass(slots=True)
class VaultSessionStore:
    _sessions: dict[UserId, dict[int, str]] = field(default_factory=dict)

    def set_password(self, user_id: UserId, item_id: int, password: str) -> None:
        self._sessions.setdefault(user_id, {})[item_id] = password

    def get_password(self, user_id: UserId, item_id: int) -> str | None:
        return self._sessions.get(user_id, {}).get(item_id)

    def is_unlocked(self, user_id: UserId) -> bool:
        return user_id in self._sessions

    def lock(self, user_id: UserId) -> None:
        self._sessions.pop(user_id, None)


class UnlockVaultService:
    def __init__(
        self,
        user_repository: UserRepository,
        vault_repository: VaultRepository,
        password_verifier: MasterPasswordVerifier,
        key_deriver: DataEncryptionKeyDeriver,
        encryption_service: VaultItemEncryptionService,
        session_store: VaultSessionStore,
    ) -> None:
        self._user_repository = user_repository
        self._vault_repository = vault_repository
        self._password_verifier = password_verifier
        self._key_deriver = key_deriver
        self._encryption_service = encryption_service
        self._session_store = session_store

    def execute(self, user_id: UserId, raw_master_password: MasterPassword) -> None:
        user = self._user_repository.get(user_id)
        if user is None:
            raise ValueError("User not found")

        vault = self._vault_repository.get_for_user(user_id)
        if vault is None:
            raise ValueError("Vault not found")

        if not self._password_verifier.verify(raw_master_password, user.password_hash):
            raise InvalidMasterPasswordError("Invalid master password")

        salt = str(user.user_id.value).encode("utf-8")[:16]
        key = self._key_deriver.derive_key(raw_master_password, salt)

        for item in vault.items:
            decrypted = self._encryption_service.decrypt(item.password, key)
            self._session_store.set_password(user_id, item.item_id, decrypted)
