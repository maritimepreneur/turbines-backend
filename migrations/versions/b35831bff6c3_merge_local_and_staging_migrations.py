"""merge local and staging migrations

Revision ID: b35831bff6c3
Revises: 04140822b62e, 9f88c863767c
Create Date: 2026-02-06 11:36:11.860371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b35831bff6c3'
down_revision = ('04140822b62e', '9f88c863767c')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
