"""Create mapper for signals chat

Revision ID: bd08080ca62d
Revises: cd3cfb155b95
Create Date: 2022-10-30 08:22:06.106272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd08080ca62d'
down_revision = 'cd3cfb155b95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'signal_chat_message_mapper',
        sa.Column('signal_id', sa.Integer),
        sa.Column('chat_id', sa.BigInteger),
        sa.Column('message_id', sa.BigInteger)
    )


def downgrade() -> None:
    op.drop_table('signal_chat_message_mapper')
