"""Add analyst_id to users table

Revision ID: cd3cfb155b95
Revises: 659a5d6e15ac
Create Date: 2022-10-23 16:20:02.191616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd3cfb155b95'
down_revision = '659a5d6e15ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('analyst_id', sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'analyst_id')
