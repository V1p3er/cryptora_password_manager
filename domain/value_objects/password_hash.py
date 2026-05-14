from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PasswordHash:
    value: str

    def __post_init__(self) -> None:

        if not isinstance(self.value, str):
            raise TypeError("Password hash must be a string")

        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Password hash cannot be empty")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return "PasswordHash(<hidden>)"