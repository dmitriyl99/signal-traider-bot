import logging
from datetime import datetime

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
                 users_repository: UsersRepository
                 ):
        self.data = data
        self.transaction_repository = transactions_repository
        self.payments_repository = payments_repository
        self.users_repository = users_repository
        self.subscriptions_repository = subscriptions_repository

    async def handle(self):
        method_maps = {
            'CheckPerformTransaction': self._handle_check_perform_transaction,
            'CheckTransaction': self._handle_check_transaction,
            'CreateTransaction': self._handle_create_transaction,
            'PerformTransaction': self._handle_perform_transaction,
            'CancelTransaction': self._handle_cancel_transaction
        }

        return await method_maps[self.data.method]()

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
        await self._validate_payment()

        transaction = self.transaction_repository.find_transaction(self.data.params)
        if transaction and (
                transaction.state == PaymeTransactionStates.STATE_CREATED or transaction.state == PaymeTransactionStates.STATE_COMPLETED):
            raise PaycomException(
                self.data.id,
                'There is other active/completed transaction for this order.',
                PaycomException.ERROR_COULD_NOT_PERFORM
            )

        payment = await self.payments_repository.get_payment_by_id(transaction.payment_id)

        return {
            'allow': True,
            'detail': {
                'receipt_type': 0,
                'items': [
                    {
                        'title': payment.subscription.name,
                        'price': payment.subscription_condition.price,
                        'count': payment.subscription_condition.duration_in_month,
                        'code': settings.ikpu,
                        'vat_percent': 0,
                        'package_code': settings.ikpu_unit_code,
                        'units': settings.ikpu_unit_code
                    }
                ]
            }
        }

    async def _handle_check_transaction(self):
        transaction = self.transaction_repository.find_transaction(self.data.params)
        if not transaction:
            raise PaycomException(
                self.data.id,
                "Transaction not found",
                PaycomException.ERROR_TRANSACTION_NOT_FOUND
            )

        return {
            'create_time': transaction.create_time,
            'perform_time': transaction.perform_time,
            'cancel_time': transaction.cancel_time,
            'transaction': transaction.id,
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
            datetime.fromtimestamp(int(self.data.params['time'])).strftime('%Y-%m-%d %H:%M:%S'),
            self.data.params['amount'],
            self.data.params['account']['order_id']
        )

        return {
            'create_time': transaction.create_time,
            'transaction': transaction.id,
            'state': transaction.state,
            'receivers': None
        }

    async def _handle_perform_transaction(self):
        transaction = self.transaction_repository.find_transaction(self.data.params)

        if not transaction:
            raise PaycomException(
                self.data.id,
                'Transaction not found',
                PaycomException.ERROR_TRANSACTION_NOT_FOUND
            )

        if transaction.state == PaymeTransactionStates.STATE_CREATED:
            await self.payments_repository.set_payment_status(transaction.payment_id, PaymentStatus.CONFIRMED)
            self.transaction_repository.perform_transaction(transaction.id)
            payment = await self.payments_repository.get_payment_by_id(transaction.payment_id)
            user = await self.users_repository.get_user_by_id(payment.user_id)
            await self.subscriptions_repository.add_subscription_to_user(user, payment.subscription_id, subscription_condition_id=payment.subscription_condition_id)
            await bot.send_message_to_user(user.telegram_user_id, "Подписка куплена!", remove_keyboard=True)

            return {
                'transaction': transaction.id,
                'perform_time': transaction.perform_time.timestamp(),
                'state': transaction.state
            }
        elif transaction.state == PaymeTransactionStates.STATE_COMPLETED:
            return {
                'transaction': transaction.id,
                'perform_time': transaction.perform_time.timestamp(),
                'state': transaction.state
            }
        else:
            raise PaycomException(
                self.data.id,
                "Could not perform transaction",
                PaycomException.ERROR_COULD_NOT_PERFORM
            )

    async def _handle_cancel_transaction(self):
        transaction = self.transaction_repository.find_transaction(self.data.params)

        if not transaction:
            raise PaycomException(
                self.data.id,
                'Transaction not found',
                PaycomException.ERROR_TRANSACTION_NOT_FOUND
            )

        if transaction.state in [PaymeTransactionStates.STATE_CANCELLED, PaymeTransactionStates.STATE_CANCELLED_AFTER_COMPLETE]:
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
