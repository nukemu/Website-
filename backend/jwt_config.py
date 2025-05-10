from authx import AuthX, AuthXConfig


config = AuthXConfig()
config.JWT_ACCESS_COOKIE_NAME = "my-access-cookie-name"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_SECRET_KEY = "RUSLAN_INPUT_YOURE_SECRET_KEY"

security = AuthX(config=config)
