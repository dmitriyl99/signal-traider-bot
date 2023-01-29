"""add cloud payments transaction id to payments

Revision ID: 8e33d4f6b865
Revises: 73df8977fb2f
Create Date: 2023-01-29 17:29:36.274157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e33d4f6b865'
down_revision = '73df8977fb2f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('payments', sa.Column('cloud_payments_transaction_id', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('payments', 'cloud_payments_transaction_id')
