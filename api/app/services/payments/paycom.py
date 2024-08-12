import logging
from datetime import datetime
import base64
import re

from typing import Any

from app.data.db.paycom_transactions_repository import PaycomTransactionsRepository
from app.data.db.payments_repository import PaymentsRepository
from app.data.db.subscriptions_repository import SubscriptionsRepository
from app.data.db.users_repository import UsersRepository
from app.data.models.payments import PaymentStatus
from app.routers.forms.payments import PaymeForm
from app.data.models.payme_transaction import PaymeTransactionStates
from app.services import bot
from app.config import settings
from app.data.models.subscription import Subscription


class PaycomPaymentHandler:
    data: PaymeForm
    transaction_repository: PaycomTransactionsRepository
    payments_repository: PaymentsRepository
    subscriptions_repository: SubscriptionsRepository
    users_repository: UsersRepository

    def __init__(self,
                 data: PaymeForm,
                 transactions_repository: PaycomTransactionsRepository,
                 payments_repository: PaymentsRepository,
                 subscriptions_repository: SubscriptionsRepository,
                 users_repository: UsersRepository,
                 headers
                 ):
        self.data = data
        self.transaction_repository = transactions_repository
        self.payments_repository = payments_repository
        self.users_repository = users_repository
        self.subscriptions_repository = subscriptions_repository
        self.headers = headers

    async def handle(self):
        method_maps = {
            'CheckPerformTransaction': self._handle_check_perform_transaction,
            'CheckTransaction': self._handle_check_transaction,
            'CreateTransaction': self._handle_create_transaction,
            'PerformTransaction': self._handle_perform_transaction,
            'CancelTransaction': self._handle_cancel_transaction
        }

        return await method_maps[self.data.method]()

    def _validate_auth(self):
        authorization = self.headers.get('Authorization')
        auth_error = PaycomException(
            self.data.id,
            PaycomException.create_message(
                'Неверная авторизация',
                'Неверная авторизация',
                'Invalid authorization'
            ),
            PaycomException.ERROR_INSUFFICIENT_PRIVILEGE,
            'Authorization'
        )
        if not authorization or not re.match(r'^\s*Basic\s+(\S+)\s*$', authorization):
            raise auth_error
        match = re.match(r'^\s*Basic\s+(\S+)\s*$', authorization)
        if not match or base64.b64decode(match.group(1)).decode('utf-8') != f"Paycom:{settings.payme_key}":
            raise auth_error

    async def _validate_payment(self):
        payment = None
        if 'order_id' in self.data.params['account']:
            payment = await self.payments_repository.get_payment_by_id(int(self.data.params['account']['order_id']))
        if not payment:
            raise PaycomException(
                self.data.id,
                PaycomException.create_message('Неверный код заказа.',
                                               'Harid kodida xatolik.',
                                               'Incorrect order code.'),
                PaycomException.ERROR_INVALID_ACCOUNT,
                'order_id'
            )
        logging.info(f"{payment.amount} - {self.data.params['amount']}")
        if payment.amount * 100 != self.data.params['amount']:
            raise PaycomException(
                self.data.id,
                'Incorrect amount',
                PaycomException.ERROR_INVALID_AMOUNT
            )
        if payment.status != PaymentStatus.NEW:
            raise PaycomException(
                self.data.id,
                'Order state is invalid',
                PaycomException.ERROR_COULD_NOT_PERFORM
            )

    async def _handle_check_perform_transaction(self):
        self._validate_auth()
        await self._validate_payment()
        logging.info(self.data.params)
        transaction = self.transaction_repository.find_transaction(self.data.params)
        if transaction and (
                transaction.state == PaymeTransactionStates.STATE_CREATED or transaction.state == PaymeTransactionStates.STATE_COMPLETED):
            raise PaycomException(
                self.data.id,
                'There is other active/completed transaction for this order.',
                PaycomException.ERROR_COULD_NOT_PERFORM
            )

        payment = await self.payments_repository.get_payment_by_id(int(self.data.params['account']['order_id']))

        return {
            'allow': True,
            'detail': {
                'receipt_type': 0,
                'items': [
                    {
                        'title': payment.subscription.name,
                        'price': payment.amount,
                        'count': payment.subscription_condition.duration_in_month,
                        'code': settings.ikpu,
                        'vat_percent': 0,
                        'package_code': settings.ikpu_unit_code,
                    }
                ]
            }
        }

    async def _handle_check_transaction(self):
        self._validate_auth()
        transaction = self.transaction_repository.find_transaction(self.data.params)
        if not transaction:
            raise PaycomException(
                self.data.id,
                "Transaction not found",
                PaycomException.ERROR_TRANSACTION_NOT_FOUND
            )

        timestamp = transaction.create_time.timestamp() * 1000000

        return {
            'create_time': int(timestamp / 1000),
            'perform_time': int(transaction.perform_time.timestamp() * 1000000 / 1000) if transaction.perform_time else 0,
            'cancel_time': int(transaction.cancel_time.timestamp() * 1000000 / 1000) if transaction.cancel_time else 0,
            'transaction': transaction.paycom_transaction_id,
            'state': transaction.state,
            'reason': 1 * transaction.reason if transaction.reason is not None else None
        }

    async def _handle_create_transaction(self):
        await self._validate_payment()
        # Check, is there any other transaction for this payment
        transaction = self.transaction_repository.find_transaction({'account': self.data.params['account']})
        if transaction:
            if (transaction.state == PaymeTransactionStates.STATE_CREATED
                or transaction.state == PaymeTransactionStates.STATE_COMPLETED) \
                    and transaction.paycom_transaction_id != self.data.params['id']:
                raise PaycomException(
                    self.data.id,
                    "There is other active/completed transaction for this order.",
                    PaycomException.ERROR_INVALID_ACCOUNT
                )
        transaction = self.transaction_repository.find_transaction(self.data.params)
        if transaction:
            if transaction.state != PaymeTransactionStates.STATE_CREATED:
                raise PaycomException(
                    self.data.id,
                    'Transaction found, but is not active.',
                    PaycomException.ERROR_COULD_NOT_PERFORM
                )
            else:
                return {
                    'create_time': transaction.create_time,
                    'transaction': transaction.id,
                    'state': transaction.state,
                    'receivers': None
                }
        transaction = self.transaction_repository.create_transaction(
            self.data.params['id'],
            self.data.params['time'],
            datetime.fromtimestamp(self.data.params['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            self.data.params['amount'],
            self.data.params['account']['order_id']
        )
        timestamp = transaction.create_time.timestamp() * 1000000

        return {
            'create_time': int(timestamp / 1000),
            'transaction': transaction.paycom_transaction_id,
            'state': transaction.state,
            'receivers': None
        }

    async def _handle_perform_transaction(self):
        self._validate_auth()
        transaction = self.transaction_repository.find_transaction(self.data.params)

        if not transaction:
            raise PaycomException(
                self.data.id,
                'Transaction not found',
                PaycomException.ERROR_TRANSACTION_NOT_FOUND
            )

        if transaction.state == PaymeTransactionStates.STATE_CREATED:
            try:
                await self.payments_repository.set_payment_status(transaction.payment_id, PaymentStatus.CONFIRMED)
                transaction = self.transaction_repository.perform_transaction(transaction.id)
                payment = await self.payments_repository.get_payment_by_id(transaction.payment_id)
                user = await self.users_repository.get_user_by_id(payment.user_id)
                subscription_user = await self.subscriptions_repository.add_subscription_to_user(user,
                                                                                                 payment.subscription_id,
                                                                                                 subscription_condition_id=payment.subscription_condition_id)
                subscription_entity: Subscription = await self.subscriptions_repository.get_subscription_by_id(
                    subscription_user.subscription_id)
                await bot.subscription_purchased(user, subscription_entity)
            except Exception as e:
                logging.error(e)

            return {
                'transaction': transaction.paycom_transaction_id,
                'perform_time': int(transaction.perform_time.timestamp() * 1000000 / 1000),
                'state': transaction.state
            }
        elif transaction.state == PaymeTransactionStates.STATE_COMPLETED:
            return {
                'transaction': transaction.paycom_transaction_id,
                'perform_time': int(transaction.perform_time.timestamp() * 1000000 / 1000),
                'state': transaction.state
            }
        else:
            raise PaycomException(
                self.data.id,
                "Could not perform transaction",
                PaycomException.ERROR_COULD_NOT_PERFORM
            )

    async def _handle_cancel_transaction(self):
        self._validate_auth()
        transaction = self.transaction_repository.find_transaction(self.data.params)

        if not transaction:
            raise PaycomException(
                self.data.id,
                'Transaction not found',
                PaycomException.ERROR_TRANSACTION_NOT_FOUND
            )

        if transaction.state in [PaymeTransactionStates.STATE_CANCELLED,
                                 PaymeTransactionStates.STATE_CANCELLED_AFTER_COMPLETE]:
            return {
                'transaction': transaction.id,
                'cancel_time': transaction.cancel_time.timestamp(),
                'state': transaction.state
            }
        elif transaction.state == PaymeTransactionStates.STATE_CREATED:
            self.transaction_repository.cancel_transaction(transaction.id, self.data.params['reason'])
            await self.payments_repository.set_payment_status(transaction.payment_id, PaymentStatus.REJECTED)
            return {
                'transaction': transaction.id,
                'cancel_time': transaction.cancel_time.timestamp(),
                'state': transaction.state
            }
        elif transaction.state == PaymeTransactionStates.STATE_COMPLETED:
            raise PaycomException(
                self.data.id,
                'Could not cancel transaction. Order is delivered/Service is completed.',
                PaycomException.ERROR_COULD_NOT_CANCEL
            )


class PaycomException(Exception):
    ERROR_INTERNAL_SYSTEM = -32400

    ERROR_INSUFFICIENT_PRIVILEGE = -32504

    ERROR_INVALID_JSON_RPC_OBJECT = -32600

    ERROR_METHOD_NOT_FOUND = -32601

    ERROR_INVALID_AMOUNT = -31001

    ERROR_TRANSACTION_NOT_FOUND = -31003

    ERROR_INVALID_ACCOUNT = -31050

    ERROR_COULD_NOT_CANCEL = -31007

    ERROR_COULD_NOT_PERFORM = -31008

    request_id: int
    message: Any
    data: Any
    code: int

    def __init__(self, request_id: int, message: Any, code: int, data: Any | None = None):
        self.request_id = request_id
        self.message = message
        self.code = code
        self.data = data

    @staticmethod
    def create_message(ru: str, uz: str = '', en: str = ''):
        return {'ru': ru, 'uz': uz, 'en': en}
