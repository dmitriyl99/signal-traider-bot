"""User registration date

Revision ID: 79bb7e453494
Revises: 2e1f5d30859d
Create Date: 2022-08-19 22:23:35.379997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79bb7e453494'
down_revision = '2e1f5d30859d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('registration_date', sa.DateTime, nullable=True, default=None))


def downgrade() -> None:
    op.drop_column('users', 'registration_date')
