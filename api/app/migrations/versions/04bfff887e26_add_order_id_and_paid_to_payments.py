"""Add order id and paid to payments

Revision ID: 04bfff887e26
Revises: cd3cfb155b95
Create Date: 2022-10-27 17:39:49.089665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04bfff887e26'
down_revision = 'cd3cfb155b95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('payments', sa.Column('order_id', sa.Text, nullable=True))
    op.add_column('payments', sa.Column('status', sa.Integer, default=1))


def downgrade() -> None:
    op.drop_column('payments', 'order_id')
    op.drop_column('payments', 'status')
