from dataclasses import dataclass
from domain.value_objects.password_strength import PasswordStrength
from domain.value_objects.username import Username
from domain.value_objects.userid import UserId
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.updated_at import UpdatedAt
from domain.value_objects.created_at import CreatedAt


@dataclass
class User:
    user_id: UserId
    username: Username
    password_hash: PasswordHash
    password_strength: PasswordStrength
    created_at: CreatedAt
    updated_at: UpdatedAt

    @classmethod
    def create(
        cls,
        *,
        user_id: UserId,
        username: Username,
        password_hash: PasswordHash,
        password_strength: PasswordStrength,
        created_at: CreatedAt,
    ) -> "User":
        return cls(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            password_strength=password_strength,
            created_at=created_at,
            updated_at=UpdatedAt.from_created(created_at),
        )

    def change_password(self, new_password_hash: PasswordHash, new_password_strength: PasswordStrength) -> None:
        if new_password_hash == self.password_hash:
            raise ValueError("New password hash must be different")

        self.password_hash = new_password_hash
        self.password_strength = new_password_strength
        self.updated_at = UpdatedAt.now()