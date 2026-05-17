from dataclasses import dataclass

from domain.value_objects.service_name import ServiceName
from domain.value_objects.domain_name import DomainName
from domain.value_objects.vault_item_username import VaultItemUsername
from domain.value_objects.encrypted_value import EncryptedValue
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.updated_at import UpdatedAt


@dataclass(slots=True)
class VaultItem:
    _item_id: int
    _title: ServiceName | None
    _domain_name: DomainName
    _username: VaultItemUsername | None
    _password: EncryptedValue
    _created_at: CreatedAt
    _updated_at: UpdatedAt

    def _assign_id(self, new_id: int) -> None:
        self._item_id = new_id

    def update_title(self, new_title: ServiceName | None) -> None:
        self._title = new_title
        self._updated_at = UpdatedAt.now()

    def update_username(self, new_username: VaultItemUsername | None) -> None:
        self._username = new_username
        self._updated_at = UpdatedAt.now()

    def update_password(self, encrypted_password: EncryptedValue) -> None:
        self._password = encrypted_password
        self._updated_at = UpdatedAt.now()

    def update_domain(self, new_domain_name: DomainName) -> None:
        self._domain_name = new_domain_name
        self._updated_at = UpdatedAt.now()

    @property
    def item_id(self) -> int:
        return self._item_id

    @property
    def title(self) -> ServiceName | None:
        return self._title

    @property
    def domain(self) -> DomainName | None:
        return self._domain_name

    @property
    def username(self) -> VaultItemUsername | None:
        return self._username

    @property
    def password(self) -> EncryptedValue:
        return self._password