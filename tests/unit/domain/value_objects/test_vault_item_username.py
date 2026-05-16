import pytest

from domain.value_objects.vault_item_username import VaultItemUsername

### Happy path test ###

def test_valid_username_creation():
    username = VaultItemUsername("john_doe")
    assert username.value == "john_doe"

def test_username_str_representation():
    username = VaultItemUsername("john123")
    assert str(username) == "john123"

def test_username_trims_whitespace():
    username = VaultItemUsername("   john   ")
    assert username.value == "john"

def test_username_allows_email_style():
    username = VaultItemUsername("john@gmail.com")
    assert username.value == "john@gmail.com"

### failures test ###

@pytest.mark.parametrize(
    "invalid_input, error_type",
    [
        (1421412, TypeError),
        (None, TypeError),
        (" ", ValueError),
        ("", ValueError),
        ("a" * 129, ValueError),
        ("special$$%^*()", ValueError)
    ]
)
def test_invalid_username(invalid_input, error_type):
    with pytest.raises(error_type):
        VaultItemUsername(invalid_input)