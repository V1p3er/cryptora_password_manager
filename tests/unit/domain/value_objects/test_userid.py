import pytest
import uuid

from dataclasses import FrozenInstanceError
from domain.value_objects.userid import UserId


def test_valid_uuid():

    raw = str(uuid.uuid4())
    user_id = UserId(raw)

    assert user_id.value == raw


def test_uppercase_normalizaton():

    raw = str(uuid.uuid4())
    upper = raw.upper()

    user_id = UserId(upper)
    assert user_id.value == raw


def test_userid_immutable():
    
    raw = str(uuid.uuid4())
    user_id = UserId(raw)

    with pytest.raises(FrozenInstanceError):
        user_id.value = str(uuid.uuid4())


def test_equal_userid():

    raw = str(uuid.uuid4())
    user_id1 = UserId(raw)
    user_id2 = UserId(raw)

    assert user_id1.value == user_id2.value


def test_not_valid_uuid4():
    
    with pytest.raises(ValueError):
        UserId(str(uuid.uuid1()))


@pytest.mark.parametrize(
    "invalid_inputs",
    [
        "",
        " ",
        "123",
        "something",
        None,
        123
    ]
)


def test_invalid_inputs(invalid_inputs):
    
    with pytest.raises(ValueError):
        UserId(invalid_inputs)