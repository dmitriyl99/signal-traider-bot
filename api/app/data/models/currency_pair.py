from . import Base

import sqlalchemy as sa


class CurrencyPair(Base):
    __tablename__ = 'currency_pairs'

    id = sa.Column(sa.Integer, primary_key=True)
    pair = sa.Column(sa.String(6))
