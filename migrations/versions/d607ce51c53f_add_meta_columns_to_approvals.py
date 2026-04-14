"""add meta columns to approvals

Revision ID: d607ce51c53f
Revises: 6dc9a0d8c94a
Create Date: 2026-04-14 13:19:14.136652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd607ce51c53f'
down_revision = '6dc9a0d8c94a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('approvals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
        batch_op.add_column(sa.Column('created_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('updated_by', sa.Integer(), nullable=True))

    # Backfill audit fields for existing approval rows linked to quotations.
    op.execute("""
        UPDATE approvals AS a
        SET
            created_at = COALESCE(q.created_at, a.created_at),
            updated_at = COALESCE(q.updated_at, a.updated_at),
            created_by = COALESCE(a.created_by, q.created_by),
            updated_by = COALESCE(a.updated_by, q.updated_by)
        FROM quotations AS q
        WHERE a.quotation_id = q.id
    """)


def downgrade():
    with op.batch_alter_table('approvals', schema=None) as batch_op:
        batch_op.drop_column('updated_by')
        batch_op.drop_column('created_by')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
