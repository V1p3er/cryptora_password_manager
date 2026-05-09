from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass(frozen=True)
class CreatedAt:
    _value: datetime

    @classmethod
    def now(cls) -> "CreatedAt":
        return cls(datetime.now(timezone.utc))

    @property
    def value(self) -> datetime:
        return self._value