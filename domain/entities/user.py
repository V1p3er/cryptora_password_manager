from dataclasses import dataclass

from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.updated_at import UpdatedAt


@dataclass
class User:
    user_id: UserId
    username: Username
    password_hash: PasswordHash
    created_at: CreatedAt
    updated_at: UpdatedAt

    @classmethod
    def create(
        cls,
        *,
        user_id: UserId,
        username: Username,
        password_hash: PasswordHash,
        created_at: CreatedAt,
    ) -> "User":
        return cls(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            created_at=created_at,
            updated_at=UpdatedAt.from_created(created_at),
        )

    def change_password(self, new_password_hash: PasswordHash) -> None:
        if new_password_hash == self.password_hash:
            raise ValueError("New password hash must be different")

        self.password_hash = new_password_hash
        self.updated_at = UpdatedAt.now()