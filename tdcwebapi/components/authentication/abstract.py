from abc import ABC, abstractmethod

from tdcwebapi.components.users.model import User


class AbstractAuthentication(ABC):

    @abstractmethod
    def for_request(self) -> User:
        pass

    @abstractmethod
    def user_from_token(self, token: str) -> User:
        pass

    @abstractmethod
    async def validate_token(self, token: str) -> bool:
        pass
