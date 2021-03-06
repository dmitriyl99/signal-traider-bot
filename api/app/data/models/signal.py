from . import Base
import sqlalchemy as sa

from datetime import datetime


class Signal(Base):
    __tablename__ = 'signals'

    id = sa.Column(sa.Integer, primary_key=True)
    currency_pair = sa.Column(sa.String)
    execution_method = sa.Column(sa.String)
    price = sa.Column(sa.Integer)
    tr_1 = sa.Column(sa.String)
    tr_2 = sa.Column(sa.String)
    sl = sa.Column(sa.String)

    created_at = sa.Column(sa.DateTime, default=datetime.now)
