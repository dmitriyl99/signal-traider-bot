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
    telegram_group_id: str

    click_secret_key: str
    click_service_id: int

    redis_host: str
    redis_port: int

    amocrm_client_id: str
    amocrm_secret_key: str
    amocrm_authorization_code: str
    amocrm_redirect_uri: str


class CsrfSettings(BaseSettings):
    secret_key: str


settings = Settings()
