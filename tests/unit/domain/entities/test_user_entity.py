import pytest
from uuid import uuid4

from domain.entities.user import User
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.updated_at import UpdatedAt


def make_user():
    user_id = UserId(uuid4())
    username = Username("arman")
    password_hash = PasswordHash("hashed_password")
    created_at = CreatedAt.now()

    return User.create(
        user_id=user_id,
        username=username,
        password_hash=password_hash,
        created_at=created_at,
    )


def test_user_creation_sets_fields_correctly():
    user = make_user()

    assert isinstance(user.user_id, UserId)
    assert isinstance(user.username, Username)
    assert isinstance(user.created_at, CreatedAt)
    assert isinstance(user.updated_at, UpdatedAt)


def test_user_creation_sets_updated_equal_to_created():
    user = make_user()

    assert user.updated_at.value == user.created_at.value


def test_change_password_updates_hash():
    user = make_user()

    new_hash = PasswordHash("new_hash")

    user.change_password(new_hash)

    assert user.password_hash == new_hash


def test_change_password_updates_updated_at():
    user = make_user()

    old_updated = user.updated_at.value

    new_hash = PasswordHash("another_hash")
    user.change_password(new_hash)

    assert user.updated_at.value >= old_updated


def test_change_password_rejects_same_hash():
    user = make_user()

    same_hash = user.password_hash
    with pytest.raises(ValueError):
        user.change_password(same_hash)