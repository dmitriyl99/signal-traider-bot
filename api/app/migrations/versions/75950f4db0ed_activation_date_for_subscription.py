"""Activation date for subscription

Revision ID: 75950f4db0ed
Revises: d342a490b2e6
Create Date: 2022-08-29 11:16:41.061334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75950f4db0ed'
down_revision = 'd342a490b2e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('subscription_user', sa.Column('activation_datetime', sa.DateTime, nullable=True, default=None))


def downgrade() -> None:
    op.drop_column('subscription_user', 'activation_datetime')
