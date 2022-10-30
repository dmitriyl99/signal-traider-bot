"""Add language to users

Revision ID: d079df242af9
Revises: bd08080ca62d
Create Date: 2022-10-30 11:47:45.148145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd079df242af9'
down_revision = 'bd08080ca62d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('language', sa.String, default='uz'))


def downgrade() -> None:
    op.drop_column('users', 'language')
