import logging

from typing import Optional

from fastapi import APIRouter, Depends, Body, Form

from app.data.db.payments_repository import PaymentsRepository
from app.data.db.paycom_transactions_repository import PaycomTransactionsRepository
from app.data.models.payments import PaymentStatus
from app.routers.forms.payments import PaymeForm
from app.dependencies import get_payments_repository, get_current_user, get_paycom_transactions_repository
from app.data.models.admin_users import AdminUser

from app.services.payments.click import ClickPaymentHandler
from app.services.payments.paycom import PaycomPaymentHandler, PaycomException

router = APIRouter(prefix='/payments', tags=['Payments'])


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
        amount: Optional[str] = Form(),
        action: Optional[str] = Form(),
        error: Optional[str] = Form(),
        sign_time: Optional[str] = Form(),
        sign_string: Optional[str] = Form(),
        merchant_prepare_id: Optional[str] = Form(None),
):
    payment_id = int(merchant_trans_id)
    click_handler = ClickPaymentHandler(payment_repository)
    result = await click_handler.handle(merchant_trans_id, click_trans_id, amount, action,
                                        error, sign_time, sign_string, merchant_prepare_id,
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
        amount: Optional[str] = Form(),
        action: Optional[str] = Form(),
        error: Optional[str] = Form(None),
        sign_time: Optional[str] = Form(),
        sign_string: Optional[str] = Form(),
        merchant_prepare_id: Optional[str] = Form(None),
):
    payment_id = int(merchant_trans_id)
    click_handler = ClickPaymentHandler(payment_repository)
    result = await click_handler.handle(merchant_trans_id, click_trans_id, amount, action,
                                        error, sign_time, sign_string, merchant_prepare_id,
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


@router.post('/payme')
async def payme(
        form: PaymeForm = Body(),
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        paycom_transactions_repository: PaycomTransactionsRepository = Depends(get_paycom_transactions_repository)
):
    handler = PaycomPaymentHandler(form, paycom_transactions_repository, payment_repository)
    try:
        result = await handler.handle()
    except PaycomException as e:
        error = {'code': e.code}
        if e.message:
            error['message'] = e.message
        if e.data:
            error['data'] = e.data
        return {
            'id': e.request_id,
            'result': None,
            'error': error
        }
    return {
        'jsonrpc': '2.0',
        'id': form.id,
        'result': result,
        'error': None
    }
