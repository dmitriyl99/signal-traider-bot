from dotenv import load_dotenv
import os

result = load_dotenv(os.path.join(os.getcwd(), '.env'))


class Config:
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str
    PAYMENT_PROVIDERS: list

    CLICK_PAYMENT_PROVIDER_TOKEN: str
    PAYME_PAYMENT_PROVIDER_TOKEN: str

    def __init__(self):
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.PAYMENT_PROVIDERS = os.getenv('PAYMENT_PROVIDERS').split(',')
        self.CLICK_PAYMENT_PROVIDER_TOKEN = os.getenv('CLICK_PAYMENT_PROVIDER_TOKEN')
        self.PAYME_PAYMENT_PROVIDER_TOKEN = os.getenv('PAYME_PAYMENT_PROVIDER_TOKEN')


config = Config()
