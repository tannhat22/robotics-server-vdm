from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID # pip require python-keycloak
from fastapi import Security, HTTPException, status,Depends
# from pydantic import Json

from .app_config import app_config
from .schemas import User, Role
from api_server.repositories import UserRepository

class KeycloakConfig:
    def __init__(self, pem_file: str, server_url: str, realm: str, client_id: str, client_secret: str = ""):
        """
        Authenticates with a JWT token, the client must send an auth params with
        a "token" key.
        :param pem_file: path to a pem encoded certificate used to verify a token.
        """
        self.server_url = server_url
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_url = f"http://localhost:8080/realms/{self.realm}/protocol/openid-connect/auth"
        self.token_url = f"http://localhost:8080/realms/{self.realm}/protocol/openid-connect/token"
        with open(pem_file, "r", encoding="utf8") as f:
            self._public_key = f.read()

keycloakConfig = KeycloakConfig(
    pem_file=app_config.jwt_public_key,
    server_url=app_config.server_keycloak_url,
    realm=app_config.realm,
    client_id=app_config.client_id,
    client_secret=app_config.client_secret
)


# This is used for fastapi docs authentification
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=keycloakConfig.authorization_url, # https://sso.example.com/auth/
    tokenUrl=keycloakConfig.token_url, # https://sso.example.com/auth/realms/example-realm/protocol/openid-connect/token
)

# This actually does the auth checks
# client_secret_key is not mandatory if the client is public on keycloak
keycloak_openid = KeycloakOpenID(
    server_url=keycloakConfig.server_url, # https://sso.example.com/auth/
    client_id=keycloakConfig.client_id, # backend-client-id
    realm_name=keycloakConfig.realm, # example-realm
    client_secret_key=keycloakConfig.client_secret, # your backend client secret
    verify=True
)

async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

# Get the payload/token from keycloak
async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    # if token is None:
    #     token = Security(oauth2_scheme)
    try:
        return keycloak_openid.decode_token(
            token,
            key= await get_idp_public_key(),
            # key=keycloakConfig._public_key,
            options={
                "verify_signature": True,
                "verify_aud": False,
                "exp": True
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
# Get user infos from the payload
async def get_user_info( payload: dict = Depends(get_payload)) -> User:
    try:
        rolesRaw = payload.get("resource_access", {}).get(keycloakConfig.client_id, {}).get("roles", [])
        roles = []
        isAdmin = False
        for role in rolesRaw:
            if role == "administrator":
                isAdmin = True
            else:
                roles.append(Role(name=role))

        user = User(
            id=payload.get("sub"),
            username=payload.get("preferred_username"),
            email=payload.get("email"),
            first_name=payload.get("given_name"),
            last_name=payload.get("family_name"),
            is_admin=isAdmin,
            roles=roles
        )
        # UserBase(
        #     id=payload.get("sub"),
        #     username=payload.get("preferred_username"),
        #     email=payload.get("email"),
        #     first_name=payload.get("given_name"),
        #     last_name=payload.get("family_name"),
        #     # realm_roles=payload.get("realm_access", {}).get("roles", []),
        #     # client_roles=payload.get("resource_access", {}).get(keycloakConfig.client_id, {}).get("roles", []),
        #     # roles= listRole
        # )
        UserRepository.get_or_create_user(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e), # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )