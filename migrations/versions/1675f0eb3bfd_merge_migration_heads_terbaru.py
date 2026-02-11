"""merge migration heads terbaru

Revision ID: 1675f0eb3bfd
Revises: 15ac839a2be3, b35831bff6c3
Create Date: 2026-02-09 10:37:51.941676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1675f0eb3bfd'
down_revision = ('15ac839a2be3', 'b35831bff6c3')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
