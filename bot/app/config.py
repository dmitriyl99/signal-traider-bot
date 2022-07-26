from dotenv import load_dotenv
import os

result = load_dotenv(os.path.join(os.getcwd(), '.env'))


class Config:
    ENV: str

    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str
    PAYMENT_PROVIDERS: list

    CLICK_PAYMENT_PROVIDER_TOKEN: str
    PAYME_PAYMENT_PROVIDER_TOKEN: str

    WEBHOOK_PORT: int
    WEBHOOK_TOKEN: str

    def __init__(self):
        self.ENV = os.getenv('ENV')
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.PAYMENT_PROVIDERS = os.getenv('PAYMENT_PROVIDERS').split(',')
        self.CLICK_PAYMENT_PROVIDER_TOKEN = os.getenv('CLICK_PAYMENT_PROVIDER_TOKEN')
        self.PAYME_PAYMENT_PROVIDER_TOKEN = os.getenv('PAYME_PAYMENT_PROVIDER_TOKEN')
        self.WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT'))
        self.WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')


config = Config()
