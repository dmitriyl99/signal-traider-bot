import logging
import json

from eskiz_sms import EskizSMS
from twilio.rest import Client
import requests

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
        sms = [{
            'phone': phone,
            'text': text
        }]
        data = {
            'login': config.SMS_LOGIN,
            'password': config.SMS_PASSWORD,
            'data': json.dumps(sms)
        }
        url = 'http://185.8.212.184/smsgateway/'
        try:
            response = requests.post(
                url,
                data=data,
                timeout=5,
                verify=False
            )
        except Exception as e:
            logging.error(f'Error while sending sms via getsms to {phone}')
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
