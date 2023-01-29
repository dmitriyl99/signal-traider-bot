import logging

import requests
from requests.auth import HTTPBasicAuth

from app.config import settings


class CloudPaymentApi:
    session: requests.Session

    host: str

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(settings.cloud_payments_public_id, settings.cloud_payments_password)
        self.host = settings.cloud_payments_host

    def test_connection(self):
        response = self._persist_get_request('test')
        if response.status_code == 200 and response.json()['Success'] is True:
            return True
        return False

    def post_3d_secure(self, transaction_id: str, pa_res: str):
        payload = {
            'TransactionId': transaction_id,
            'PaRes': pa_res
        }
        response = self._persist_post_request('payments/cards/post3ds', payload)
        response_data = response.json()
        if response_data['Success']:
            return {
                'status': 'success'
            }
        return {
            'status': 'rejected',
            'data': {
                'reason_code': response_data['ReasonCode'],
                'reason': response_data['Reason'],
                'message': response_data['CardHolderMessage']
            }
        }

    def _persist_get_request(self, path: str, params: dict = None) -> requests.Response:
        return self.session.get(f"{self.host}/{path}", params=params)

    def _persist_post_request(self, path: str, payload: dict = None) -> requests.Response:
        return self.session.post(f"{self.host}/{path}", json=payload)
