import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from tdcwebapi.security.token_verifier import TokenVerifier, UnauthorizedException, UnauthenticatedException


router = APIRouter(
    prefix="/multiplayer",
    tags=["multiplayer"]
)


@router.websocket("/", name="Websocket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    token = await websocket.receive_text()
    try:
        await TokenVerifier().verify_token(token)

    except UnauthenticatedException:
        await websocket.send_text("No token provided")
        await websocket.close()
        return

    except UnauthorizedException as error:
        await websocket.send_text(f"Authentication failed: {str(error)}")
        await websocket.close()
        return

    await websocket.send_text("Authentication OK")

    try:
        while True:
            await asyncio.sleep(1)
            # TODO : work here

    except (ConnectionClosedOK, ConnectionClosedError, WebSocketDisconnect):
        pass
