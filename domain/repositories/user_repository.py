from abc import ABC, abstractmethod
from typing import Optional, List
from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.entities.user import User


class UserRepository(ABC):
    
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    
    @abstractmethod
    def get(self, user_id: UserId) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: Username) -> Optional[User]:
        pass
    
    @abstractmethod
    def exists(self, user_id: UserId) -> bool:
        pass
    
    @abstractmethod
    def exists_by_username(self, username: Username) -> bool:
        pass
    
    @abstractmethod
    def delete(self, user_id: UserId) -> None:
        pass