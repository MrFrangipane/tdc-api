from fastapi import WebSocket

from tdcwebapi.components.multiplayer.message_queue import MessageQueueSingleton
from tdcwebapi.components.security import api as security
from tdcwebapi.logger import logger


class ConnectionManager:
    def __init__(self):
        self._queue = MessageQueueSingleton()
        self._websockets: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        logger.info(f"New connection WebSocket id={id(websocket)}")

        if await security.validate_websocket(websocket):
            logger.info(f"New connection validated")
            self._websockets.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self._websockets.remove(websocket)

    async def broadcast_message_to_other(self, websocket_sender: WebSocket, message: str):
        logger.info(
            f'Broadcasting message="{message}" from WebSocket id={id(websocket_sender)} to {len(self._websockets) - 1} clients'
        )
        for websocket in self._websockets:
            if websocket != websocket_sender:
                await websocket.send_text(message)
