from . import Base

import sqlalchemy as sa


class PaymeTransaction(Base):
    __tablename__ = 'payme_transactions'

    id = sa.Column(sa.BigInteger, primary_key=True),
    paycom_transaction_id = sa.Column(sa.String(25)),
    paycom_time = sa.Column(sa.String(13)),
    paycom_time_datetime = sa.Column(sa.DateTime),
    create_time = sa.Column(sa.DateTime),
    perform_time = sa.Column(sa.DateTime, nullable=True),
    cancel_time = sa.Column(sa.DateTime, nullable=True),
    amount = sa.Column(sa.Integer),
    state = sa.Column(sa.SmallInteger),
    reason = sa.Column(sa.SmallInteger, nullable=True),
    receivers = sa.Column(sa.String(500), nullable=True, comment='JSON array of receivers'),
    payment_id = sa.Column(sa.BigInteger)


class PaymeTransactionStates:
    STATE_CREATED = 1
    
    STATE_COMPLETED = 2
    
    STATE_CANCELLED = -1
    
    STATE_CANCELLED_AFTER_COMPLETE = -2


class PaymeTransactionReasons:
    REASON_RECEIVERS_NOT_FOUND = 1

    REASON_PROCESSING_EXECUTION_FAILED = 2

    REASON_EXECUTION_FAILED = 3

    REASON_CANCELLED_BY_TIMEOUT = 4

    REASON_FUND_RETURNED = 5

    REASON_UNKNOWN = 10
