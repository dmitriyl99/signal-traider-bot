"""Create payments table

Revision ID: c977e7b6cc71
Revises: de6ec11f9113
Create Date: 2022-07-01 13:49:39.940589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c977e7b6cc71'
down_revision = 'de6ec11f9113'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('amount', sa.Integer),
        sa.Column('provider', sa.String),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('subscription_id', sa.Integer, sa.ForeignKey('subscriptions.id')),
        sa.Column('subscription_condition_id', sa.Integer, sa.ForeignKey('subscription_conditions.id')),
    )


def downgrade() -> None:
    op.drop_table('payments')
