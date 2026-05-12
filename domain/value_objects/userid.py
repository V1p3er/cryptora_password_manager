from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID

    def __post_init__(self):

        if self.value.version != 4:
            raise ValueError("UserId must be UUIDv4")

    def __str__(self) -> str:
        return str(self.value)