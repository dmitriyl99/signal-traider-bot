import logging

from typing import Optional

from fastapi import APIRouter, Depends, Body, Form, Request
from fastapi.templating import Jinja2Templates

from app.data.db.payments_repository import PaymentsRepository
from app.data.db.subscriptions_repository import SubscriptionsRepository
from app.data.db.paycom_transactions_repository import PaycomTransactionsRepository
from app.data.db.users_repository import UsersRepository
from app.data.models.payments import PaymentStatus
from app.routers.forms.payments import PaymeForm, CloudPaymentsPost3dSecureForm
from app.dependencies import get_payments_repository, get_current_user, get_paycom_transactions_repository, \
    get_subscriptions_repository, get_user_repository
from app.data.models.admin_users import AdminUser

from app.services.payments.click import ClickPaymentHandler
from app.services.payments.paycom import PaycomPaymentHandler, PaycomException
from app.services.cloud_payments import CloudPaymentApi
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
        await bot.send_message_to_user(user.telegram_user_id, "Подписка куплена!")
    result['click_trans_id'] = click_trans_id
    result['merchant_trans_id'] = merchant_trans_id
    result['merchant_prepare_id'] = merchant_prepare_id
    result['merchant_confirm_id'] = merchant_prepare_id

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


@router.get('/cloud-payments/pre-3d-secure')
async def cloud_payments_pre_3d_secure(
        request: Request,
        acs_url: str,
        pa_req: str,
        md: str,
):
    templates = Jinja2Templates(directory='app/templates')
    return templates.TemplateResponse(
        'cloud-payments-3d-secure.html', {
            'request': request,
            'acs_url': acs_url,
            'pa_req': pa_req.strip(),
            'md': md
        }
    )


@router.post('/cloud-payments/post-3d-secure')
async def cloud_payments_post_3d_secure(
        form: CloudPaymentsPost3dSecureForm = Body(),
        subscription_repository: SubscriptionsRepository = Depends(get_subscriptions_repository),
        payment_repository: PaymentsRepository = Depends(get_payments_repository),
        users_repository: UsersRepository = Depends(get_user_repository),
):
    cloud_payments_api = CloudPaymentApi()
    result = cloud_payments_api.post_3d_secure(form.MD, form.PaRes)
    payment = await payment_repository.get_payment_by_clouds_payment_transaction_id(form.MD)
    if payment is not None:
        user = await users_repository.get_user_by_id(payment.user_id)
        if result['status'] == 'success':
            await subscription_repository.add_subscription_to_user(
                user,
                payment.subscription_id,
                subscription_condition_id=payment.subscription_condition_id,
                active=True
            )
            await payment_repository.set_payment_status(payment_id=payment.id, status=PaymentStatus.CONFIRMED)
            await bot.send_message_to_user(user.telegram_user_id, "Подписка куплена!")
            return 'Success'
        else:
            data = result['data']
            await bot.send_message_to_user(
                user.telegram_user_id,
                f'Оплата не прошла\n\n<b>Код ошибки:</b> <code>{data["reason_code"]}</code>\n<b>Ошибка:</b> {data["reason"]}\n<b>Сообщение:</b> {data["message"]}'
            )
            return 'Rejected'
    return 'Error'
