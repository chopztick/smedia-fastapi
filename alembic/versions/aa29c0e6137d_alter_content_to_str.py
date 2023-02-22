"""alter_content_to_str

Revision ID: aa29c0e6137d
Revises: 96100c18dd54
Create Date: 2023-02-12 21:11:00.566197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa29c0e6137d'
down_revision = '96100c18dd54'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('posts', 'content', type_=sa.String())


def downgrade() -> None:
    op.alter_column('posts', 'content', type_=sa.Integer())
