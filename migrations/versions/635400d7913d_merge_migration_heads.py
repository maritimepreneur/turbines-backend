"""merge migration heads

Revision ID: 635400d7913d
Revises: 04140822b62e, 9f88c863767c
Create Date: 2026-02-06 11:20:11.494501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '635400d7913d'
down_revision = ('04140822b62e', '9f88c863767c')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
