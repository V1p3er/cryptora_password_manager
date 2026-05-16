from dataclasses import dataclass

from domain.value_objects.username import Username
from domain.value_objects.userid import UserId
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.updated_at import UpdatedAt
from domain.value_objects.created_at import CreatedAt

@dataclass(slots=True)
class User:
    _user_id: UserId
    _username: Username
    _password_hash: PasswordHash
    _created_at: CreatedAt
    _updated_at: UpdatedAt

    @classmethod
    def create(
        cls,
        user_id: UserId,
        username: Username,
        password_hash: PasswordHash,
        created_at: CreatedAt,
    ) -> "User":

        updated_at = UpdatedAt(created_at.value)

        return cls(
            _user_id=user_id,
            _username=username,
            _password_hash=password_hash,
            _created_at=created_at,
            _updated_at=updated_at
        )

    def change_password(self, new_password_hash: PasswordHash) -> None:
        if new_password_hash == self._password_hash:
            raise ValueError("New password hash must be different")

        self._password_hash = new_password_hash
        self._updated_at = UpdatedAt.now()

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def username(self) -> Username:
        return self._username

    @property
    def password_hash(self) -> PasswordHash:
        return self._password_hash

    @property
    def created_at(self) -> CreatedAt:
        return self._created_at

    @property
    def updated_at(self) -> UpdatedAt:
        return self._updated_at