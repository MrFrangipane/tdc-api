from typing import Optional

from fastapi import Depends
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
import jwt

from tdcwebapi.security.settings import get_settings
from tdcwebapi.security.exceptions import UnauthorizedException, UnauthenticatedException


class TokenVerifier:
    """Does all the token verification using PyJWT"""

    def __init__(self):
        self._config = get_settings()

        jwks_url = f'https://{self._config.auth0_domain}/.well-known/jwks.json'
        self._jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify_token(self, token: str):
        """Verifies the given token"""
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
        except Exception as error:
            raise UnauthorizedException(str(error))

        return payload

    async def verify_http(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
    ):
        """Verifies the token. Used by fastapi.security.Security Depends"""
        return await self.verify_token(token.credentials)
