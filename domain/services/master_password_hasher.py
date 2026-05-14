from argon2 import PasswordHasher as ArgonHasher
from argon2.exceptions import (
    VerifyMismatchError,
    InvalidHash,
)

from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash


class MasterPasswordHasher:

    _hasher = ArgonHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        salt_len=16,
    )

    @classmethod
    def hash(cls, password: MasterPassword) -> PasswordHash:

        hashed = cls._hasher.hash(password.value)

        return PasswordHash(hashed)

    @classmethod
    def verify(
        cls,
        password: MasterPassword,
        password_hash: PasswordHash,
    ) -> bool:

        try:
            return cls._hasher.verify(
                password_hash.value,
                password.value,
            )

        except (VerifyMismatchError, InvalidHash):
            return False
