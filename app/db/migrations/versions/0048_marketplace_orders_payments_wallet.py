"""marketplace orders payments and seller wallet

Revision ID: 0048_marketplace_orders_payments_wallet
Revises: 0046_merge_supplier_offers_marketplace_inquiry_source, 0047_listing_expiry_promotion
"""

from alembic import op

revision = "0048_marketplace_orders_payments_wallet"
down_revision = ("0046_merge_supplier_offers_marketplace_inquiry_source", "0047_listing_expiry_promotion")
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SEQUENCE IF NOT EXISTS marketplace_order_seq START 1000")
    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_orders (
            id BIGSERIAL PRIMARY KEY,
            order_number TEXT NOT NULL UNIQUE,
            actor_id TEXT NOT NULL,
            supplier_id BIGINT NOT NULL REFERENCES suppliers(id),
            warehouse_id BIGINT REFERENCES warehouses(id),
            source TEXT NOT NULL DEFAULT 'marqet'
                CHECK (source IN ('marqet','qpartner','api')),
            status TEXT NOT NULL DEFAULT 'pending_payment'
                CHECK (status IN ('draft','pending_payment','paid','accepted','preparing','shipped','delivered','completed','cancelled','refunded')),
            currency TEXT NOT NULL DEFAULT 'KZT',
            subtotal_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
            delivery_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
            discount_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
            total_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
            buyer_name TEXT,
            buyer_phone TEXT,
            buyer_email TEXT,
            delivery_address TEXT,
            notes TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            paid_at TIMESTAMPTZ,
            cancelled_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_orders_actor ON marketplace_orders(actor_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_orders_supplier_status ON marketplace_orders(supplier_id, status, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_orders_status ON marketplace_orders(status, created_at DESC)")

    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_order_items (
            id BIGSERIAL PRIMARY KEY,
            order_id BIGINT NOT NULL REFERENCES marketplace_orders(id) ON DELETE CASCADE,
            catalog_item_id BIGINT REFERENCES supplier_catalog_items(id) ON DELETE SET NULL,
            product_id BIGINT REFERENCES products(id) ON DELETE SET NULL,
            product_name TEXT NOT NULL,
            sku TEXT,
            unit TEXT NOT NULL DEFAULT 'шт',
            quantity NUMERIC(18,3) NOT NULL CHECK (quantity > 0),
            unit_price NUMERIC(18,2) NOT NULL CHECK (unit_price >= 0),
            line_total NUMERIC(18,2) NOT NULL CHECK (line_total >= 0),
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_order_items_order ON marketplace_order_items(order_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_order_items_catalog ON marketplace_order_items(catalog_item_id)")

    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_payment_methods (
            id BIGSERIAL PRIMARY KEY,
            actor_id TEXT NOT NULL,
            provider TEXT NOT NULL,
            provider_token TEXT NOT NULL,
            brand TEXT NOT NULL DEFAULT 'unknown',
            last4 TEXT NOT NULL,
            expiry_month INTEGER,
            expiry_year INTEGER,
            holder_name TEXT,
            status TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active','expired','disabled')),
            is_default BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            UNIQUE(provider, provider_token)
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_payment_methods_actor ON marketplace_payment_methods(actor_id, status)")

    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_payments (
            id BIGSERIAL PRIMARY KEY,
            order_id BIGINT NOT NULL REFERENCES marketplace_orders(id) ON DELETE CASCADE,
            actor_id TEXT NOT NULL,
            supplier_id BIGINT NOT NULL REFERENCES suppliers(id),
            payment_method_id BIGINT REFERENCES marketplace_payment_methods(id) ON DELETE SET NULL,
            provider TEXT NOT NULL DEFAULT 'manual',
            provider_payment_id TEXT,
            method TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','requires_action','authorized','paid','failed','cancelled','refunded')),
            amount NUMERIC(18,2) NOT NULL CHECK (amount >= 0),
            currency TEXT NOT NULL DEFAULT 'KZT',
            idempotency_key TEXT,
            payment_url TEXT,
            error_code TEXT,
            error_message TEXT,
            metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            authorized_at TIMESTAMPTZ,
            paid_at TIMESTAMPTZ,
            failed_at TIMESTAMPTZ,
            refunded_at TIMESTAMPTZ
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_payments_order ON marketplace_payments(order_id, created_at DESC)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_payments_actor ON marketplace_payments(actor_id, created_at DESC)")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_marketplace_payments_provider_payment ON marketplace_payments(provider, provider_payment_id) WHERE provider_payment_id IS NOT NULL")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_marketplace_payments_idempotency ON marketplace_payments(actor_id, idempotency_key) WHERE idempotency_key IS NOT NULL")

    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_payment_events (
            id BIGSERIAL PRIMARY KEY,
            payment_id BIGINT REFERENCES marketplace_payments(id) ON DELETE CASCADE,
            provider TEXT NOT NULL,
            provider_event_id TEXT,
            event_type TEXT NOT NULL,
            payload JSONB NOT NULL DEFAULT '{}'::jsonb,
            received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            processed_at TIMESTAMPTZ,
            processing_error TEXT
        )
    """)
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_marketplace_payment_events_provider ON marketplace_payment_events(provider, provider_event_id) WHERE provider_event_id IS NOT NULL")
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_payment_events_payment ON marketplace_payment_events(payment_id, received_at DESC)")

    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_seller_accounts (
            id BIGSERIAL PRIMARY KEY,
            supplier_id BIGINT NOT NULL UNIQUE REFERENCES suppliers(id) ON DELETE CASCADE,
            currency TEXT NOT NULL DEFAULT 'KZT',
            available_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
            pending_amount NUMERIC(18,2) NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_seller_ledger (
            id BIGSERIAL PRIMARY KEY,
            supplier_id BIGINT NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
            order_id BIGINT REFERENCES marketplace_orders(id) ON DELETE SET NULL,
            payment_id BIGINT REFERENCES marketplace_payments(id) ON DELETE SET NULL,
            entry_type TEXT NOT NULL CHECK (entry_type IN ('credit','debit','hold','release','refund','adjust')),
            status TEXT NOT NULL DEFAULT 'posted' CHECK (status IN ('pending','posted','cancelled')),
            amount NUMERIC(18,2) NOT NULL,
            currency TEXT NOT NULL DEFAULT 'KZT',
            description TEXT,
            source_type TEXT,
            source_id TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_seller_ledger_supplier ON marketplace_seller_ledger(supplier_id, created_at DESC)")
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_marketplace_seller_ledger_source ON marketplace_seller_ledger(source_type, source_id, entry_type) WHERE source_type IS NOT NULL AND source_id IS NOT NULL")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS marketplace_seller_ledger")
    op.execute("DROP TABLE IF EXISTS marketplace_seller_accounts")
    op.execute("DROP TABLE IF EXISTS marketplace_payment_events")
    op.execute("DROP TABLE IF EXISTS marketplace_payments")
    op.execute("DROP TABLE IF EXISTS marketplace_payment_methods")
    op.execute("DROP TABLE IF EXISTS marketplace_order_items")
    op.execute("DROP TABLE IF EXISTS marketplace_orders")
    op.execute("DROP SEQUENCE IF EXISTS marketplace_order_seq")
