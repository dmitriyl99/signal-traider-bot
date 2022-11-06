"""Add order id and status to payments

Revision ID: d87cd414a6f0
Revises: d079df242af9
Create Date: 2022-11-04 06:54:35.206427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd87cd414a6f0'
down_revision = 'd079df242af9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('payments', sa.Column('status', sa.String, default='NEW'))


def downgrade() -> None:
    op.drop_column('payments', 'status')
