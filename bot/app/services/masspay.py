import requests
import logging
from typing import Optional

from app.config import config


class CheckHashCommandResult:
    subscription_days: int
    user_phone_number: str

    def __init__(
            self,
            subscription_days: int,
            user_phone_number: str
    ):
        self.subscription_days = subscription_days
        self.user_phone_number = user_phone_number


def check_hash_command(hash_command: str) -> Optional[CheckHashCommandResult]:
    payload = {
        'hash': hash_command
    }
    response = requests.post(f'{config.MASSPAY_HOST}/order/activate', json=payload)
    if response.status_code not in [200, 202]:
        logging.error(f'Error while requesting HASH command {hash_command}. Status code: f{response.status_code}, Content: f{response.content}')
        return None

    response_data = response.json()
    if 'course' in response_data:
        return CheckHashCommandResult(
            subscription_days=response_data['course']['vip_signal_subscription'],
            user_phone_number=str(response_data['accaunt']['user_tel'])
        )
    return None
