import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:

    _value: str

    def __post_init__(self):

        try:
            parsed = uuid.UUID(self._value, version=4)
        
        except (ValueError, TypeError, AttributeError):
            raise ValueError("UserId must be a valid uuid version4")
        
        normalized = str(parsed)

        object.__setattr__(self, "_value", normalized)

    @property
    def value(self) -> str:
        return self._value
    
    def __str__(self) -> str:
        return self._value