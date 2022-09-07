"""Nullable columns for signals table

Revision ID: 49279fa30323
Revises: c406527e0b4b
Create Date: 2022-09-07 05:35:53.734130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49279fa30323'
down_revision = 'c406527e0b4b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('signals', 'tr_1', nullable=True)
    op.alter_column('signals', 'tr_2', nullable=True)
    op.alter_column('signals', 'sl', nullable=True)


def downgrade() -> None:
    op.alter_column('signals', 'tr_1', nullable=False)
    op.alter_column('signals', 'tr_2', nullable=False)
    op.alter_column('signals', 'sl', nullable=False)
