"""enforce one-to-one purchase order relations

Revision ID: 33c345f64d8e
Revises: d607ce51c53f
Create Date: 2026-04-14 13:48:46.047542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33c345f64d8e'
down_revision = 'd607ce51c53f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('approvals', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_approvals_po_id', ['po_id'])

    with op.batch_alter_table('purchase_orders', schema=None) as batch_op:
        batch_op.alter_column('quotation_id', existing_type=sa.Integer(), nullable=False)
        batch_op.create_unique_constraint('uq_purchase_orders_quotation_id', ['quotation_id'])


def downgrade():
    with op.batch_alter_table('purchase_orders', schema=None) as batch_op:
        batch_op.drop_constraint('uq_purchase_orders_quotation_id', type_='unique')
        batch_op.alter_column('quotation_id', existing_type=sa.Integer(), nullable=True)

    with op.batch_alter_table('approvals', schema=None) as batch_op:
        batch_op.drop_constraint('uq_approvals_po_id', type_='unique')
