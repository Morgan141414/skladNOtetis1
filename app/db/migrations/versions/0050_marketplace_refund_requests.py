"""add marketplace refund request audit table

Revision ID: 0050_marketplace_refund_requests
Revises: 0049_marketplace_refund_requested_status
"""

from alembic import op

revision = "0050_marketplace_refund_requests"
down_revision = "0049_marketplace_refund_requested_status"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_refund_requests (
            id BIGSERIAL PRIMARY KEY,
            order_id BIGINT NOT NULL REFERENCES marketplace_orders(id) ON DELETE CASCADE,
            payment_id BIGINT REFERENCES marketplace_payments(id) ON DELETE SET NULL,
            actor_id TEXT NOT NULL,
            supplier_id BIGINT NOT NULL REFERENCES suppliers(id),
            amount NUMERIC(18,2) NOT NULL CHECK (amount >= 0),
            currency TEXT NOT NULL DEFAULT 'KZT',
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'requested'
                CHECK (status IN ('requested','approved','rejected','processing','refunded','cancelled')),
            reviewer_id TEXT,
            review_reason TEXT,
            reviewed_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_refund_requests_order ON marketplace_refund_requests(order_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_refund_requests_actor ON marketplace_refund_requests(actor_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_refund_requests_supplier_status ON marketplace_refund_requests(supplier_id, status, created_at DESC)")
    op.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_marketplace_refund_requests_active_order
        ON marketplace_refund_requests(order_id)
        WHERE status IN ('requested','approved','processing')
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS marketplace_refund_requests")
