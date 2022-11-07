"""create payme_transactions table

Revision ID: 30cf2572d627
Revises: d87cd414a6f0
Create Date: 2022-11-06 12:06:31.485998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30cf2572d627'
down_revision = 'd87cd414a6f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'payme_transactions',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('paycom_transaction_id', sa.String(25)),
        sa.Column('paycom_time', sa.String(13)),
        sa.Column('paycom_time_datetime', sa.DateTime),
        sa.Column('create_time', sa.DateTime),
        sa.Column('perform_time', sa.DateTime, nullable=True),
        sa.Column('cancel_time', sa.DateTime, nullable=True),
        sa.Column('amount', sa.Integer),
        sa.Column('state', sa.SmallInteger),
        sa.Column('reason', sa.SmallInteger, nullable=True),
        sa.Column('receivers', sa.String(500), nullable=True, comment='JSON array of receivers'),
        sa.Column('payment_id', sa.BigInteger)
    )


def downgrade() -> None:
    op.drop_table('payme_transactions')
