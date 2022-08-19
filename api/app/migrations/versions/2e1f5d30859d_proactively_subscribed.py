"""Proactively subscribed

Revision ID: 2e1f5d30859d
Revises: b2d07996f511
Create Date: 2022-08-19 21:02:52.477690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e1f5d30859d'
down_revision = 'b2d07996f511'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('subscription_user', sa.Column('proactively_added', sa.Boolean, default=False))


def downgrade() -> None:
    op.drop_column('subscription_user', 'proactively_added')
