import hashlib
import logging

from typing import Optional

from app.config import settings
from app.data.db.payments_repository import PaymentsRepository
from app.data.models.payments import PaymentStatus


class ClickPaymentHandler:
    payments_repository: PaymentsRepository

    def __init__(self, payments_repository: PaymentsRepository):
        self.payments_repository = payments_repository

    async def handle(self, merchant_trans_id: str | None,
                     click_trans_id: Optional[str],
                     amount: Optional[str],
                     action: Optional[str],
                     error: Optional[str],
                     sign_time: Optional[str],
                     sign_string: Optional[str],
                     merchant_prepare_id: Optional[str], payment_repository: PaymentsRepository):
        merchant_prepare_id = merchant_prepare_id if action is not None and action == '1' else ''
        my_sign_string = '{}{}{}{}{}{}{}'.format(
            click_trans_id, settings.click_service_id, settings.click_secret_key, merchant_trans_id,
            amount, action, sign_time
        )
        logging.info('My sign string params {} {} {} {} {} {} {}'.format(
            click_trans_id, settings.click_service_id, settings.click_secret_key, merchant_trans_id,
            amount, action, sign_time
        ))
        encoder = hashlib.md5(my_sign_string.encode('utf-8'))
        my_sign_string = encoder.hexdigest()
        logging.info(f'Sign Strings: {sign_string} + {my_sign_string}')
        if my_sign_string != sign_string:
            return {
                'error': '-1',
                'error_note': 'SIGN CHECK FAILED!'
            }
        if action not in ['0', '1']:
            return {
                'error': '-3',
                'error_note': 'Action not found'
            }
        payment = await payment_repository.get_payment_by_id(int(merchant_trans_id))
        if not payment:
            return {
                'error': '-5',
                'error_note': 'Payment not found'
            }

        if abs(float(amount) * 100 - float(payment.amount) > 0.01):
            return {
                'error': '-2',
                'error_note': 'Incorrect parameter amount'
            }

        if payment.status == PaymentStatus.CONFIRMED:
            return {
                'error': '-4',
                'error_note': 'Already paid'
            }

        if action == '1':
            if merchant_trans_id != merchant_prepare_id:
                return {
                    'error': '-6',
                    'error_note': 'Transaction not found'
                }
        if payment.status == PaymentStatus.REJECTED or int(error) < 0:
            return {
                'error': '-9',
                'error_note': 'Transaction cancelled'
            }

        return {
            'error': '0',
            'error_note': 'Success'
        }
