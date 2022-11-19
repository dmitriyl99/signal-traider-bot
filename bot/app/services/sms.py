from eskiz_sms import EskizSMS

from app.config import config


def _configure_client() -> EskizSMS:
    return EskizSMS(email=config.ESKIZ_EMAIL, password=config.ESKIZ_PASSWORD)


def send_sms(phone: str, text: str):
    client = _configure_client()
    client.send_sms(phone, text, from_whom=config.SMS_FROM_WHOM, callback_url=None)
