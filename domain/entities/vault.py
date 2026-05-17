from dataclasses import dataclass, field

from domain.value_objects.userid import UserId
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.updated_at import UpdatedAt
from domain.entities.vault_item import VaultItem
from domain.value_objects.service_name import ServiceName
from domain.value_objects.domain_name import DomainName
from domain.value_objects.vault_item_username import VaultItemUsername
from domain.value_objects.encrypted_value import EncryptedValue


@dataclass(slots=True)
class Vault:
    _vault_id: UserId
    _user_id: UserId
    _items: list[VaultItem] = field(default_factory=list)

    @classmethod
    def create_for_user(cls, user_id: UserId) -> "Vault":
        return cls(
            _vault_id=user_id,
            _user_id=user_id,
            _items=[]
        )

    def _find_item(self, item_id: int) -> VaultItem:
        for item in self._items:
            if item.item_id == item_id:
                return item
        raise ValueError(f"VaultItem with ID {item_id} not found in this vault.")

    def add_item(self, title: ServiceName | None, username: VaultItemUsername | None, password: EncryptedValue, domain_name: DomainName) -> None:
        
        next_id = len(self._items)
        
        created = CreatedAt.now()

        new_item = VaultItem(
            _item_id=next_id,
            _title=title,
            _username=username,
            _password=password,
            _domain_name=domain_name,
            _created_at=created,
            _updated_at=UpdatedAt(created.value)
        )

        self._items.append(new_item)

    def update_item_title(self, item_id: int, new_title: ServiceName | None) -> None:
        item = self._find_item(item_id)
        item.update_title(new_title)

    def update_item_username(self, item_id: int, new_username: VaultItemUsername | None) -> None:
        item = self._find_item(item_id)
        item.update_username(new_username)

    def update_item_password(self, item_id: int, encrypted_password: EncryptedValue) -> None:
        item = self._find_item(item_id)
        item.update_password(encrypted_password)

    def update_item_domain(self, item_id: int, new_domain_name: DomainName) -> None:
        item = self._find_item(item_id)
        item.update_domain(new_domain_name)

    def remove_item(self, item_id: int) -> None:
        item_to_remove = self._find_item(item_id)
        self._items.remove(item_to_remove)

        for current_index, item in enumerate(self._items):
            item._assign_id(current_index)


    @property
    def vault_id(self) -> str:
        return str(self._vault_id.value)

    @property
    def items(self) -> list[VaultItem]:
        return list(self._items)