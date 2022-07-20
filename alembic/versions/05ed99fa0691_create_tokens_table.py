"""create tokens table

Revision ID: 05ed99fa0691
Revises: 1d513b664545
Create Date: 2022-07-19 16:27:06.711367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05ed99fa0691'
down_revision = '1d513b664545'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tokens',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(256), nullable=False),
        sa.Column('jwt_token_active', sa.Boolean()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )


def downgrade() -> None:
    op.drop_table('tokens')
