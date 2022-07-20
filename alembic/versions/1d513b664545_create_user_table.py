"""create: user table

Revision ID: 1d513b664545
Revises: 
Create Date: 2022-07-17 00:02:46.982402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d513b664545'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(256), nullable=False),
        sa.Column('password', sa.String(256), nullable=False),
        sa.Column('is_admin', sa.Boolean())
    )


def downgrade() -> None:
    op.drop_table('users')
