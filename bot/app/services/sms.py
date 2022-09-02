from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance

from app.config import config


def _configure_client() -> Client:
    return Client(
        config.TWILIO_ACCOUNT_SID,
        config.TWILIO_AUTH_TOKEN
    )


def send_sms(phone: str, text: str) -> MessageInstance:
    client = _configure_client()

    message = client.messages.create(
        body=text,
        from_=config.TWILIO_PHONE_NUMBER,
        to=phone
    )

    return message
