import pytest
from domain.value_objects.master_password import MasterPassword
from dataclasses import FrozenInstanceError

def test_successful_master_password():
    
    password = MasterPassword("StrongPassword123@")
    assert password.value == "StrongPassword123@"

def test_master_pass_is_immutable():
    
    password = MasterPassword("StrongPassword123@")
    
    with pytest.raises(FrozenInstanceError):
        password.value = "StrongPassword123@11"

@pytest.mark.parametrize(
    "invalid_input",
    [
        "sTrong1!",
        "Strongpassword#####",
        "biiisatoo123!!!!!!",
        "BIISTOO123123123!",
        "BIstoooo1231241sf",
        "",
        " ",
        None,
        123414
    ]
)

def test_invalid_master_password(invalid_input):
    
    with pytest.raises(ValueError):
        MasterPassword(invalid_input)