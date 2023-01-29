from datetime import datetime

from . import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Payment(Base):
    __tablename__ = 'payments'

    id = sa.Column(sa.BigInteger, primary_key=True)
    amount = sa.Column(sa.Integer)
    provider = sa.Column(sa.String)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    subscription_id = sa.Column(sa.Integer, sa.ForeignKey('subscriptions.id'))
    subscription_condition_id = sa.Column(sa.Integer, sa.ForeignKey('subscription_conditions.id'))
    cloud_payments_transaction_id = sa.Column(sa.String(255), nullable=True)
    status = sa.Column(sa.String, default='NEW')
    created_at = sa.Column(sa.DateTime, default=datetime.now)

    user = relationship('User', back_populates='payments')
    subscription = relationship('Subscription')
    subscription_condition = relationship('SubscriptionCondition')


class PaymentStatus:
    NEW = 'NEW'
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'
    WAITING = 'WAITING'
