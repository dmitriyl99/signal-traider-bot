"""add duration in days to subscription condition

Revision ID: 73df8977fb2f
Revises: d5e6a0b5f831
Create Date: 2023-01-27 15:06:33.110432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73df8977fb2f'
down_revision = 'd5e6a0b5f831'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('subscription_conditions', sa.Column('duration_in_days', sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column('subscription_conditions', 'duration_in_days')
