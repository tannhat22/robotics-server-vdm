from typing import Any, Callable, Coroutine, Optional, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OpenIdConnect

from .app_config import app_config
from .logger import logger
# from .models import User
from .schemas import User, Role
from api_server.repositories import UserRepository



class AuthenticationError(Exception):
    pass


class JwtAuthenticator:
    def __init__(self, pem_file: str, aud: str, iss: str, *, oidc_url: str = "", client_id: str = ""):
        """
        Authenticates with a JWT token, the client must send an auth params with
        a "token" key.
        :param pem_file: path to a pem encoded certificate used to verify a token.
        """
        self.aud = aud
        self.iss = iss
        self.oidc_url = oidc_url
        self.client_id = client_id
        with open(pem_file, "r", encoding="utf8") as f:
            self._public_key = f.read()

    async def _get_user(self, claims: dict) -> User:
        if not "preferred_username" in claims:
            raise AuthenticationError(
                "expected 'preferred_username' username claim to be present"
            )
        try:
            rolesRaw = claims.get("resource_access", {}).get(self.client_id, {}).get("roles", [])
            roles = []
            isAdmin = False
            for role in rolesRaw:
                if role == "administrator":
                    isAdmin = True
                else:
                    roles.append(Role(name=role))

            user = User(
                id=claims.get("sub"),
                username=claims.get("preferred_username"),
                email=claims.get("email"),
                first_name=claims.get("given_name"),
                last_name=claims.get("family_name"),
                is_admin=isAdmin,
                roles=roles
            )
            UserRepository.get_or_create_user(user)
            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e), # "Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def verify_token(self, token: Optional[str]) -> User:
        if not token:
            raise AuthenticationError("authentication required")
        try:
            claims = jwt.decode(
                token,
                self._public_key,
                algorithms=["RS256"],
                audience=self.aud,
                issuer=self.iss,
            )
            return await self._get_user(claims)
        except jwt.InvalidTokenError as e:
            raise AuthenticationError(str(e)) from e

    def fastapi_dep(self) -> Callable[..., Union[Coroutine[Any, Any, User], User]]:
        async def dep(
            auth_header: str = Depends(OpenIdConnect(openIdConnectUrl=self.oidc_url)),
        ):
            parts = auth_header.split(" ")
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise HTTPException(401, "invalid bearer format")
            try:
                return await self.verify_token(parts[1])
            except AuthenticationError as e:
                raise HTTPException(401, str(e)) from e

        return dep


class StubAuthenticator(JwtAuthenticator):
    def __init__(self):  # pylint: disable=super-init-not-called
        self._user = User(username="stub", is_admin=True)

    async def verify_token(self, token: Optional[str]) -> User:
        return self._user

    def fastapi_dep(self) -> Callable[..., Union[Coroutine[Any, Any, User], User]]:
        return lambda: self._user


if app_config.jwt_public_key:
    if app_config.iss is None:
        raise ValueError("iss is required")
    authenticator = JwtAuthenticator(
        app_config.jwt_public_key,
        app_config.aud,
        app_config.iss,
        oidc_url=app_config.oidc_url or "",
        client_id=app_config.client_id,
    )
else:
    authenticator = StubAuthenticator()
    logger.warning("authentication is disabled")

user_dep = authenticator.fastapi_dep()
