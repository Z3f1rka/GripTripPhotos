from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    ACCESS_TOKEN_LT: int
    REFRESH_TOKEN_LT: int
    JWT_SECRET_KEY: str
    ENCRYPT_ALG: str
    API_HOST: str
    MAIN_API: str
    API_PORT: int
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
