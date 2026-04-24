import pytest
from domain.value_objects.master_password import MasterPassword


def test_successful_input():
    
    password = MasterPassword("StrongPassword123@")
    assert password.value == "StrongPassword123@"



def test_short_password():
    with pytest.raises(ValueError):
        MasterPassword("sTrong1!")

def test_pass_without_number():
    with pytest.raises(ValueError):
        MasterPassword("Strongpassword#####")

def test_pass_without_uppercase():
    with pytest.raises(ValueError):
        MasterPassword("biiisatoo123!!!!!!")

def test_pass_without_lowercase():
    with pytest.raises(ValueError):
        MasterPassword("BIISTOO123123123!")
    
def test_pass_without_special_chars():
    with pytest.raises(ValueError):
        MasterPassword("BIstoooo1231241sf")

def test_empty_pass():
    with pytest.raises(ValueError):
        MasterPassword("")

def test_none_pass():
    with pytest.raises(ValueError):
        MasterPassword(None)

def test_only_space():
    with pytest.raises(ValueError):
        MasterPassword("    ")