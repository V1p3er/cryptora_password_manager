import re
from dataclasses import dataclass

_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9._@\-+]+$")

MIN_LENGTH = 1
MAX_LENGTH = 128


@dataclass(frozen=True, slots=True)
class VaultItemUsername:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("Vault item username must be a string")

        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Vault item username cannot be empty")

        if len(normalized) > MAX_LENGTH:
            raise ValueError(
                f"Vault item username must not exceed {MAX_LENGTH} characters"
            )

        if not normalized.isascii():
            raise ValueError("Vault item username must contain only ASCII characters")

        if not _USERNAME_PATTERN.fullmatch(normalized):
            raise ValueError(
                "Vault item username contains invalid characters"
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value