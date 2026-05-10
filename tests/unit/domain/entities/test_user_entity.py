import uuid
import pytest

from domain.entities.user import User
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.password_strength import PasswordStrength
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.updated_at import UpdatedAt



def create_user(argon2_hasher, *, raw_password: str = "initial-password") -> User:
    return User.create(
        user_id=UserId(str(uuid.uuid4())),
        username=Username("arman"),
        password_hash=PasswordHash(argon2_hasher.hash(raw_password)),
        password_strength=PasswordStrength.from_password(raw_password),
        created_at=CreatedAt.now(),
    )


def test_user_creation_sets_updated_at_equal_created_at(argon2_hasher):
    user = create_user(argon2_hasher)

    assert user.created_at.value == user.updated_at.value
    assert user.created_at.value.tzinfo is not None


def test_change_password_updates_hash_strength_and_timestamp(argon2_hasher):
    user = create_user(argon2_hasher)

    new_raw = "new-password"
    new_hash = PasswordHash(argon2_hasher.hash(new_raw))
    new_strength = PasswordStrength.from_password(new_raw)

    before = user.updated_at.value

    user.change_password(new_hash, new_strength)

    assert user.password_hash == new_hash
    assert user.password_strength == new_strength
    assert user.updated_at.value > before


def test_change_password_same_hash_raises(argon2_hasher):
    raw = "same-password"
    same_hash = PasswordHash(argon2_hasher.hash(raw))
    same_strength = PasswordStrength.from_password(raw)

    user = User.create(
        user_id=UserId(str(uuid.uuid4())),
        username=Username("arman"),
        password_hash=same_hash,
        password_strength=same_strength,
        created_at=CreatedAt.now(),
    )

    with pytest.raises(ValueError):
        user.change_password(same_hash, same_strength)