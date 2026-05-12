import re
from dataclasses import dataclass

_USERNAME_PATTERN = re.compile(r"^[a-z0-9._-]+$")

MIN_LENGTH = 5
MAX_LENGTH = 32


@dataclass(frozen=True, slots=True)
class Username:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("Username must be a string")

        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("Username cannot be empty")

        if not normalized.isascii():
            raise ValueError("Username must contain only ASCII characters")

        if not (MIN_LENGTH <= len(normalized) <= MAX_LENGTH):
            raise ValueError(
                f"Username must be between {MIN_LENGTH} and {MAX_LENGTH} characters"
            )

        if not _USERNAME_PATTERN.fullmatch(normalized):
            raise ValueError(
                "Username can only contain lowercase letters, numbers, dots, hyphens, and underscores"
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
