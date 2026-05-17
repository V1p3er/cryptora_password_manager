import pytest
from uuid import uuid4

from domain.entities.vault import Vault
from domain.value_objects.userid import UserId
from domain.value_objects.service_name import ServiceName
from domain.value_objects.domain_name import DomainName
from domain.value_objects.vault_item_username import VaultItemUsername
from domain.value_objects.encrypted_value import EncryptedValue


# =====================================================
# HAPPY PATHS
# =====================================================

def test_vault_factory_creates_correct_id_mapping():
    """Vault factory should mirror the user_id into vault_id."""

    user_uuid = uuid4()
    user_id = UserId(user_uuid)

    vault = Vault.create_for_user(user_id)

    assert vault.vault_id == str(user_uuid)
    assert len(vault.items) == 0


def test_vault_add_item_assigns_sequential_ids():
    """Items added to the vault should receive sequential internal IDs."""

    vault = Vault.create_for_user(UserId(uuid4()))

    vault.add_item(
        ServiceName("Google"),
        VaultItemUsername("u1"),
        EncryptedValue("p1"),
        DomainName("google.com"),
    )

    vault.add_item(
        ServiceName("Apple"),
        VaultItemUsername("u2"),
        EncryptedValue("p2"),
        DomainName("apple.com"),
    )

    items = vault.items

    assert len(items) == 2

    assert items[0].item_id == 0
    assert items[0].title.value == "google"

    assert items[1].item_id == 1
    assert items[1].title.value == "apple"


def test_vault_delegates_item_mutations():
    """Vault should correctly delegate update operations to nested items."""

    vault = Vault.create_for_user(UserId(uuid4()))

    vault.add_item(
        ServiceName("Netflix"),
        VaultItemUsername("bro"),
        EncryptedValue("old"),
        DomainName("netflix.com"),
    )

    vault.update_item_title(0, ServiceName("Netflix Ultra"))
    vault.update_item_username(0, VaultItemUsername("ultra_bro"))
    vault.update_item_password(0, EncryptedValue("new_secret"))
    vault.update_item_domain(0, DomainName("netflix.org"))

    item = vault.items[0]

    assert item.title.value == "netflix ultra"
    assert item.username.value == "ultra_bro"
    assert item.password.value == "new_secret"
    assert item.domain.value == "netflix.org"


def test_vault_remove_middle_item_reindexes_sequence():
    """Removing an item should shift trailing items down to maintain contiguous IDs."""

    vault = Vault.create_for_user(UserId(uuid4()))

    vault.add_item(ServiceName("Spotify"), VaultItemUsername("u"), EncryptedValue("p1"), DomainName("spotify.com"))
    vault.add_item(ServiceName("Netflix"), VaultItemUsername("u"), EncryptedValue("p2"), DomainName("netflix.com"))
    vault.add_item(ServiceName("Github"), VaultItemUsername("u"), EncryptedValue("p3"), DomainName("github.com"))

    vault.remove_item(1)

    items = vault.items

    assert len(items) == 2

    assert items[0].item_id == 0
    assert items[0].title.value == "spotify"

    assert items[1].item_id == 1
    assert items[1].title.value == "github"


# =====================================================
# FAILURE PATHS
# =====================================================

@pytest.mark.parametrize("operation", [
    "title",
    "username",
    "password",
    "domain",
    "remove",
])
def test_vault_operations_on_missing_item_raise_value_error(operation):
    """Operations targeting nonexistent item IDs should raise ValueError."""

    vault = Vault.create_for_user(UserId(uuid4()))

    vault.add_item(
        ServiceName("Valid"),
        VaultItemUsername("user"),
        EncryptedValue("pass"),
        DomainName("valid.com"),
    )

    with pytest.raises(ValueError):

        if operation == "title":
            vault.update_item_title(99, ServiceName("Fail"))

        elif operation == "username":
            vault.update_item_username(99, VaultItemUsername("Fail"))

        elif operation == "password":
            vault.update_item_password(99, EncryptedValue("Fail"))

        elif operation == "domain":
            vault.update_item_domain(99, DomainName("fail.com"))

        elif operation == "remove":
            vault.remove_item(99)