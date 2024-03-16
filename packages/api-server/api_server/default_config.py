# pylint: disable=line-too-long
config = {
    # ip or hostname to bind the socket to, this only applies when running the server in
    # standalone mode.
    "host": "127.0.0.1",
    # "host": "10.7.11.9",
    # port to bind to, this only applies when running the server in standalone mode.
    "port": 8000,
    "db_url": "mysql+pymysql://root:tannhatamr@127.0.0.1:3306/amrvdmdatabase",
    # url that rmf-server is being served on.
    # When being a proxy, this must be the url that rmf-server is mounted on.
    # E.g. https://example.com/rmf/api/v1
    "public_url": "http://localhost:8000",
    # "public_url": "http://10.7.11.9:8000",
    "cache_directory": "run/cache",  # The directory where cached files should be stored.
    "log_level": "WARNING",  # https://docs.python.org/3.8/library/logging.html#levels
    # a user that is automatically given admin privileges, note that this does not guarantee that the user exists in the identity provider.
    "builtin_admin": "admin",
    # path to a PEM encoded RSA public key which is used to verify JWT tokens, if the path is relative, it is based on the working dir.
    "jwt_public_key": None,
    # "jwt_public_key": "/home/tannhat/nhat_ws/monorepo/rmf-web/packages/api-server/jwt-key/keycloak-public.key",
    # url to the oidc endpoint, used to authenticate rest requests, it should point to the well known endpoint, e.g.
    # http://localhost:8080/auth/realms/rmf-web/.well-known/openid-configuration.
    # NOTE: This is ONLY used for documentation purposes, the "jwt_public_key" will be the
    # only key used to verify a token.
    "oidc_url": None,
    # "oidc_url": "http://localhost:8080/realms/rmf-web/.well-known/openid-configuration",
    # "oidc_url": "http://10.7.11.9:8080/realms/rmf-web/.well-known/openid-configuration",
    # Audience the access token is meant for. Can also be an array.
    # Used to verify the "aud" claim.
    # "aud": "rmf_api_server",
    "aud": "account",
    # url or string that identifies the entity that issued the jwt token
    # Used to verify the "iss" claim
    # If iss is set to None, it means that authentication should be disabled
    "iss": None,
    # "iss": "http://localhost:8080/realms/rmf-web",
    # "iss": "http://10.7.11.9:8080/realms/rmf-web",
    # list of arguments passed to the ros node, "--ros-args" is automatically prepended to the list.
    # e.g.
    #   Run with sim time: ["-p", "use_sim_time:=true"]
    "ros_args": [],
}
