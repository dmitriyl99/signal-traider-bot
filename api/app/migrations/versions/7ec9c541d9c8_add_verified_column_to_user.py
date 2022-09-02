"""Add verified column to user

Revision ID: 7ec9c541d9c8
Revises: 75950f4db0ed
Create Date: 2022-08-31 22:15:05.719028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ec9c541d9c8'
down_revision = '75950f4db0ed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('verified_at', sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'verified_at')
