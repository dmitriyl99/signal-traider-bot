from fastapi import APIRouter, Depends, Body

from app.data.db.payments_repository import PaymentsRepository
from app.dependencies import get_payments_repository, get_current_user
from app.data.models.admin_users import AdminUser
from app.data.models.payments import PaymentStatus
from app.routers.forms.payments import ClickPreparePaymentForm

from app.config import settings

import hashlib

router = APIRouter(prefix='/payments', tags=['Payments'])


@router.get('/')
async def get_payments_list(
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        current_user: AdminUser = Depends(get_current_user)
):
    return await payment_repository.get_all_payment()


def get_click_webhook_result(form: ClickPreparePaymentForm, payment_repository: PaymentsRepository):
    merchant_prepare_id = form.merchant_prepare_id if form.action is not None and form.action == 1 else ''
    sign_string = '{}{}{}{}{}{}{}{}'.format(
        form.click_trans_id, settings.click_service_id, settings.click_secret_key, form.merchant_trans_id, merchant_prepare_id, form.amount, form.action, form.sign_time
    )
    encoder = hashlib.md5(sign_string.encode('utf-8'))
    sign_string = encoder.hexdigest()
    if sign_string != form.sign_string:
        return {
            'error': '-1',
            'error_note': 'SIGN CHECK FAILED!'
        }
    if form.action not in ['0', '1']:
        return {
            'error': '-3',
            'error_note': 'Action not found'
        }
    payment = await payment_repository.get_payment_by_order_id(form.merchant_trans_id)
    if not payment:
        return {
            'error': '-5',
            'error_note': 'Order does not exists'
        }
    if abs(float(form.amount) - float(payment.amount) > 0.01):
        return {
            'error': '-2',
            'error_note': 'Incorrect parameter amount'
        }
    if payment.status == PaymentStatus.CONFIRMED:
        return {
            'error': '-4',
            'error_note': 'Already paid'
        }
    if form.action == '1':
        if form.merchant_trans_id != merchant_prepare_id:
            return {
                'error': '-6',
                'error_note': 'Transaction not found'
            }
    if payment.status == PaymentStatus.REJECTED or int(form.error) < 0:
        return {
            'error': '-9',
            'error_note': 'Transaction cancelled'
        }

    return {
        'error': '0',
        'error_note': 'Success'
    }


@router.post('/click/prepare')
async def click_prepare_payment(
        form: ClickPreparePaymentForm = Body(...),
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
):
    order_id = form.merchant_trans_id
    result = get_click_webhook_result(form, payment_repository)
    if result['error'] == 0:
        await payment_repository.set_status_for_payment_by_order_id(order_id, PaymentStatus.WAITING)
    result['click_trans_id'] = form.click_trans_id
    result['merchant_trans_id'] = form.merchant_trans_id
    result['merchant_prepare_id'] = form.merchant_trans_id
    result['merchant_confirm_id'] = form.merchant_trans_id

    return result


@router.post('/click/complete')
async def click_complete_payment(
        form: ClickPreparePaymentForm = Body(...),
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
):
    order_id = form.merchant_trans_id
    result = get_click_webhook_result(form, payment_repository)
    if form.error is not None and int(form.error) < 0:
        await payment_repository.set_status_for_payment_by_order_id(order_id, PaymentStatus.REJECTED)
    if form.error == '0':
        await payment_repository.set_status_for_payment_by_order_id(order_id, PaymentStatus.CONFIRMED)

    result['click_trans_id'] = form.click_trans_id
    result['merchant_trans_id'] = form.merchant_trans_id
    result['merchant_prepare_id'] = form.merchant_prepare_id
    result['merchant_confirm_id'] = form.merchant_prepare_id

    return result
