import pytest
from domain.value_objects.username import Username
from dataclasses import FrozenInstanceError

def test_correct_username():
    
    username = Username(" Armangg ")
    assert username.value == "armangg"


### failures test ###
def test_username_is_immutable():
    username = Username("arman")
    with pytest.raises(FrozenInstanceError):
        username.value = "ali"

def test_hash_and_username_equality():
    username1 = Username("Arman")
    username2 = Username("arman")

    assert username1 == username2
    assert hash(username1) == hash(username2)

def test_no_string_username():
    with pytest.raises(ValueError):
        Username(124151)

def test_short_username():
    with pytest.raises(ValueError):
        Username("ag")

def test_long_username():
    with pytest.raises(ValueError):
        Username("a2c94f10c50de39b6sdfsdfgaggsdgsadgsdagjhrjyjf74b52d89318a523b764cbdA")
    
def test_not_match_username_pattern():
    with pytest.raises(ValueError):
        Username("Arman13!!^")

def test_empty_username():
    with pytest.raises(ValueError):
        Username("")

def test_only_space_username():
    with pytest.raises(ValueError):
        Username("     ")
    
def test_none_username():
    with pytest.raises(ValueError):
        Username(None)