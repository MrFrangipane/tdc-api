from typing import Any
from abc import ABC, abstractmethod

from fastapi import WebSocket


class AbstractSecurity(ABC):

    @abstractmethod
    def http(self) -> Any:
        """"""
        pass

    @abstractmethod
    async def validate_websocket(self, websocket: WebSocket) -> bool:
        pass
