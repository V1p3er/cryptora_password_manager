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

@pytest.mark.parametrize(
    "invalid_inputs",
    [
        "shrt",
        "longggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg",
        "invalid#%^#*",
        "",
        "  ",
        123456,
        None  
    ]
)
def test_invalid_username(invalid_inputs):
    with pytest.raises(ValueError):
        Username(invalid_inputs)