import logging
from typing import Any

from fastapi import WebSocket

from tdcwebapi.components.security.abstract import AbstractSecurity


_logger = logging.getLogger(__name__)


class NoAuthSecurity(AbstractSecurity):

    def __init__(self):
        _logger.warning("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !")
        _logger.warning("! No authentication, DONT USE IN PRODUCTION !")
        _logger.warning("! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !")

    def http(self) -> Any:
        return ""

    async def validate_websocket(self, websocket: WebSocket) -> bool:
        return True
