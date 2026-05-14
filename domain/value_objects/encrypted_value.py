from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class EncryptedValue:

    value: str = field(repr=False)

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("encrypted value should be string")

        normalized = self.value.strip()

        if not normalized:
            raise ValueError("encrypted value cannot be empty")

        object.__setattr__(self, "value", normalized)

    def __repr__(self):
        return "EncryptedValue(<hidden>)"