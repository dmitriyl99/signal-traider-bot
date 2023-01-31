"""add importance for messages

Revision ID: 96d89fd62929
Revises: 73df8977fb2f
Create Date: 2023-01-31 10:27:35.101530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96d89fd62929'
down_revision = '73df8977fb2f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('text_distributions', sa.Column('importance', sa.Integer, default=0))


def downgrade() -> None:
    op.drop_column('text_distributions', 'importance')
