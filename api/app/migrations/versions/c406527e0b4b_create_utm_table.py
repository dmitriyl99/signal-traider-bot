"""Create utm table

Revision ID: c406527e0b4b
Revises: 7ec9c541d9c8
Create Date: 2022-09-02 22:51:16.607454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c406527e0b4b'
down_revision = '7ec9c541d9c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'utm_commands',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String)
    )

    op.create_table(
        'utm_command_clicks',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('utm_command_id', sa.BigInteger, sa.ForeignKey('utm_commands.id'), nullable=True),
        sa.Column('utm_command_name', sa.String(250), nullable=True),
        sa.Column('user_telegram_id', sa.BigInteger, nullable=True),
        sa.Column('created_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('utm_command_clicks')
    op.drop_table('utm_commands')
