import logging

from typing import Optional

from fastapi import APIRouter, Depends, Body, Form, HTTPException, Request
from fastapi_csrf_protect import CsrfProtect

from app.data.db.payments_repository import PaymentsRepository
from app.data.db.subscriptions_repository import SubscriptionsRepository
from app.data.db.paycom_transactions_repository import PaycomTransactionsRepository
from app.data.db.users_repository import UsersRepository
from app.data.models.payments import PaymentStatus
from app.routers.forms.payments import PaymeForm, CloudPaymentsForm
from app.dependencies import get_payments_repository, get_current_user, get_paycom_transactions_repository, \
    get_subscriptions_repository, get_user_repository
from app.data.models.admin_users import AdminUser

from app.services.payments.click import ClickPaymentHandler
from app.services.payments.paycom import PaycomPaymentHandler, PaycomException
from app.services import bot

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
    logging.info(f'Request from click prepare: merchant_trans_id: {merchant_trans_id}, click_trans_id: {click_trans_id}, amount: {amount}, action: {action}, error: {error}, sign_time: {sign_time}, merchant_prepare_id: {merchant_prepare_id}')
    result = await click_handler.handle(merchant_trans_id, click_trans_id, amount, action,
                                        error, sign_time, sign_string, merchant_prepare_id,
                                        payment_repository)
    if result['error'] == '0':
        await payment_repository.set_payment_status(payment_id, PaymentStatus.WAITING)
    result['click_trans_id'] = click_trans_id
    result['merchant_trans_id'] = merchant_trans_id
    result['merchant_prepare_id'] = merchant_trans_id
    result['merchant_confirm_id'] = merchant_trans_id

    logging.info(f'Click prepare response {result}')

    return result


@router.post('/click/complete')
async def click_complete(
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        subscription_repository: SubscriptionsRepository = Depends(get_subscriptions_repository),
        users_repository: UsersRepository = Depends(get_user_repository),
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
    logging.info(
        f'Request from click complete: merchant_trans_id: {merchant_trans_id}, click_trans_id: {click_trans_id}, amount: {amount}, action: {action}, error: {error}, sign_time: {sign_time}, merchant_prepare_id: {merchant_prepare_id}')
    result = await click_handler.handle(merchant_trans_id, click_trans_id, amount, action,
                                        error, sign_time, sign_string, merchant_prepare_id,
                                        payment_repository)
    if error is not None and int(error) < 0:
        await payment_repository.set_payment_status(payment_id, PaymentStatus.REJECTED)
    if result['error'] == '0':
        payment = await payment_repository.get_payment_by_id(payment_id)
        user = await users_repository.get_user_by_id(payment.id)
        await payment_repository.set_payment_status(payment_id, PaymentStatus.CONFIRMED)
        await subscription_repository.add_subscription_to_user(
            user,
            payment.subscription_id,
            subscription_condition_id=payment.subscription_condition_id,
            active=True
        )
        await bot.send_message_to_user(user.telegram_user_id, "Подписка куплена!", remove_keyboard=True)
        await bot.add_user_to_group(telegram_user_id=user.telegram_user_id)
    result['click_trans_id'] = click_trans_id
    result['merchant_trans_id'] = merchant_trans_id
    result['merchant_prepare_id'] = merchant_prepare_id
    result['merchant_confirm_id'] = merchant_prepare_id

    logging.info(f'Click complete response {result}')

    return result


@router.post('/payme')
async def payme(
        form: PaymeForm = Body(),
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        paycom_transactions_repository: PaycomTransactionsRepository = Depends(get_paycom_transactions_repository),
        subscription_repository: SubscriptionsRepository = Depends(get_subscriptions_repository),
        users_repository: UsersRepository = Depends(get_user_repository),

):
    handler = PaycomPaymentHandler(form, paycom_transactions_repository, payment_repository, subscription_repository,
                                   users_repository)
    logging.info(f'Request from payme: id: {form.id}, Method: {form.method}, Params: {form.params}')
    try:
        result = await handler.handle()
    except PaycomException as e:
        error = {'code': e.code}
        if e.message:
            error['message'] = e.message
        if e.data:
            error['data'] = e.data

        response = {
            'id': e.request_id,
            'result': None,
            'error': error
        }
        logging.info(f'Response to payme {response}')
        return response
    response = {
        'jsonrpc': '2.0',
        'id': form.id,
        'result': result,
        'error': None
    }
    logging.info(f'Response to payme {response}')
    return response


@router.post('/cloud-payments/success')
async def cloud_payments(
        request: Request,
        csrf_protect: CsrfProtect = Depends(),
        form: CloudPaymentsForm = Body(),
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        subscription_repository: SubscriptionsRepository = Depends(get_subscriptions_repository),
        users_repository: UsersRepository = Depends(get_user_repository),
):
    csrf_protect.validate_csrf_in_cookies(request)
    await payment_repository.set_payment_status(form.payment_id, PaymentStatus.CONFIRMED)
    user = await users_repository.get_user_by_id(form.user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    await subscription_repository.add_subscription_to_user(
        user, form.subscription_id,
        subscription_condition_id=form.subscription_condition_id,
        proactively_added=False,
        active=True
    )
    await bot.send_message_to_user(user.telegram_user_id, "Подписка куплена!", remove_keyboard=True)
    await bot.add_user_to_group(telegram_user_id=user.telegram_user_id)

    return {}
