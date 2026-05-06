from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class UpdatedAt:
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise TypeError("Updated At must be datetime")
        if self.value.tzinfo is None:
            raise ValueError("Updated At must be timezone-aware")

    @classmethod
    def now(cls):
        return cls(datetime.now(timezone.utc))
