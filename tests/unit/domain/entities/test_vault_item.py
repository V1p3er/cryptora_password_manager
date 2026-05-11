import pytest
from cryptography.fernet import Fernet

from domain.entities.vault_item import VaultItem
from domain.value_objects.service_name import ServiceName
from domain.value_objects.domain_name import DomainName
from domain.value_objects.username import Username
from domain.value_objects.encrypted_value import EncryptedValue


def test_encrypt_decrypt_password():
    key = Fernet.generate_key()

    raw_password = "SuperSecret123!"
    encrypted = EncryptedValue.from_plain(raw_password, key)

    decrypted = encrypted.decrypt(key)

    assert decrypted == raw_password
    assert encrypted.value != raw_password


@pytest.fixture
def example_item():
    key = Fernet.generate_key()

    encrypted_pw = EncryptedValue.from_plain("SecretPass!", key)

    return VaultItem(
        service_name=ServiceName("github"),
        domain_name=DomainName("github.com"),
        username=Username("arman_hack"),
        encrypted_password=encrypted_pw,
    )


def test_vault_item_fields(example_item):
    assert example_item.service_name.value == "github"
    assert example_item.domain_name.value == "github.com"
    assert example_item.username.value == "arman_hack"
    assert isinstance(example_item.encrypted_password.value, str)