import re
from dataclasses import dataclass

_DOMAIN_PATTERN = re.compile(
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


@dataclass(frozen=True, slots=True)
class DomainName:

    value: str

    def __post_init__(self):

        if not isinstance(self.value, str):
            raise TypeError("Domain must be a string")

        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("Domain cannot be empty")

        if not _DOMAIN_PATTERN.fullmatch(normalized):
            raise ValueError("Invalid domain name")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value