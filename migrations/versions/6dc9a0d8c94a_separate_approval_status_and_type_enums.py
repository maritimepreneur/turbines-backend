"""separate approval status and type enums

Revision ID: 6dc9a0d8c94a
Revises: 665efac2c5e6
Create Date: 2026-04-13 14:29:42.991917

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '6dc9a0d8c94a'
down_revision = '665efac2c5e6'
branch_labels = None
depends_on = None


def upgrade():
    # Backfill status from legacy type values before changing type enum.
    op.execute("""
        UPDATE approvals
        SET status = CASE
            WHEN type::text = 'PENDING' THEN 'PENDING'::approval_status_enum
            WHEN type::text = 'APPROVED' THEN 'APPROVED'::approval_status_enum
            WHEN type::text = 'REJECTED' THEN 'REJECTED'::approval_status_enum
            ELSE status
        END
        WHERE status IS NULL
          AND type IS NOT NULL
    """)

    op.execute("ALTER TYPE approval_type_enum RENAME TO approval_type_enum_old")
    op.execute("CREATE TYPE approval_type_enum AS ENUM ('QUOTATION', 'PO', 'INVOICE', 'EXPENSE')")

    op.execute("""
        ALTER TABLE approvals
        ALTER COLUMN type TYPE approval_type_enum
        USING (
            CASE
                WHEN code LIKE 'QUO-%' THEN 'QUOTATION'
                WHEN code LIKE 'PO-%' THEN 'PO'
                WHEN code LIKE 'INV-%' THEN 'INVOICE'
                WHEN code LIKE 'EXP-%' THEN 'EXPENSE'
                WHEN quotation_id IS NOT NULL THEN 'QUOTATION'
                WHEN po_id IS NOT NULL THEN 'PO'
                WHEN invoice_id IS NOT NULL THEN 'INVOICE'
                WHEN expense_id IS NOT NULL THEN 'EXPENSE'
                ELSE NULL
            END
        )::approval_type_enum
    """)

    op.execute("DROP TYPE approval_type_enum_old")


def downgrade():
    op.execute("ALTER TYPE approval_type_enum RENAME TO approval_type_enum_new")
    op.execute("CREATE TYPE approval_type_enum AS ENUM ('PENDING', 'APPROVED', 'REJECTED')")

    op.execute("""
        ALTER TABLE approvals
        ALTER COLUMN type TYPE approval_type_enum
        USING (
            CASE
                WHEN COALESCE(status::text, 'PENDING') IN ('PENDING', 'APPROVED', 'REJECTED')
                    THEN COALESCE(status::text, 'PENDING')
                ELSE 'PENDING'
            END
        )::approval_type_enum
    """)

    op.execute("DROP TYPE approval_type_enum_new")
