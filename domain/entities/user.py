from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class User:

    user_id: UUID
    username: str
    password_hash: str

    @classmethod
    def create_user(cls, username: str, password_hash: str) -> "User":

        username = username.strip()

        if not username:
            raise ValueError("Username cannot be empty")
        
        if not password_hash:
            raise ValueError("Password hash cannot be empty")
        
        user_id = uuid4()

        return cls(
            user_id=user_id,
            username=username,
            password_hash=password_hash
        )
    
    def change_password(self, new_password_hash: str) -> None:

        if not new_password_hash:
            raise ValueError("New password hash cannot be empty")
        
        self.password_hash = new_password_hash
    
    def verify_password(self, password_hash: str) -> bool:
        
        return self.password_hash == password_hash