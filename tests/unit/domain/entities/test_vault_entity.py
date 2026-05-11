import uuid
import pytest
from cryptography.fernet import Fernet

from domain.entities.vault import Vault
from domain.entities.vault_item import VaultItem

from domain.value_objects.userid import UserId
from domain.value_objects.service_name import ServiceName
from domain.value_objects.domain_name import DomainName
from domain.value_objects.username import Username
from domain.value_objects.encrypted_value import EncryptedValue


@pytest.fixture
def encryption_key():
    return Fernet.generate_key()


@pytest.fixture
def vault():
    return Vault(
        user_id=UserId(str(uuid.uuid4()))
    )


@pytest.fixture
def item(encryption_key):
    return VaultItem(
        service_name=ServiceName("gmail"),
        domain_name=DomainName("gmail.com"),
        username=Username("arman123"),
        encrypted_password=EncryptedValue.from_plain(
            "SuperSecret123!",
            encryption_key
        ),
    )


def test_add_item(vault, item):
    vault.add_item(item)

    assert len(vault.items) == 1
    assert item in vault.items


def test_add_duplicate_item_raises(vault, item):
    vault.add_item(item)

    with pytest.raises(ValueError, match="Vault item already exists"):
        vault.add_item(item)


def test_remove_item(vault, item):
    vault.add_item(item)

    vault.remove_item(
        ServiceName("gmail"),
        Username("arman123")
    )

    assert len(vault.items) == 0


def test_remove_nonexistent_item_raises(vault):
    with pytest.raises(ValueError, match="Vault item not found"):
        vault.remove_item(
            ServiceName("github"),
            Username("unknown")
        )


def test_update_item(vault, item, encryption_key):
    vault.add_item(item)

    updated_item = VaultItem(
        service_name=ServiceName("gmail"),
        domain_name=DomainName("gmail.com"),
        username=Username("arman123"),
        encrypted_password=EncryptedValue.from_plain(
            "NewPassword456!",
            encryption_key
        ),
    )

    vault.update_item(updated_item)

    stored_item = vault.items[0]

    decrypted_password = stored_item.encrypted_password.decrypt(
        encryption_key
    )

    assert decrypted_password == "NewPassword456!"


def test_update_nonexistent_item_raises(vault, encryption_key):
    non_existing_item = VaultItem(
        service_name=ServiceName("twitter"),
        domain_name=DomainName("twitter.com"),
        username=Username("ghost"),
        encrypted_password=EncryptedValue.from_plain(
            "ghostpass",
            encryption_key
        ),
    )

    with pytest.raises(ValueError, match="Vault item not found"):
        vault.update_item(non_existing_item)
