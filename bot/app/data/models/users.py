from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from . import Base
from .subscription import SubscriptionUser
from .payments import Payment


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_user_id = sa.Column(sa.BigInteger)
    name = sa.Column(sa.String(128))
    phone = sa.Column(sa.String(12))
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    registration_date = sa.Column(sa.DateTime)
    verified_at = sa.Column(sa.DateTime, nullable=True)

    subscriptions = relationship(SubscriptionUser, back_populates='user')
    payments = relationship(Payment, back_populates='user')
