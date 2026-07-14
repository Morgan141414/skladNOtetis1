"""marketplace orders tables"""
from alembic import op

revision = "0048_marketplace_orders"
down_revision = "0047_listing_expiry_promotion"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_orders (
            id              BIGSERIAL PRIMARY KEY,
            order_number    TEXT UNIQUE NOT NULL,
            buyer_id        INTEGER REFERENCES sklad_users(id),
            supplier_id     INTEGER REFERENCES suppliers(id),
            status          TEXT NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','confirmed','paid','shipped','delivered','cancelled')),
            payment_method  TEXT NOT NULL DEFAULT 'cod'
                            CHECK (payment_method IN ('cod','kaspi','bank','card_online')),
            payment_status  TEXT NOT NULL DEFAULT 'pending'
                            CHECK (payment_status IN ('pending','awaiting','paid','refunded')),
            total_amount    NUMERIC(18,2),
            buyer_name      TEXT NOT NULL,
            buyer_phone     TEXT NOT NULL,
            delivery_address TEXT NOT NULL,
            notes           TEXT,
            seller_payment_details TEXT,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS marketplace_order_items (
            id              BIGSERIAL PRIMARY KEY,
            order_id        BIGINT NOT NULL REFERENCES marketplace_orders(id) ON DELETE CASCADE,
            catalog_item_id INTEGER REFERENCES supplier_catalog_items(id),
            product_name    TEXT NOT NULL,
            quantity        NUMERIC(18,3) NOT NULL DEFAULT 1,
            unit_price      NUMERIC(18,2),
            unit            TEXT,
            image_url       TEXT
        )
    """)

    op.execute("""
        ALTER TABLE suppliers
            ADD COLUMN IF NOT EXISTS kaspi_phone TEXT,
            ADD COLUMN IF NOT EXISTS bank_iban   TEXT,
            ADD COLUMN IF NOT EXISTS bank_name   TEXT
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_orders_buyer ON marketplace_orders(buyer_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_orders_supplier ON marketplace_orders(supplier_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON marketplace_orders(status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON marketplace_order_items(order_id)")


def downgrade():
    op.execute("DROP TABLE IF EXISTS marketplace_order_items")
    op.execute("DROP TABLE IF EXISTS marketplace_orders")
    op.execute("ALTER TABLE suppliers DROP COLUMN IF EXISTS kaspi_phone, DROP COLUMN IF EXISTS bank_iban, DROP COLUMN IF EXISTS bank_name")
