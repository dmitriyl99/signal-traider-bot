import sqlalchemy as sa
from sqlalchemy.orm import relationship

from . import Base

role_user_association_table = sa.Table(
    'role_user',
    Base.metadata,
    sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
    sa.Column('admin_user_id', sa.Integer, sa.ForeignKey('admin_users.id'))
)

permission_role_association_table = sa.Table(
    'permission_role',
    Base.metadata,
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id')),
    sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id'))
)

permission_user_association_table = sa.Table(
    'permission_user',
    Base.metadata,
    sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id')),
    sa.Column('admin_user_id', sa.Integer, sa.ForeignKey('admin_users.id'))
)


class Role(Base):
    __tablename__ = 'roles'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(255))

    users = relationship("AdminUser", secondary=role_user_association_table, back_populates='roles')
    permissions = relationship('Permission', secondary=permission_role_association_table, back_populates='roles')


class Permission(Base):
    __tablename__ = 'permissions'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(255))

    users = relationship("AdminUser", secondary=permission_user_association_table, back_populates='permissions')
    roles = relationship("Role", secondary=permission_role_association_table, back_populates='permissions')
