from typing import Any

from tdcwebapi.components.authentication.abstract import AbstractAuthentication
from tdcwebapi.components.users.model import User
from tdcwebapi.logger import logger


class NoAuth(AbstractAuthentication):

    def __init__(self):
        logger.warning("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !")
        logger.warning("! No authentication, DONT USE IN PRODUCTION !")
        logger.warning("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !")

    def for_request(self) -> Any:
        return ""

    async def validate_token(self, token: str) -> bool:
        return True

    def user_from_token(self, token: str) -> User:
        return User(id="12345678", name="NoAuth User")
