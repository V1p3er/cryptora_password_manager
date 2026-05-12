import pytest
from uuid import UUID, uuid4, uuid1

from dataclasses import FrozenInstanceError
from domain.value_objects.userid import UserId

valid_uuid = uuid4()

def test_valid_uuid():


    user_id = UserId(valid_uuid)

    assert user_id.value == valid_uuid


def test_userid_immutable():
    
    user_id = UserId(valid_uuid)

    with pytest.raises(FrozenInstanceError):
        user_id.value = valid_uuid


def test_equal_userid():

    user_id1 = UserId(valid_uuid)
    user_id2 = UserId(valid_uuid)

    assert user_id1 == user_id2


def test_not_valid_uuid4():
    
    with pytest.raises(ValueError):
        UserId(uuid1())