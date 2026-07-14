"""Add last_seen_at to users, tracking/delivery fields to orders"""
from alembic import op

revision = "0049_online_tracking"
down_revision = "0048_marketplace_orders"
branch_labels = None
depends_on = None


def upgrade():
    # Track when user was last active
    op.execute("""
        ALTER TABLE sklad_users
            ADD COLUMN IF NOT EXISTS last_seen_at TIMESTAMPTZ
    """)

    # Order delivery tracking fields
    op.execute("""
        ALTER TABLE marketplace_orders
            ADD COLUMN IF NOT EXISTS tracking_number TEXT,
            ADD COLUMN IF NOT EXISTS tracking_carrier TEXT,
            ADD COLUMN IF NOT EXISTS estimated_delivery DATE,
            ADD COLUMN IF NOT EXISTS seller_note TEXT
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_users_last_seen ON sklad_users(last_seen_at) WHERE last_seen_at IS NOT NULL")


def downgrade():
    op.execute("ALTER TABLE sklad_users DROP COLUMN IF EXISTS last_seen_at")
    op.execute("""
        ALTER TABLE marketplace_orders
            DROP COLUMN IF EXISTS tracking_number,
            DROP COLUMN IF EXISTS tracking_carrier,
            DROP COLUMN IF EXISTS estimated_delivery,
            DROP COLUMN IF EXISTS seller_note
    """)
