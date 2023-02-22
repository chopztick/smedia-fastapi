"""add content column

Revision ID: 777e8712279d
Revises: 0d9cecf066e6
Create Date: 2023-02-12 18:31:45.022231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '777e8712279d'
down_revision = '0d9cecf066e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
