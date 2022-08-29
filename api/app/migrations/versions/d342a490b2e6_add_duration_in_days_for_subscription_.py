"""Add duration in days for subscription user

Revision ID: d342a490b2e6
Revises: 295b25ba304f
Create Date: 2022-08-28 09:02:40.068753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd342a490b2e6'
down_revision = '295b25ba304f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('subscription_user_subscription_condition_id_fkey', 'subscription_user', type_='foreignkey')
    op.drop_constraint('subscription_user_pkey', 'subscription_user')

    op.add_column('subscription_user', sa.Column('duration_in_days', sa.Integer, default=0))
    op.drop_column('subscription_user', 'subscription_condition_id')

    op.create_foreign_key('subscription_user_subscription_id_fkey', 'subscription_user', 'subscriptions', ['subscription_id'], ['id'])
    op.create_primary_key('subscription_user_pkey', 'subscription_user', ['user_id', 'subscription_id'])


def downgrade() -> None:
    op.drop_constraint('subscription_user_subscription_id_fkey', 'subscription_user', type_='foreignkey')
    op.drop_constraint('subscription_user_pkey', 'subscription_user')

    op.drop_column('subscription_user', 'duration_in_days')
    op.add_column('subscription_user', sa.Column('subscription_condition_id', sa.Integer, sa.ForeignKey('subscription_conditions.id'), nullable=True))

    op.create_foreign_key('subscription_user_subscription_condition_id_fkey', 'subscription_user', 'subscription_conditions', ['subscription_condition_id'], ['id'])
    op.create_primary_key('subscription_user_pkey', 'subscription_user', ['user_id'])
