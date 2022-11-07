from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import Session
from ..models.payme_transaction import PaymeTransaction, PaymeTransactionStates


class PaycomTransactionsRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    def find_transaction(self, params: dict) -> PaymeTransaction | None:
        with Session() as session:
            if 'id' in params:
                return session.query(PaymeTransaction).where(PaymeTransaction.paycom_transaction_id == params['id']).first()
            elif 'account' in params and 'order_id' in params['account']:
                return session.query(PaymeTransaction).where(PaymeTransaction.payment_id == params['account']['order_id']).first()
            else:
                raise Exception('Parameter to find a transaction is not specified.')

    def create_transaction(
            self,
            paycom_transaction_id,
            paycom_time,
            paycom_time_datetime,
            amount,
            payment_id,
    ) -> PaymeTransaction:
        transaction = PaymeTransaction(
            paycom_transaction_id=paycom_transaction_id,
            paycom_time=paycom_time,
            paycom_time_datetime=paycom_time_datetime,
            create_time=datetime.now(),
            amount=amount,
            state=PaymeTransactionStates.STATE_CREATED,
            payment_id=payment_id
        )
        with Session() as session:
            session.add(transaction)
            session.commit()
        return transaction

    def perform_transaction(self, transaction_id: int):
        with Session() as session:
            transaction: PaymeTransaction = session.query(PaymeTransaction).get(transaction_id)
            transaction.state = PaymeTransactionStates.STATE_COMPLETED
            transaction.perform_time = datetime.now()
            session.commit()

    def cancel_transaction(self, transaction_id: int, reason):
        with Session() as session:
            transaction: PaymeTransaction = session.query(PaymeTransaction).get(transaction_id)
            transaction.reason = 1 * reason
            transaction.cancel_time = datetime.now()
            if transaction.state == PaymeTransactionStates.STATE_COMPLETED:
                transaction.state = PaymeTransactionStates.STATE_CANCELLED_AFTER_COMPLETE
            else:
                transaction.state = PaymeTransactionStates.STATE_CANCELLED
            session.commit()
