from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from . import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    category = sa.Column(sa.String)
    telegram_group_ids = sa.Column(sa.String(255))

    conditions = relationship('SubscriptionCondition', back_populates='subscription', lazy='subquery')
    users = relationship('SubscriptionUser', back_populates='subscription')


class SubscriptionCondition(Base):
    __tablename__ = 'subscription_conditions'

    id = sa.Column(sa.Integer, primary_key=True)
    duration_in_month = sa.Column(sa.Integer)
    duration_in_days = sa.Column(sa.Integer)
    price = sa.Column(sa.Integer)
    subscription_id = sa.Column(sa.Integer, sa.ForeignKey('subscriptions.id'))

    subscription = relationship('Subscription', back_populates='conditions')


class SubscriptionUser(Base):
    __tablename__ = 'subscription_user'

    user_id = sa.Column(sa.ForeignKey('users.id'), primary_key=True)
    subscription_id = sa.Column(sa.ForeignKey('subscriptions.id'), primary_key=True)
    active = sa.Column(sa.Boolean)
    proactively_added = sa.Column(sa.Boolean)
    duration_in_days = sa.Column(sa.Integer)
    activation_datetime = sa.Column(sa.DateTime, nullable=True, default=None)
    subscription: Subscription = relationship('Subscription', back_populates='users')
    user = relationship('User', back_populates='subscriptions')

    created_at = sa.Column(sa.DateTime, default=datetime.now)
