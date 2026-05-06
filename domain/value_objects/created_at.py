from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class CreatedAt:
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise TypeError("CreatedAt must be a datetime")

        # must always be timezone-aware
        if self.value.tzinfo is None:
            raise ValueError("CreatedAt must be timezone-aware")

    @classmethod
    def now(cls):
        return cls(datetime.now(timezone.utc))

    def to_epoch(self) -> int:
        return int(self.value.timestamp())
