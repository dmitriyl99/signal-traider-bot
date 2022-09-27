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

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str

    REDIS_HOST: str

    MASSPAY_HOST: str

    def __init__(self):
        self.ENV = os.getenv('ENV')
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.PAYMENT_PROVIDERS = os.getenv('PAYMENT_PROVIDERS').split(',')
        self.CLICK_PAYMENT_PROVIDER_TOKEN = os.getenv('CLICK_PAYMENT_PROVIDER_TOKEN')
        self.PAYME_PAYMENT_PROVIDER_TOKEN = os.getenv('PAYME_PAYMENT_PROVIDER_TOKEN')
        self.WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT'))
        self.WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
        self.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
        self.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
        self.TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
        self.REDIS_HOST = os.getenv('REDIS_HOST')
        self.MASSPAY_HOST = os.getenv('MASSPAY_HOST')


config = Config()
