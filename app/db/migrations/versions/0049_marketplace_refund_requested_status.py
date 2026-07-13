"""allow marketplace refund requested status

Revision ID: 0049_marketplace_refund_requested_status
Revises: 0048_marketplace_orders_payments_wallet
"""

from alembic import op

revision = "0049_marketplace_refund_requested_status"
down_revision = "0048_marketplace_orders_payments_wallet"
branch_labels = None
depends_on = None


ORDER_STATUSES = (
    "'draft','pending_payment','paid','accepted','preparing','shipped',"
    "'delivered','completed','cancelled','refund_requested','refunded'"
)


def upgrade() -> None:
    op.execute(
        f"""
        DO $$
        DECLARE
            constraint_name text;
        BEGIN
            SELECT con.conname
              INTO constraint_name
              FROM pg_constraint con
              JOIN pg_class rel ON rel.oid = con.conrelid
              JOIN pg_namespace nsp ON nsp.oid = rel.relnamespace
             WHERE rel.relname = 'marketplace_orders'
               AND nsp.nspname = current_schema()
               AND con.contype = 'c'
               AND pg_get_constraintdef(con.oid) LIKE '%status%'
               AND pg_get_constraintdef(con.oid) LIKE '%pending_payment%'
             LIMIT 1;

            IF constraint_name IS NOT NULL THEN
                EXECUTE format('ALTER TABLE marketplace_orders DROP CONSTRAINT %I', constraint_name);
            END IF;

            ALTER TABLE marketplace_orders
                ADD CONSTRAINT marketplace_orders_status_check
                CHECK (status IN ({ORDER_STATUSES}));
        END $$;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE marketplace_orders
            DROP CONSTRAINT IF EXISTS marketplace_orders_status_check;
        ALTER TABLE marketplace_orders
            ADD CONSTRAINT marketplace_orders_status_check
            CHECK (status IN ('draft','pending_payment','paid','accepted','preparing','shipped','delivered','completed','cancelled','refunded'));
        """
    )
