from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import between

from . import Session
from ..models.payme_transaction import PaymeTransaction, PaymeTransactionStates
from app.helpers import date as date_helper


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
            session.refresh(transaction)
        return transaction

    def perform_transaction(self, transaction_id: int) -> PaymeTransaction:
        with Session() as session:
            transaction: PaymeTransaction = session.query(PaymeTransaction).get(transaction_id)
            transaction.state = PaymeTransactionStates.STATE_COMPLETED
            transaction.perform_time = datetime.now()
            session.commit()
            session.refresh(transaction)
        return transaction

    def cancel_transaction(self, transaction_id: int, reason) -> PaymeTransaction:
        with Session() as session:
            transaction: PaymeTransaction = session.query(PaymeTransaction).get(transaction_id)
            transaction.reason = 1 * reason
            transaction.cancel_time = datetime.now()
            if transaction.state == PaymeTransactionStates.STATE_COMPLETED:
                transaction.state = PaymeTransactionStates.STATE_CANCELLED_AFTER_COMPLETE
            else:
                transaction.state = PaymeTransactionStates.STATE_CANCELLED
            session.commit()
            session.refresh(transaction)
        return transaction

    def report(self, from_date, to_date):
        from_date = date_helper.timestamp2datetime(from_date)
        to_date = date_helper.timestamp2datetime(to_date)

        with Session() as session:
            transactions = session.query(PaymeTransaction).filter(
                between(PaymeTransaction.paycom_time_datetime, from_date, to_date)
            )
        result = []

        for transaction in transactions:
            result.append({
                'id': transaction.paycom_transaction_id,
                'time': 1 * transaction.paycom_time,
                'amount': 1 * transaction.amount,
                'account': {
                    'order_id': transaction.payment_id
                },
                'create_time': date_helper.datetime2timestamp(transaction.create_time),
                'perform_time': date_helper.datetime2timestamp(transaction.perform_time),
                'cancel_time': date_helper.datetime2timestamp(transaction.cancel_time),
                'transaction': 1 * transaction.id,
                'state': 1 * transaction.state,
                'reason': 1 * transaction.reason if transaction.reason else None,
                'receivers': None
            })

        return result
