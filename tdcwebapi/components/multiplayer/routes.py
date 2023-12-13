from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from tdcwebapi.components.multiplayer.connection_manager import ConnectionManager
from tdcwebapi.components.multiplayer.message_queue import MessageQueueSingleton
from tdcwebapi.logger import logger


router = APIRouter(
    prefix="/multiplayer",
    tags=["multiplayer"]
)
queue = MessageQueueSingleton()
connection_manager = ConnectionManager()


@router.websocket("/", name="Websocket")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)

    try:
        while True:
            message = await queue.messages.get()
            await connection_manager.broadcast_message_to_other(websocket, message)

    except (ConnectionClosedOK, ConnectionClosedError, WebSocketDisconnect):
        connection_manager.disconnect(websocket)
