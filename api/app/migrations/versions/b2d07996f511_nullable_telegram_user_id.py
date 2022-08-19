"""Nullable telegram user id

Revision ID: b2d07996f511
Revises: ac27be85240c
Create Date: 2022-08-19 10:14:32.153960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2d07996f511'
down_revision = 'ac27be85240c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('users', 'telegram_user_id', nullable=True)


def downgrade() -> None:
    pass
