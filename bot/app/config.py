from dotenv import load_dotenv
import os

result = load_dotenv(os.path.join(os.getcwd(), '.env'))


class Config:
    ENV: str

    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str
    PAYMENT_PROVIDERS: list

    CLICK_PAYMENT_PROVIDER_TOKEN: str
    CLICK_SERVICE_ID: str
    CLICK_MERCHANT_ID: str
    CLICK_SECRET_KEY: str
    CLICK_MERCHANT_USER_ID: int

    PAYME_PAYMENT_PROVIDER_TOKEN: str
    PAYME_MERCHANT_ID: str
    PAYME_KEY: str
    PAYME_TEST_KEY: str

    CLOUD_PAYMENTS_PUBLIC_ID: str
    CLOUD_PAYMENTS_PASSWORD: str
    CLOUD_PAYMENTS_HOST: str

    WEBHOOK_PORT: int
    WEBHOOK_TOKEN: str

    ESKIZ_EMAIL: str
    ESKIZ_PASSWORD: str
    SMS_FROM_WHOM: str

    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str

    REDIS_HOST: str

    MASSPAY_HOST: str

    AMOCRM_CLIENT_ID: str
    AMOCRM_SECRET_KEY: str
    AMOCRM_AUTHORIZATION_CODE: str
    AMOCRM_REDIRECT_URI: str
    AMOCRM_SUBDOMAIN: str

    def __init__(self):
        self.ENV = os.getenv('ENV')
        self.TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.PAYMENT_PROVIDERS = os.getenv('PAYMENT_PROVIDERS').split(',')
        self.CLICK_PAYMENT_PROVIDER_TOKEN = os.getenv('CLICK_PAYMENT_PROVIDER_TOKEN')
        self.CLICK_SERVICE_ID = os.getenv('CLICK_SERVICE_ID')
        self.CLICK_MERCHANT_ID = os.getenv('CLICK_MERCHANT_ID')
        self.CLICK_SECRET_KEY = os.getenv('CLICK_SECRET_KEY')
        self.CLICK_MERCHANT_USER_ID = os.getenv('CLICK_MERCHANT_USER_ID')
        self.PAYME_PAYMENT_PROVIDER_TOKEN = os.getenv('PAYME_PAYMENT_PROVIDER_TOKEN')
        self.PAYME_MERCHANT_ID = os.getenv('PAYME_MERCHANT_ID')
        self.PAYME_KEY = os.getenv('PAYME_KEY')
        self.PAYME_TEST_KEY = os.getenv('PAYME_TEST_KEY')
        self.CLOUD_PAYMENTS_PUBLIC_ID = os.getenv('CLOUD_PAYMENTS_PUBLIC_ID')
        self.CLOUD_PAYMENTS_PASSWORD = os.getenv('CLOUD_PAYMENTS_PASSWORD')
        self.CLOUD_PAYMENTS_HOST = os.getenv('CLOUD_PAYMENTS_HOST')
        self.WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT'))
        self.WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
        self.ESKIZ_EMAIL = os.getenv('ESKIZ_EMAIL')
        self.ESKIZ_PASSWORD = os.getenv('ESKIZ_PASSWORD')
        self.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
        self.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
        self.TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
        self.SMS_FROM_WHOM = os.getenv('SMS_FROM_WHOM')
        self.REDIS_HOST = os.getenv('REDIS_HOST')
        self.MASSPAY_HOST = os.getenv('MASSPAY_HOST')
        self.AMOCRM_CLIENT_ID = os.getenv('AMOCRM_CLIENT_ID')
        self.AMOCRM_SECRET_KEY = os.getenv('AMOCRM_SECRET_KEY')
        self.AMOCRM_AUTHORIZATION_CODE = os.getenv('AMOCRM_AUTHORIZATION_CODE')
        self.AMOCRM_REDIRECT_URI = os.getenv('AMOCRM_REDIRECT_URI')
        self.AMOCRM_SUBDOMAIN = os.getenv('AMOCRM_SUBDOMAIN')


config = Config()
