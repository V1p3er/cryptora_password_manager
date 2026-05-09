from datetime import datetime, timezone
from dataclasses import dataclass

from domain.value_objects.created_at import CreatedAt


@dataclass(frozen=True)
class UpdatedAt:
    _value: datetime

    @classmethod
    def now(cls) -> "UpdatedAt":
        return cls(datetime.now(timezone.utc))

    @classmethod
    def from_created(cls, created_at: CreatedAt) -> "UpdatedAt":
        return cls(created_at.value)

    @property
    def value(self) -> datetime:
        return self._value