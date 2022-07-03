"""Create subscriptions table

Revision ID: 645acf3ebe36
Revises: 38c859c0a816
Create Date: 2022-06-18 16:42:55.527419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '645acf3ebe36'
down_revision = '38c859c0a816'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(128))
    )

    op.create_table(
        'subscription_conditions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('duration_in_month', sa.Integer),
        sa.Column('price', sa.Integer),
        sa.Column('subscription_id', sa.Integer, sa.ForeignKey('subscriptions.id'))
    )

    op.create_table(
        'subscription_user',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('subscription_condition_id', sa.Integer, sa.ForeignKey('subscription_conditions.id'), primary_key=True),
        sa.Column('subscription_id', sa.Integer),
        sa.Column('active', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table('subscription_user')
    op.drop_table('subscription_conditions')
    op.drop_table('subscriptions')
