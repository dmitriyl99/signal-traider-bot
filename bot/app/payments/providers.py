import base64
import logging
import urllib.parse
import hashlib
import time

from app.config import config
import requests

from typing import List


class PaymentProvider:
    name: str
    provider_token: str

    def __init__(self, name: str, provider_token: str):
        self.name = name
        self.provider_token = provider_token

    def get_payment_url(self, amount, title, payment_id):
        pass

    def create_invoice(self, amount, phone, payment_id):
        pass


class PaymePaymentProvider(PaymentProvider):
    merchant_id: str
    key: str
    test_key: str

    def __init__(self, name: str, provider_token: str, merchant_id: str, key: str, test_key: str):
        super().__init__(name, provider_token)

        self.merchant_id = merchant_id
        self.key = key
        self.test_key = test_key

    def get_payment_url(self, amount, title, payment_id):
        if config.ENV == 'local':
            host = 'https://checkout.test.paycom.uz'
        else:
            host = 'https://checkout.paycom.uz'
        payload = {
            'm': self.merchant_id,
            'ac.order_id': payment_id,
            'a': amount,
            'ds.items.0.title': title,
            'ds.items.0.price': amount,
            'ds.items.0.count': 1
        }
        payload_str = ''
        for k, v in payload.items():
            payload_str += f'{k}={v}'
            if k != 'ds.items.0.count':
                payload_str += ';'
        payload_str_bytes = payload_str.encode('utf-8')
        payload_str_base64_bytes = base64.b64encode(payload_str_bytes)
        payload_str_base64_string = payload_str_base64_bytes.decode('utf-8')
        return f"{host}/{payload_str_base64_string}"


class ClickPaymentProvider(PaymentProvider):
    service_id: int
    merchant_id: int
    secret_key: str
    merchant_user_id: int

    def __init__(self, name: str, provider_token: str, service_id: int, merchant_id: int, secret_key: str,
                 merchant_user_id: int):
        super().__init__(name, provider_token)
        self.service_id = service_id
        self.merchant_id = merchant_id
        self.secret_key = secret_key
        self.merchant_user_id = merchant_user_id

    def get_payment_url(self, amount, title, payment_id):
        host = 'https://my.click.uz'
        schema = 'services/pay'
        payload = {
            'service_id': self.service_id,
            'merchant_id': self.merchant_id,
            'amount': amount,
            'transaction_param': payment_id
        }
        query_string = urllib.parse.urlencode(payload)
        return f"{host}/{schema}?{query_string}"

    def create_invoice(self, amount, phone, payment_id):
        timestamp = int(time.time())
        token = hashlib.sha1('{timestamp}{secret_key}'.format(
            timestamp=timestamp, secret_key=self.secret_key
        ).encode('utf-8')
                             ).hexdigest()
        headers = {
            'Auth': f"{self.merchant_id}:{token}:{timestamp}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = {
            'service_id': int(self.service_id),
            'amount': float(amount),
            'phone_number': phone,
            'merchant_trans_id': str(payment_id)
        }
        response = requests.post('https://api.click.uz/v2/merchant/invoice/create', json=payload, headers=headers)
        if response.status_code != 200:
            logging.error(
                f'Error while creating invoice in Click. Status code: {response.status_code}. Content: {response.content}')
            raise Exception('Error while creating invoice in Click')
        logging.info(f'Response from Click: {response.status_code} - {response.content}')


def get_payment_providers() -> List[PaymentProvider]:
    available_providers = config.PAYMENT_PROVIDERS
    providers = []
    if 'click' in available_providers:
        providers.append(ClickPaymentProvider(
            name='Click',
            provider_token=config.CLICK_PAYMENT_PROVIDER_TOKEN,
            service_id=config.CLICK_SERVICE_ID,
            merchant_id=config.CLICK_MERCHANT_ID,
            secret_key=config.CLICK_SECRET_KEY,
            merchant_user_id=config.CLICK_MERCHANT_USER_ID
        ))
    if 'payme' in available_providers:
        providers.append(PaymePaymentProvider(
            name='Payme',
            provider_token=config.PAYME_PAYMENT_PROVIDER_TOKEN,
            merchant_id=config.PAYME_MERCHANT_ID,
            key=config.PAYME_KEY,
            test_key=config.PAYME_TEST_KEY
        ))
    return providers


def get_payment_provider_by_name(name: str) -> PaymentProvider | None:
    providers = get_payment_providers()
    found_providers = list(filter(lambda provider: provider.name == name, providers))
    if len(found_providers) > 0:
        return found_providers[0]
    return None
