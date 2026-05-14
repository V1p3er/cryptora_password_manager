import pytest
from dataclasses import FrozenInstanceError

from domain.value_objects.master_password import MasterPassword

### Happy path test ###

def test_successful_master_password():
    password = MasterPassword("StrongPassword123@")
    assert password.value == "StrongPassword123@"

def test_master_pass_is_immutable():
    password = MasterPassword("StrongPassword123@")
    with pytest.raises(FrozenInstanceError):
        password.value = "StrongPassword123@11"

### failures test ###

@pytest.mark.parametrize(
    "invalid_input, error_type",
    [
        ("sTrong1!", ValueError),
        ("Strongpassword#####", ValueError),
        ("biiisatoo123!!!!!!", ValueError),
        ("BIISTOO123123123!", ValueError),
        ("BIstoooo1231241sf", ValueError),
        ("", ValueError),
        (" ", ValueError),
        (None, TypeError),
        (123414, TypeError)
    ]
)

def test_invalid_master_password(invalid_input, error_type):
    with pytest.raises(error_type):
        MasterPassword(invalid_input)