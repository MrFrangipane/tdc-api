import logging
from typing import Any

from fastapi import Security, WebSocket

from tdcwebapi.components.security.abstract import AbstractSecurity
from tdcwebapi.components.security.exceptions import UnauthenticatedException, UnauthorizedException
from tdcwebapi.infrastructure.auth0.token_verifier import TokenVerifier


_logger = logging.getLogger(__name__)


class Auth0Security(AbstractSecurity):
    def __init__(self):
        _logger.info("Auth0 Authentication")
        self._token_verifier = TokenVerifier()

    def http(self) -> Any:
        return Security(self._token_verifier.verify_http)

    async def validate_websocket(self, websocket: WebSocket) -> bool:
        token = await websocket.receive_text()
        try:
            await self._token_verifier.verify_token(token)

        except UnauthenticatedException:
            await websocket.send_text("No token provided")
            await websocket.close()
            return False

        except UnauthorizedException as error:
            await websocket.send_text(f"Authentication failed: {str(error)}")
            await websocket.close()
            return False

        await websocket.send_text("Authentication OK")
        return True
