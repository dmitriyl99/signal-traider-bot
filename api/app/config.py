import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_ttl: int

    database_url: str

    telegram_bot_api_domain: str
    telegram_bot_api_token: str

    redis_host: str
    redis_port: int


settings = Settings()
