import pytest
import time

from domain.entities.vault_item import VaultItem
from domain.value_objects.service_name import ServiceName
from domain.value_objects.domain_name import DomainName
from domain.value_objects.vault_item_username import VaultItemUsername
from domain.value_objects.encrypted_value import EncryptedValue
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.updated_at import UpdatedAt



# HAPPY PATHS

def test_vault_item_creation_and_properties():

    created = CreatedAt.now()
    updated = UpdatedAt(created.value)

    item = VaultItem(
        _item_id=0,
        _title=ServiceName("Netflix"),
        _domain_name=DomainName("netflix.com"),
        _username=VaultItemUsername("bro_user"),
        _password=EncryptedValue("secret123"),
        _created_at=created,
        _updated_at=updated,
    )

    assert item.item_id == 0
    assert item.title.value == "netflix"
    assert item.domain.value == "netflix.com"
    assert item.username.value == "bro_user"
    assert item.password.value == "secret123"


def test_vault_item_handles_nullable_fields():

    item = VaultItem(
        _item_id=5,
        _title=None,
        _domain_name=DomainName("anonymous.org"),
        _username=None,
        _password=EncryptedValue("pass"),
        _created_at=CreatedAt.now(),
        _updated_at=UpdatedAt.now(),
    )

    assert item.title is None
    assert item.username is None
    assert item.domain.value == "anonymous.org"
    assert item.password.value == "pass"


def test_vault_item_update_methods_modify_fields_and_timestamp():

    created = CreatedAt.now()

    item = VaultItem(
        _item_id=0,
        _title=ServiceName("Spotify"),
        _domain_name=DomainName("spotify.com"),
        _username=VaultItemUsername("free_user"),
        _password=EncryptedValue("old_pass"),
        _created_at=created,
        _updated_at=UpdatedAt(created.value),
    )

    time.sleep(0.001)

    item.update_title(ServiceName("Spotify Premium"))
    item.update_username(VaultItemUsername("premium_user"))
    item.update_password(EncryptedValue("new_pass"))
    item.update_domain(DomainName("spotify.co.uk"))

    assert item.title.value == "spotify premium"
    assert item.username.value == "premium_user"
    assert item.password.value == "new_pass"
    assert item.domain.value == "spotify.co.uk"

    assert item._updated_at.value > created.value


def test_vault_item_internal_id_assignment():

    item = VaultItem(
        _item_id=2,
        _title=ServiceName("Github"),
        _domain_name=DomainName("github.com"),
        _username=VaultItemUsername("git_bro"),
        _password=EncryptedValue("token"),
        _created_at=CreatedAt.now(),
        _updated_at=UpdatedAt.now(),
    )

    assert item.item_id == 2

    # internal behavior used by Vault
    item._assign_id(0)

    assert item.item_id == 0