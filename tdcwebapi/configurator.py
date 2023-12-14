import os

from tdcwebapi.configuration_singleton import ConfigurationSingleton
from tdcwebapi.infrastructure.auth0 import Auth0
from tdcwebapi.infrastructure.no_auth import NoAuth


if os.environ.get('NO_AUTH', default="") == "1":
    ConfigurationSingleton().authentication = NoAuth()
else:
    ConfigurationSingleton().authentication = Auth0()
