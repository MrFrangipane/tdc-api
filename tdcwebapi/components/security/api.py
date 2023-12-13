from fastapi import WebSocket

from tdcwebapi.configuration_singleton import ConfigurationSingleton


def http():  # FIXME return a callable ? (to avoid 'NoneType' object has no attribute 'http')
    return ConfigurationSingleton().security.http()


async def validate_websocket(websocket: WebSocket) -> bool:
    return await ConfigurationSingleton().security.validate_websocket(websocket)
