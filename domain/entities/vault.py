from dataclasses import dataclass, field
from typing import List

from domain.value_objects.userid import UserId
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.updated_at import UpdatedAt

from domain.entities.vault_item import VaultItem
from domain.value_objects.service_name import ServiceName
from domain.value_objects.username import Username


@dataclass
class Vault:
    user_id: UserId
    items: List[VaultItem] = field(default_factory=list)
    created_at: CreatedAt = field(default_factory=CreatedAt.now)
    updated_at: UpdatedAt = field(default_factory=UpdatedAt.now)

    def add_item(self, item: VaultItem) -> None:
        for existing in self.items:
            if (
                existing.service_name == item.service_name
                and existing.username == item.username
            ):
                raise ValueError("Vault item already exists")

        self.items.append(item)
        self.updated_at = UpdatedAt.now()

    def remove_item(self, service_name: ServiceName, username: Username) -> None:
        for item in self.items:
            if item.service_name == service_name and item.username == username:
                self.items.remove(item)
                self.updated_at = UpdatedAt.now()
                return

        raise ValueError("Vault item not found")

    def update_item(self, updated_item: VaultItem) -> None:
        for index, item in enumerate(self.items):
            if (
                item.service_name == updated_item.service_name
                and item.username == updated_item.username
            ):
                self.items[index] = updated_item
                self.updated_at = UpdatedAt.now()
                return

        raise ValueError("Vault item not found")
