from typing import Any

from fastapi import WebSocket

from tdcwebapi.components.security.abstract import AbstractSecurity
from tdcwebapi.logger import logger


class NoAuthSecurity(AbstractSecurity):

    def __init__(self):
        logger.warning("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !")
        logger.warning("! No authentication, DONT USE IN PRODUCTION !")
        logger.warning("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !")

    def http(self) -> Any:
        return ""

    async def validate_websocket(self, websocket: WebSocket) -> bool:
        return True
