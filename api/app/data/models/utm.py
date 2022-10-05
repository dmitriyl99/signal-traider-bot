from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from . import Base


class UtmCommand(Base):
    __tablename__ = 'utm_commands'

    id = sa.Column(sa.BigInteger, primary_key=True)
    name = sa.Column(sa.String(250))

    clicks = relationship('UtmCommandClick', back_populates='utm_command')


class UtmCommandClick(Base):
    __tablename__ = 'utm_command_clicks'

    id = sa.Column(sa.BigInteger, primary_key=True)
    utm_command_id = sa.Column(sa.BigInteger, sa.ForeignKey('utm_commands.id'))
    utm_command_name = sa.Column(sa.String, nullable=True)
    user_telegram_id = sa.Column(sa.BigInteger, nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.now)

    utm_command = relationship(UtmCommand, back_populates='clicks')
