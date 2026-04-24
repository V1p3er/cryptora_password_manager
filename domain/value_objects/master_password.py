import re
from dataclasses import dataclass

# immutable class using frozen=True parameter from dataclass
@dataclass(frozen=True)
class MasterPassword:
    
    value:str

    # post init validations
    def __post_init__(self):
        
        if not isinstance(self.value, str):
            raise TypeError("master password should be string")
        
        if len(self.value) < 12:
            raise ValueError("master password should be at least 12 characters")
        
        if not re.search(r"[0-9]", self.value):
            raise ValueError("master password should contain at least one number")

        if not re.search(r"[a-z]", self.value):
            raise ValueError("master password should contain at least one lowercase character")

        if not re.search(r"[A-Z]", self.value):
            raise ValueError("master password should contain at least one uppercase character")
        
        if not re.search(r"[^a-zA-Z0-9]", self.value):
            raise ValueError("master password should contain at least one special character")