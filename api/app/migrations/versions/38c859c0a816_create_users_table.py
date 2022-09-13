"""Create users table

Revision ID: 38c859c0a816
Revises: 
Create Date: 2022-06-18 15:40:25.771080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38c859c0a816'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('telegram_user_id', sa.BigInteger),
        sa.Column('name', sa.String(128)),
        sa.Column('phone', sa.String(25)),
        sa.Column('created_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('users')
