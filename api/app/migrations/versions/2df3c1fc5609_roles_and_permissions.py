"""roles and permissions

Revision ID: 2df3c1fc5609
Revises: 49279fa30323
Create Date: 2022-10-16 12:36:20.785946

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2df3c1fc5609'
down_revision = '49279fa30323'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255))
    )
    op.create_table(
        'permissions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255))
    )
    op.create_table(
        'role_user',
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')),
        sa.Column('admin_user_id', sa.Integer, sa.ForeignKey('admin_users.id'))
    )
    op.create_table(
        'permission_role',
        sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id')),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id'))
    )
    op.create_table(
        'permission_user',
        sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id')),
        sa.Column('admin_user_id', sa.Integer, sa.ForeignKey('admin_users.id'))
    )

    initialize_role_and_permission()


def downgrade() -> None:
    op.drop_table('permission_role')
    op.drop_table('permission_user')
    op.drop_table('role_user')
    op.drop_table('permissions')
    op.drop_table('roles')


def initialize_role_and_permission() -> None:
    from sqlalchemy.orm import declarative_base

    base = declarative_base()

    permissions = ['can_send_signals', 'can_send_distribution', 'can_see_bot_users', 'can_add_admin_users',
                   'can_see_payments', 'can_use_utm']

    roles_table = sa.Table(
        'roles',
        base.metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255))
    )
    permissions_table = sa.Table(
        'permissions',
        base.metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255))
    )
    permission_role_table = sa.Table(
        'permission_role',
        base.metadata,
        sa.Column('permission_id', sa.Integer, sa.ForeignKey('permissions.id')),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id')))

    permissions = [
        {
            'id': 1,
            'name': 'can_send_signals'
        },
        {
            'id': 2,
            'name': 'can_send_distribution'
        },
        {
            'id': 3,
            'name': 'can_see_bot_users'
        },
        {
            'id': 4,
            'name': 'can_add_admin_users'
        },
        {
            'id': 5,
            'name': 'can_see_payments'
        },
        {
            'id': 6,
            'name': 'can_use_utm'
        }
    ]

    op.bulk_insert(roles_table, rows=[{'id': 1, 'name': 'Admin'}])
    op.bulk_insert(permissions_table, rows=permissions)
    op.bulk_insert(permission_role_table, rows=[{'role_id': 1, 'permission_id': permission['id']} for permission in permissions])
