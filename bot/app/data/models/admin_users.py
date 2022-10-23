from . import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .roles_and_permissions import role_user_association_table, permission_user_association_table


class AdminUser(Base):
    __tablename__ = 'admin_users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(250))
    password = sa.Column(sa.Text)

    roles = relationship("Role", secondary=role_user_association_table, back_populates='users')
    permissions = relationship("Permission", secondary=permission_user_association_table, back_populates='users')
