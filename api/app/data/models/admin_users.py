from . import Base
import sqlalchemy as sa


class AdminUser(Base):
    __tablename__ = 'admin_users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(250))
    password = sa.Column(sa.Text)
