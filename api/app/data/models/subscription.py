from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from . import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

    conditions = relationship('SubscriptionCondition', back_populates='subscription', lazy='subquery')


class SubscriptionCondition(Base):
    __tablename__ = 'subscription_conditions'

    id = sa.Column(sa.Integer, primary_key=True)
    duration_in_month = sa.Column(sa.Integer)
    price = sa.Column(sa.Integer)
    subscription_id = sa.Column(sa.Integer, sa.ForeignKey('subscriptions.id'))

    subscription = relationship('Subscription', back_populates='conditions')
    users = relationship('SubscriptionUser', back_populates='subscription_condition')


class SubscriptionUser(Base):
    __tablename__ = 'subscription_user'
    user_id = sa.Column(sa.ForeignKey('users.id'), primary_key=True)
    subscription_condition_id = sa.Column(sa.ForeignKey('subscription_conditions.id'), primary_key=True)
    subscription_id = sa.Column(sa.Integer)
    active = sa.Column(sa.Boolean)
    subscription_condition: SubscriptionCondition = relationship('SubscriptionCondition', back_populates='users')
    subscription: Subscription = relationship('Subscription')
    user = relationship('User', back_populates='subscription')

    created_at = sa.Column(sa.DateTime, default=datetime.now)
