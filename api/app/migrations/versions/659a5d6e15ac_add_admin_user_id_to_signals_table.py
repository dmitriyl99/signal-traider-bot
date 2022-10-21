"""Add admin user id to signals table

Revision ID: 659a5d6e15ac
Revises: 2df3c1fc5609
Create Date: 2022-10-21 13:11:04.549164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '659a5d6e15ac'
down_revision = '2df3c1fc5609'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('signals', sa.Column('admin_user_id', sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column('signals', 'admin_user_id')
