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

    click_secret_key: str
    click_service_id: int

    cloud_payments_public_id: str
    cloud_payments_password: str
    cloud_payments_host: str

    redis_host: str
    redis_port: int


class CsrfSettings(BaseSettings):
    secret_key: str


settings = Settings()
