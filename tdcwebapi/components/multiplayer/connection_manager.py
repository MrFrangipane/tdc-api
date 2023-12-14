from fastapi import WebSocket

from tdcwebapi.components.multiplayer.message_queue import MessageQueueSingleton
from tdcwebapi.components.users.model import User
from tdcwebapi.logger import logger


class ConnectionManager:
    def __init__(self):
        self._queue = MessageQueueSingleton()
        self._websockets: list[WebSocket] = []
        self._users: dict[WebSocket, User] = {}

    async def connect(self, websocket: WebSocket, user: User) -> None:
        await websocket.accept()
        logger.info(f"New connection WebSocket id={id(websocket)}")
        self._websockets.append(websocket)
        self._users[websocket] = user

    def disconnect(self, websocket: WebSocket):
        logger.info(f"Disconnected WebSocket id={id(websocket)}")
        self._websockets.remove(websocket)

    async def broadcast_message_to_other(self, websocket_sender: WebSocket, message: str):
        logger.info(
            f'Broadcasting message="{message}" '
            f'from User<{self._users[websocket_sender].name}> '
            f'to {len(self._websockets) - 1} clients'
        )
        for websocket in self._websockets:
            if websocket != websocket_sender:
                await websocket.send_text(message)
