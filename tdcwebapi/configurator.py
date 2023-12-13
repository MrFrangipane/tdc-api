import os

from tdcwebapi.configuration_singleton import ConfigurationSingleton
from tdcwebapi.infrastructure.auth0.security import Auth0Security
from tdcwebapi.infrastructure.no_auth_security import NoAuthSecurity


if os.environ.get('NO_AUTH', default="") == "1":
    ConfigurationSingleton().security = NoAuthSecurity()
else:
    ConfigurationSingleton().security = Auth0Security()
