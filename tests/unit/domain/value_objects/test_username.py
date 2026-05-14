import pytest
from dataclasses import FrozenInstanceError

from domain.value_objects.username import Username

### Happy path test ###

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
    "invalid_input, error_type",
    [
        (1421412, TypeError),
        (None, TypeError),
        ("sh", ValueError),
        ("toooolonggggggggggggggggggggggggggggggggggggggggggggggggggg", ValueError),
        (" s", ValueError),
        (" ", ValueError),
        ("", ValueError),
        ("special@#$$%^&*()", ValueError)
    ]
)
def test_invalid_username(invalid_input, error_type):
    with pytest.raises(error_type):
        Username(invalid_input)