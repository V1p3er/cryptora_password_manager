from __future__ import annotations

from dataclasses import dataclass

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError


@dataclass(frozen=True)
class PasswordHash:

    _value: str

    _hasher = PasswordHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        salt_len=16,
    )

    def __post_init__(self) -> None:
        if not isinstance(self._value, str):
            raise TypeError("Password hash must be a string")

        normalized = self._value.strip()

        if not normalized:
            raise ValueError("Password hash cannot be empty")

        try:
            PasswordHash._hasher.verify(normalized, "__dummy_wrong_password__")
        except VerifyMismatchError:
            pass
        except InvalidHash as exc:
            raise ValueError("Invalid password hash format") from exc

        object.__setattr__(self, "_value", normalized)

    @classmethod
    def from_plain(cls, plain_password: str) -> PasswordHash:

        if not isinstance(plain_password, str):
            raise TypeError("Password must be a string")

        if not plain_password:
            raise ValueError("Password cannot be empty")

        hashed = cls._hasher.hash(plain_password)
        return cls(hashed)

    def verify(self, plain_password: str) -> bool:

        if not isinstance(plain_password, str):
            raise TypeError("Password must be a string")

        try:
            return self._hasher.verify(self._value, plain_password)
        except VerifyMismatchError:
            return False
        except InvalidHash as exc:
            raise ValueError("Stored password hash is invalid") from exc

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return "PasswordHash(<hidden>)"
