import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from tdcwebapi.components.multiplayer.connection_manager import ConnectionManager
from tdcwebapi.components.multiplayer.message_queue import MessageQueueSingleton
from tdcwebapi.components.authentication import api as security
from tdcwebapi.components.authentication.exceptions import UnauthorizedException, UnauthenticatedException
from tdcwebapi.logger import logger


router = APIRouter(
    prefix="/multiplayer",
    tags=["multiplayer"]
)
queue = MessageQueueSingleton()
connection_manager = ConnectionManager()


# don't use "/" for path
# https://stackoverflow.com/questions/67020476/cannot-connect-to-to-fastapi-with-websocket-in-flutter-403-forbidden-code-100
@router.websocket("", name="Websocket")
async def websocket_endpoint(websocket: WebSocket, token: str) -> None:
    try:
        await security.validate_token(token)
    except (UnauthorizedException, UnauthenticatedException):
        logger.info(f"New connection validated")
        return

    user = security.user_from_token(token)
    await connection_manager.connect(websocket, user)

    try:
        while True:
            message = await queue.messages.get()
            await connection_manager.broadcast_message_to_other(websocket, message)

    except (ConnectionClosedOK, ConnectionClosedError, WebSocketDisconnect) as e:
        print(f"Connection closed due to {e}")
        connection_manager.disconnect(websocket)
