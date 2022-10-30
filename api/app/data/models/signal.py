from . import Base, metadata
import sqlalchemy as sa

from datetime import datetime


class Signal(Base):
    __tablename__ = 'signals'

    id = sa.Column(sa.Integer, primary_key=True)
    currency_pair = sa.Column(sa.String)
    execution_method = sa.Column(sa.String)
    price = sa.Column(sa.Float)
    tr_1 = sa.Column(sa.String, nullable=True)
    tr_2 = sa.Column(sa.String, nullable=True)
    sl = sa.Column(sa.String, nullable=True)
    admin_user_id = sa.Column(sa.Integer, nullable=True)

    created_at = sa.Column(sa.DateTime, default=datetime.now)


signal_chat_message_mapper_table = sa.Table(
    'signal_chat_message_mapper',
    metadata,
    sa.Column('signal_id', sa.Integer),
    sa.Column('chat_id', sa.BigInteger),
    sa.Column('message_id', sa.BigInteger)
)
