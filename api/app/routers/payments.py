import logging

from typing import Optional

from fastapi import APIRouter, Depends, Body, Form

from app.data.db.payments_repository import PaymentsRepository
from app.data.models.payments import PaymentStatus
from app.routers.forms.payments import ClickForm
from app.dependencies import get_payments_repository, get_current_user
from app.data.models.admin_users import AdminUser
from app.config import settings

import hashlib

router = APIRouter(prefix='/payments', tags=['Payments'])


async def check_click_webhook(merchant_trans_id: str | None,
                              click_trans_id: Optional[str],
                              service_id: Optional[str],
                              click_paydoc_id: Optional[str],
                              amount: Optional[str],
                              action: Optional[str],
                              error: Optional[str],
                              error_note: Optional[str],
                              sign_time: Optional[str],
                              sign_string: Optional[str],
                              merchant_prepare_id: Optional[str], payment_repository: PaymentsRepository):
    merchant_prepare_id = merchant_prepare_id if action is not None and action == '1' else ''
    my_sign_string = '{}{}{}{}{}{}{}{}'.format(
        click_trans_id, settings.click_service_id, settings.click_secret_key, merchant_trans_id,
        merchant_prepare_id, amount, action, sign_time
    )
    encoder = hashlib.md5(my_sign_string.encode('utf-8'))
    my_sign_string = encoder.hexdigest()
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

    if abs(float(amount) - float(payment.amount) > 0.01):
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


@router.get('/')
async def get_payments_list(
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    return await payment_repository.get_all_payment()


@router.post('/click/prepare')
async def click_prepare(
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        merchant_trans_id: str | None = Form(),
        click_trans_id: Optional[str] = Form(),
        service_id: Optional[str] = Form(),
        click_paydoc_id: Optional[str] = Form(),
        amount: Optional[str] = Form(),
        action: Optional[str] = Form(),
        error: Optional[str] = Form(),
        error_note: Optional[str] = Form(),
        sign_time: Optional[str] = Form(),
        sign_string: Optional[str] = Form(),
        merchant_prepare_id: Optional[str] = Form(None),
):
    payment_id = int(merchant_trans_id)
    result = await check_click_webhook(merchant_trans_id, click_trans_id, service_id, click_paydoc_id, amount, action,
                                       error, error_note, sign_time, sign_string, merchant_prepare_id,
                                       payment_repository)
    if result['error'] == '0':
        await payment_repository.set_payment_status(payment_id, PaymentStatus.WAITING)
    result['click_trans_id'] = click_trans_id
    result['merchant_trans_id'] = merchant_trans_id
    result['merchant_prepare_id'] = merchant_trans_id
    result['merchant_confirm_id'] = merchant_trans_id

    return result


@router.post('/click/complete')
async def click_complete(
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        merchant_trans_id: str | None = Form(),
        click_trans_id: Optional[str] = Form(),
        service_id: Optional[str] = Form(),
        click_paydoc_id: Optional[str] = Form(),
        amount: Optional[str] = Form(),
        action: Optional[str] = Form(),
        error: Optional[str] = Form(None),
        error_note: Optional[str] = Form(),
        sign_time: Optional[str] = Form(),
        sign_string: Optional[str] = Form(),
        merchant_prepare_id: Optional[str] = Form(None),
):
    payment_id = int(merchant_trans_id)
    result = await check_click_webhook(merchant_trans_id, click_trans_id, service_id, click_paydoc_id, amount, action,
                                       error, error_note, sign_time, sign_string, merchant_prepare_id,
                                       payment_repository)
    if error is not None and int(error) < 0:
        logging.info('Reject payment')
        await payment_repository.set_payment_status(payment_id, PaymentStatus.REJECTED)
    if result['error'] == '0':
        logging.info('Confirm payment')
        await payment_repository.set_payment_status(payment_id, PaymentStatus.CONFIRMED)

    result['click_trans_id'] = click_trans_id
    result['merchant_trans_id'] = merchant_trans_id
    result['merchant_prepare_id'] = merchant_prepare_id
    result['merchant_confirm_id'] = merchant_prepare_id

    return result
