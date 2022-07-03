"""Create signals table

Revision ID: ac27be85240c
Revises: c977e7b6cc71
Create Date: 2022-07-03 12:12:06.609180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac27be85240c'
down_revision = 'c977e7b6cc71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'signals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('currency_pair', sa.String),
        sa.Column('execution_method', sa.String),
        sa.Column('price', sa.Integer),
        sa.Column('tr_1', sa.String),
        sa.Column('tr_2', sa.String),
        sa.Column('sl', sa.String),
        sa.Column('created_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('signals')
