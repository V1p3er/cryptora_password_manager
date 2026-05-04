import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class UserId:

    _value: str

    def __post_init__(self):

        if not isinstance(self._value, str) or not self._value.strip():
            raise ValueError("UserId must be a valid uuid version4")
        
        try:
            parsed = uuid.UUID(self._value)
        except (ValueError, TypeError, AttributeError):
            raise ValueError("UserId must be a valid uuid version4")

        if parsed.version != 4:
            raise ValueError("UserId must be a valid uuid version4")

        normalized = str(parsed)
        object.__setattr__(self, "_value", normalized)

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value