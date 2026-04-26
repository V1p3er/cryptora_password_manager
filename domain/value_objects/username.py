import re
from dataclasses import dataclass

_CORRECT_PATTERN = re.compile(r"^[a-zA-Z0-9._-]+$")

@dataclass(frozen=True)
class Username:

    value: str

    def __post_init__(self):
        
        if not isinstance(self.value, str):
            raise TypeError("Username should be string!")
        
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("Username cannot be empty")


        if len(normalized) < 5:
            raise ValueError("Username should be at least 5 characters")
        

        if len(normalized) > 32:
            raise ValueError("Username should be at most 32 characters")
        

        if not _CORRECT_PATTERN.match(normalized):
            raise ValueError("Username cannot contain special characters")
        

        object.__setattr__(self, "value", normalized)
    
    def __str__(self) -> str:
        return self.value