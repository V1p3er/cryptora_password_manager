import pytest
import uuid
import time
from domain.repositories.user_repository import UserRepository
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.created_at import CreatedAt
from domain.entities.user import User


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}

    def save(self, user: User) -> None:
        self._users[user.user_id] = user

    def get(self, user_id: UserId) -> User | None:
        return self._users.get(user_id)

    def get_by_username(self, username: Username) -> User | None:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def exists(self, user_id: UserId) -> bool:
        return user_id in self._users

    def exists_by_username(self, username: Username) -> bool:
        return any(u.username == username for u in self._users.values())

    def delete(self, user_id: UserId) -> None:
        self._users.pop(user_id, None)


def make_user(username: str = "testuser") -> User:
    return User.create(
        user_id=UserId(value=uuid.uuid4()),
        username=Username(value=username),
        password_hash=PasswordHash(value="hashed_" + "x" * 36),
        created_at=CreatedAt.now(),
    )


def test_save_and_get_user():
    repo = InMemoryUserRepository()
    user = make_user()

    repo.save(user)
    retrieved = repo.get(user.user_id)

    assert retrieved is not None
    assert retrieved.user_id == user.user_id
    assert retrieved.username == user.username


def test_get_nonexistent_user_returns_none():
    repo = InMemoryUserRepository()
    fake_id = UserId(value=uuid.uuid4())

    result = repo.get(fake_id)

    assert result is None


def test_get_by_username_finds_user():
    repo = InMemoryUserRepository()
    user = make_user(username="alice01")
    repo.save(user)

    result = repo.get_by_username(Username(value="alice01"))

    assert result is not None
    assert result.username == Username(value="alice01")


def test_get_by_username_returns_none_for_missing():
    repo = InMemoryUserRepository()

    result = repo.get_by_username(Username(value="nobody1"))

    assert result is None


def test_get_by_username_respects_vo_equality():
    repo = InMemoryUserRepository()
    user = make_user(username="CaseSensitive1")
    repo.save(user)


    result = repo.get_by_username(Username(value="CaseSensitive1"))

    assert result is not None


def test_exists_returns_true_for_saved_user():
    repo = InMemoryUserRepository()
    user = make_user()
    repo.save(user)

    assert repo.exists(user.user_id) is True


def test_exists_returns_false_for_unknown_user():
    repo = InMemoryUserRepository()
    fake_id = UserId(value=uuid.uuid4())

    assert repo.exists(fake_id) is False


def test_exists_by_username_returns_true():
    repo = InMemoryUserRepository()
    user = make_user(username="bob123")
    repo.save(user)

    assert repo.exists_by_username(Username(value="bob123")) is True


def test_exists_by_username_returns_false():
    repo = InMemoryUserRepository()

    assert repo.exists_by_username(Username(value="nobody1")) is False


def test_delete_removes_user():
    repo = InMemoryUserRepository()
    user = make_user()
    repo.save(user)

    repo.delete(user.user_id)

    assert repo.exists(user.user_id) is False


def test_delete_nonexistent_user_does_not_raise():
    repo = InMemoryUserRepository()
    fake_id = UserId(value=uuid.uuid4())

    repo.delete(fake_id)


def test_save_updates_existing_user():
    repo = InMemoryUserRepository()
    user = make_user()
    repo.save(user)

    new_hash = PasswordHash(value="new_hash_" + "y" * 35)
    user.change_password(new_hash)
    repo.save(user)

    retrieved = repo.get(user.user_id)
    assert retrieved.password_hash == new_hash


def test_save_preserves_created_at_on_update():
    repo = InMemoryUserRepository()
    user = make_user()
    original_created_at = user.created_at
    repo.save(user)

    new_hash = PasswordHash(value="another_hash_" + "z" * 30)
    user.change_password(new_hash)
    repo.save(user)

    retrieved = repo.get(user.user_id)
    assert retrieved.created_at == original_created_at


def test_save_updates_updated_at():
    repo = InMemoryUserRepository()
    user = make_user()
    original_updated_at = user.updated_at
    repo.save(user)

    time.sleep(0.001)

    new_hash = PasswordHash(value="fresh_hash_" + "w" * 33)
    user.change_password(new_hash)
    repo.save(user)

    retrieved = repo.get(user.user_id)
    assert retrieved.updated_at.value > original_updated_at.value


def test_save_multiple_users():
    repo = InMemoryUserRepository()
    user1 = make_user(username="user1abc")
    user2 = make_user(username="user2abc")

    repo.save(user1)
    repo.save(user2)

    assert repo.get(user1.user_id) == user1
    assert repo.get(user2.user_id) == user2
    assert repo.get_by_username(Username(value="user1abc")) == user1
    assert repo.get_by_username(Username(value="user2abc")) == user2


def test_save_does_not_mix_users():
    repo = InMemoryUserRepository()
    user1 = make_user(username="user1xyz")
    user2 = make_user(username="user2xyz")
    repo.save(user1)
    repo.save(user2)

    retrieved = repo.get(user1.user_id)

    assert retrieved.username == Username(value="user1xyz")


def test_delete_only_removes_target_user():
    repo = InMemoryUserRepository()
    user1 = make_user(username="keep_user")
    user2 = make_user(username="delete_me")
    repo.save(user1)
    repo.save(user2)

    repo.delete(user2.user_id)

    assert repo.exists(user1.user_id) is True
    assert repo.exists(user2.user_id) is False