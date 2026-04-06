"""merge heads 89f6 and f1f29

Revision ID: e6e53c418829
Revises: 89f6c8c06177, f1f29e725880
Create Date: 2026-03-13 11:27:20.051996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6e53c418829'
down_revision = ('89f6c8c06177', 'f1f29e725880')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
