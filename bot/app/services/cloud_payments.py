import logging

import requests
from requests.auth import HTTPBasicAuth

from app.config import config


class CloudPaymentApi:
    session: requests.Session

    host: str

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(config.CLOUD_PAYMENTS_PUBLIC_ID, config.CLOUD_PAYMENTS_PASSWORD)
        self.host = config.CLOUD_PAYMENTS_HOST

    def test_connection(self):
        response = self._persist_get_request('test')
        if response.status_code == 200 and response.json()['Success'] is True:
            return True
        return False

    def charge(self, amount, currency, ip_address, card_cryptogram_packet, payment_id: int,
               card_holder_name=None) -> dict:
        payload = {
            'Amount': amount / 100,
            'Currency': currency if currency else 'UZS',
            'IpAddress': ip_address,
            'InvoiceId': payment_id,
            'CardCryptogramPacket': card_cryptogram_packet
        }
        if card_holder_name:
            payload['Name'] = card_holder_name
        logging.info('Sending payload to Cloud Payments: %r', payload)
        response = self._persist_post_request('payments/cards/charge', payload)
        response_data = response.json()
        logging.info(response_data)
        if response_data['Success'] is not True and response_data['Message']:
            logging.error('Error while getting charge in Cloud Payments service: %r', response_data['Message'])
        elif response_data['Success'] is not True and not response_data['Message']:
            if 'Model' in response_data:
                if 'AcsUrl' in response_data['Model']:
                    # Need 3-D Secure
                    acs_url = response_data['Model']['AcsUrl']
                    return {
                        'status': '3d_secure',
                        'data': {
                            'acs_url': acs_url,
                            'transaction_id': response_data['Model']['TransactionId'],
                            'pa_req': response_data['Model']['PaReq']
                        }
                    }
                elif 'ReasonCode' in response_data['Model']:
                    # The transaction was rejected
                    return {
                        'status': 'rejected',
                        'data': {
                            'reason_code': response_data['ReasonCode'],
                            'reason': response_data['Reason'],
                            'message': response_data['CardHolderMessage']
                        }
                    }
        elif response_data['Success']:
            return {
                'status': 'success'
            }

    def _persist_get_request(self, path: str, params: dict = None) -> requests.Response:
        return self.session.get(f"{self.host}/{path}", params=params)

    def _persist_post_request(self, path: str, payload: dict = None) -> requests.Response:
        return self.session.post(f"{self.host}/{path}", json=payload)
