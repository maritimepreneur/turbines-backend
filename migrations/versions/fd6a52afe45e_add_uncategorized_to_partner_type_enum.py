"""add Uncategorized to partner_type_enum

Revision ID: fd6a52afe45e
Revises: 9b335ad4c864
Create Date: 2026-03-06 14:05:03.528900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd6a52afe45e'
down_revision = '9b335ad4c864'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE partner_type_enum ADD VALUE 'UNCATEGORIZED'")

def downgrade():
    pass
