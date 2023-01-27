"""add subscriptions category

Revision ID: d5e6a0b5f831
Revises: b9a5c1aed464
Create Date: 2023-01-27 14:43:47.866398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5e6a0b5f831'
down_revision = 'b9a5c1aed464'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('subscriptions', sa.Column('category', sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column('subscriptions', 'category')
