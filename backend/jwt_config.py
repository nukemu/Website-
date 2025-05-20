from authx import AuthX, AuthXConfig


config = AuthXConfig()
config.JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
config.JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_SECRET_KEY = "RUSLAN_INPUT_YOURE_SECRET_KEY"
# config.JWT_COOKIE_CSRF_PROTECT = True
# config.JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
config.JWT_COOKIE_CSRF_PROTECT = False
# config.JWT_ACCESS_TOKEN_EXPIRES = 3600

security = AuthX(
    config=config,
)
