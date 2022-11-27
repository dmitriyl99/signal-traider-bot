"""add text_messages table

Revision ID: b9a5c1aed464
Revises: 30cf2572d627
Create Date: 2022-11-27 09:26:48.041693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9a5c1aed464'
down_revision = '30cf2572d627'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'text_distributions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('text', sa.Text),
        sa.Column('admin_user_id', sa.Integer, sa.ForeignKey('admin_users.id')),
        sa.Column('created_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('text_distributions')
