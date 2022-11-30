import logging

from eskiz_sms import EskizSMS
from twilio.rest import Client

from app.config import config


def _configure_client_eskiz() -> EskizSMS:
    return EskizSMS(email=config.ESKIZ_EMAIL, password=config.ESKIZ_PASSWORD)


def _configure_client_twilio() -> Client:
    return Client(
        config.TWILIO_ACCOUNT_SID,
        config.TWILIO_AUTH_TOKEN
    )


def send_sms(phone: str, text: str):
    if phone.startswith('998') or phone.startswith('+998'):
        phone = phone.replace('+', '')
        client = _configure_client_eskiz()
        try:
            client.send_sms(phone, text, from_whom=config.SMS_FROM_WHOM, callback_url=None)
        except Exception as e:
            logging.error(f'Error while sending sms via eskiz to {phone}')
            raise e
    else:
        client = _configure_client_twilio()
        try:
            client.messages.create(
                body=text,
                from_=config.TWILIO_PHONE_NUMBER,
                to=phone
            )
        except Exception as e:
            logging.error(f'Error while sending sms via Twilio to {phone}')
            raise e
