import re
from dataclasses import dataclass

_USERNAME_PATTERN = re.compile(r"^[a-z0-9._-]+$")


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self):

        if not isinstance(self.value, str):
            raise ValueError("Username must be a string")

        normalized = self.value.strip().casefold()

        if not normalized:
            raise ValueError("Username cannot be empty")

        length = len(normalized)

        if length < 5:
            raise ValueError("Username must be at least 5 characters")

        if length > 32:
            raise ValueError("Username must be at most 32 characters")

        if not _USERNAME_PATTERN.match(normalized):
            raise ValueError("Username contains invalid characters")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value