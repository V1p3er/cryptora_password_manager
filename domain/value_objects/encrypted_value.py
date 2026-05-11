from __future__ import annotations

from dataclasses import dataclass
from cryptography.fernet import Fernet, InvalidToken


@dataclass(frozen=True)
class EncryptedValue:
    _value: str

    def __post_init__(self) -> None:
        if not isinstance(self._value, str):
            raise TypeError("Encrypted value must be a string")

        normalized = self._value.strip()

        if not normalized:
            raise ValueError("Encrypted value cannot be empty")

        object.__setattr__(self, "_value", normalized)

    @staticmethod
    def _build_fernet(key: bytes) -> Fernet:
        if not isinstance(key, bytes):
            raise TypeError("Key must be bytes")

        try:
            return Fernet(key)
        except Exception as exc:
            raise ValueError("Invalid encryption key") from exc

    @classmethod
    def from_plain(cls, plain_text: str, key: bytes) -> "EncryptedValue":
        if not isinstance(plain_text, str):
            raise TypeError("Plain text must be a string")

        plain_text = plain_text.strip()

        if not plain_text:
            raise ValueError("Plain text cannot be empty")

        fernet = cls._build_fernet(key)

        encrypted = fernet.encrypt(
            plain_text.encode("utf-8")
        ).decode("utf-8")

        return cls(encrypted)

    def decrypt(self, key: bytes) -> str:
        fernet = self._build_fernet(key)

        try:
            decrypted = fernet.decrypt(
                self._value.encode("utf-8")
            )
        except InvalidToken as exc:
            raise ValueError("Decryption failed") from exc

        return decrypted.decode("utf-8")

    @property
    def value(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return "EncryptedValue(<hidden>)"

    def __str__(self) -> str:
        return "<encrypted>"