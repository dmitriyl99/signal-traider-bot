"""Create currency pairs table

Revision ID: 295b25ba304f
Revises: 79bb7e453494
Create Date: 2022-08-25 12:46:10.742613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '295b25ba304f'
down_revision = '79bb7e453494'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'currency_pairs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pair', sa.String(6))
    )


def downgrade() -> None:
    op.drop_table('currency_pairs')
