"""add currency for text messages

Revision ID: dad83ec0673e
Revises: 96d89fd62929
Create Date: 2023-01-31 15:13:04.674517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dad83ec0673e'
down_revision = '96d89fd62929'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('text_distributions', sa.Column('currency', sa.String(10), nullable=True))


def downgrade() -> None:
    op.drop_column('text_distributions', 'currency')
