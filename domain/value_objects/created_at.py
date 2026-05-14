from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreatedAt:
    _value: datetime

    def __post_init__(self):

        if self._value.tzinfo is None:
            raise ValueError("CreatedAt must be timezone-aware")

    @classmethod
    def now(cls) -> "CreatedAt":
        return cls(datetime.now(timezone.utc))

    @property
    def value(self) -> datetime:
        return self._value
