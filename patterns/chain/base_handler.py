# patterns/chain/base_handler.py

from abc import ABC, abstractmethod
from fastapi import HTTPException


class BaseAccessHandler(ABC):
    def __init__(self, successor=None):
        self.successor = successor

    @abstractmethod
    def can_handle(self, user, reservation) -> bool:
        pass

    def handle(self, user, reservation):
        if self.can_handle(user, reservation):
            return True
        elif self.successor:
            return self.successor.handle(user, reservation)
        else:
            raise HTTPException(
                status_code=403, detail="You are not authorized to perform this action."
            )
