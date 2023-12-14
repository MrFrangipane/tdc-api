from typing import Any

from tdcwebapi.components.users.model import User
from tdcwebapi.configuration_singleton import ConfigurationSingleton


def for_request():  # FIXME return a callable ? (to avoid 'NoneType' object has no attribute 'http')
    """Used in routes signatures to provide authentication and User

    ````python
    from tdcwebapi.components.authentication import api as authentication
    from tdcwebapi.components.users.model import User

    @router.post("/")
    async def get(user: User = authentication.for_request()) -> Something:
        pass
    ````"""
    return ConfigurationSingleton().authentication.for_request()


def user_from_token(token: str) -> User:
    """Used to retrieve User object from Authorization service

    ````python
    from tdcwebapi.components.authentication import api as authentication
    from tdcwebapi.components.user.model import User

    @router.websocket("", name="Websocket")  # don't use "/" for path
    async def websocket_endpoint(websocket: WebSocket, token: str) -> None:
        try:
            await security.validate_token(token)
        except (UnauthorizedException, UnauthenticatedException):
            logger.info(f"New connection validated")
            return

        user = authentication.user_from_token(token)
        await connection_manager.connect(websocket, user)
    ````"""
    return ConfigurationSingleton().authentication.user_from_token(token)


async def validate_token(token: str) -> Any:
    """Used to validate token outside routes (i.e. WebSocket)

    ````python
    from tdcwebapi.components.security import api as security
    from tdcwebapi.components.user.model import User

    @router.websocket("", name="Websocket")  # don't use "/" for path
    async def websocket_endpoint(websocket: WebSocket, token: str) -> None:
        try:
            await security.validate_token(token)
        except (UnauthorizedException, UnauthenticatedException):
            logger.info(f"New connection validated")
            return

        user = security.user_from_token(token)
        await connection_manager.connect(websocket, user)
    ````"""
    return await ConfigurationSingleton().authentication.validate_token(token)
