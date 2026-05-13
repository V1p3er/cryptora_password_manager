import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServiceName:

    value: str

    def __post_init__(self):

        if not isinstance(self.value, str):
            raise TypeError("Service name should be string")
        
        normalized = self.value.strip().casefold()

        if not normalized:
            raise ValueError("Service name cannot be empty")
        
        if re.search(r"[^a-zA-Z0-9_.-]", normalized):
            raise ValueError("Cannot use special characters for service name!")

        length = len(normalized)
        if length > 24:
            raise ValueError("service name is too long")
        
        if length < 3: 
            raise ValueError("service name is too short")
        object.__setattr__(self, "value", normalized)
    
    def __str__(self) -> str:
        return self.value
