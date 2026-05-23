import json
from datetime import datetime
from pathlib import Path
from uuid import UUID

from domain.entities.user import User
from domain.entities.vault import Vault
from domain.entities.vault_item import VaultItem
from domain.repositories.user_repository import UserRepository
from domain.repositories.vault_repository import VaultRepository
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.domain_name import DomainName
from domain.value_objects.encrypted_value import EncryptedValue
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.service_name import ServiceName
from domain.value_objects.updated_at import UpdatedAt
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.vault_item_username import VaultItemUsername


class FileStorage:
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def load(self) -> dict:
        if not self._path.exists():
            return {"users": {}, "vaults": {}}
        return json.loads(self._path.read_text(encoding="utf-8"))

    def save(self, data: dict) -> None:
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class FileUserRepository(UserRepository):
    def __init__(self, storage: FileStorage) -> None:
        self._storage = storage

    def save(self, user: User) -> None:
        data = self._storage.load()
        data["users"][str(user.user_id.value)] = self._serialize_user(user)
        self._storage.save(data)

    def get(self, user_id: UserId) -> User | None:
        data = self._storage.load()
        raw = data["users"].get(str(user_id.value))
        if raw is None:
            return None
        return self._deserialize_user(raw)

    def get_by_username(self, username: Username) -> User | None:
        data = self._storage.load()
        for raw in data["users"].values():
            if raw["username"] == username.value:
                return self._deserialize_user(raw)
        return None

    def exists(self, user_id: UserId) -> bool:
        data = self._storage.load()
        return str(user_id.value) in data["users"]

    def exists_by_username(self, username: Username) -> bool:
        return self.get_by_username(username) is not None

    def delete(self, user_id: UserId) -> None:
        data = self._storage.load()
        data["users"].pop(str(user_id.value), None)
        self._storage.save(data)

    @staticmethod
    def _serialize_user(user: User) -> dict:
        return {
            "user_id": str(user.user_id.value),
            "username": user.username.value,
            "password_hash": user.password_hash.value,
            "created_at": user.created_at.value.isoformat(),
            "updated_at": user.updated_at.value.isoformat(),
        }

    @staticmethod
    def _deserialize_user(raw: dict) -> User:
        return User(
            _user_id=UserId(UUID(raw["user_id"])),
            _username=Username(raw["username"]),
            _password_hash=PasswordHash(raw["password_hash"]),
            _created_at=CreatedAt(datetime.fromisoformat(raw["created_at"])),
            _updated_at=UpdatedAt(datetime.fromisoformat(raw["updated_at"])),
        )


class FileVaultRepository(VaultRepository):
    def __init__(self, storage: FileStorage) -> None:
        self._storage = storage

    def save(self, vault: Vault) -> None:
        data = self._storage.load()
        data["vaults"][str(vault._user_id.value)] = self._serialize_vault(vault)
        self._storage.save(data)

    def get_for_user(self, user_id: UserId) -> Vault | None:
        data = self._storage.load()
        raw = data["vaults"].get(str(user_id.value))
        if raw is None:
            return None
        return self._deserialize_vault(raw)

    def exists(self, user_id: UserId) -> bool:
        data = self._storage.load()
        return str(user_id.value) in data["vaults"]

    def delete(self, user_id: UserId) -> None:
        data = self._storage.load()
        data["vaults"].pop(str(user_id.value), None)
        self._storage.save(data)

    @staticmethod
    def _serialize_vault(vault: Vault) -> dict:
        return {
            "vault_id": str(vault._vault_id.value),
            "user_id": str(vault._user_id.value),
            "items": [
                {
                    "item_id": item.item_id,
                    "title": item.title.value if item.title else None,
                    "username": item.username.value if item.username else None,
                    "password": item.password.value,
                    "domain": item.domain.value,
                    "created_at": item._created_at.value.isoformat(),
                    "updated_at": item._updated_at.value.isoformat(),
                }
                for item in vault.items
            ],
        }

    @staticmethod
    def _deserialize_vault(raw: dict) -> Vault:
        items = []
        for item_raw in raw["items"]:
            items.append(
                VaultItem(
                    _item_id=item_raw["item_id"],
                    _title=ServiceName(item_raw["title"]) if item_raw["title"] else None,
                    _domain_name=DomainName(item_raw["domain"]),
                    _username=VaultItemUsername(item_raw["username"])
                    if item_raw["username"]
                    else None,
                    _password=EncryptedValue(item_raw["password"]),
                    _created_at=CreatedAt(datetime.fromisoformat(item_raw["created_at"])),
                    _updated_at=UpdatedAt(datetime.fromisoformat(item_raw["updated_at"])),
                )
            )

        return Vault(
            _vault_id=UserId(UUID(raw["vault_id"])),
            _user_id=UserId(UUID(raw["user_id"])),
            _items=items,
        )
