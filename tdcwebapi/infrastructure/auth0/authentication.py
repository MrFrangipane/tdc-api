import json
import logging
from functools import cache
from typing import Optional
from urllib.request import Request, urlopen

import jwt
from fastapi import Depends, Security
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from tdcwebapi.components.authentication.abstract import AbstractAuthentication
from tdcwebapi.components.authentication.exceptions import UnauthenticatedException, UnauthorizedException
from tdcwebapi.components.users.model import User
from tdcwebapi.infrastructure.auth0.settings import get_settings


_logger = logging.getLogger(__name__)


class Auth0(AbstractAuthentication):
    def __init__(self):
        _logger.info("Auth0 Authentication")
        self._config = get_settings()
        self._user_provider_url = None

        jwks_url = f'https://{self._config.auth0_domain}/.well-known/jwks.json'
        self._jwks_client = jwt.PyJWKClient(jwks_url)

    def for_request(self) -> User:
        return Security(self._verify_http)

    @cache
    def user_from_token(self, token: str) -> User:
        if self._user_provider_url is None:
            raise UnauthenticatedException()

        headers = {"Authorization": f"Bearer {token}"}
        user_data = json.loads(urlopen(Request(
            url=self._user_provider_url,
            headers=headers
        )).read().decode())

        user = User(
            id=user_data['sub'],
            name=user_data['name']
        )

        return user

    async def validate_token(self, token: str) -> bool:
        await self._verify_token(token)
        return True

    async def _verify_token(self, token: str) -> User:
        if token is None:
            raise UnauthenticatedException

        try:
            signing_key = self._jwks_client.get_signing_key_from_jwt(token).key

        except (jwt.exceptions.PyJWKClientError, jwt.exceptions.DecodeError) as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=self._config.auth0_algorithms,
                audience=self._config.auth0_api_audience,
                issuer=f"https://{self._config.auth0_domain}/"
            )
            self._user_provider_url = payload['aud'][1]
        except Exception as error:
            raise UnauthorizedException(str(error))

        return self.user_from_token(token)

    async def _verify_http(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
    ) -> User:
        """Verifies the token. Used by fastapi.security.Security Depends"""
        return await self._verify_token(token.credentials)
