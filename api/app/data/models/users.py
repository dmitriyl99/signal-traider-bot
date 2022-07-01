from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from . import Base
from .subscription import SubscriptionUser


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_user_id = sa.Column(sa.Integer)
    name = sa.Column(sa.String(128))
    phone = sa.Column(sa.String(12))
    created_at = sa.Column(sa.DateTime, default=datetime.now)

    subscriptions = relationship(SubscriptionUser, back_populates='user')
