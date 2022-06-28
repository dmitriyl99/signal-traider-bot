"""Create AdminUsers table

Revision ID: de6ec11f9113
Revises: 
Create Date: 2022-06-28 07:02:52.981766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de6ec11f9113'
down_revision = '645acf3ebe36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'admin_users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(250)),
        sa.Column('password', sa.Text)
    )


def downgrade() -> None:
    op.drop_table('admin_users')
