"""Marketplace online payments + installment plans.

Adds the marketplace_payments ledger that backs card payments and the
"рассрочка" (installment) checkout flow. Provider-agnostic: the row stores the
gateway reference and status regardless of which acquirer processed it.

Revision ID: 0048_marketplace_payments
Revises: 0046_merge_supplier_offers_marketplace_inquiry_source
"""

from alembic import op

revision = "0048_marketplace_payments"
down_revision = "0046_merge_supplier_offers_marketplace_inquiry_source"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS marketplace_payments (
            id                  BIGSERIAL PRIMARY KEY,
            actor_id            TEXT NOT NULL,
            inquiry_ids         TEXT,
            amount              NUMERIC(18,2) NOT NULL,
            currency            TEXT NOT NULL DEFAULT 'KZT',
            method              TEXT NOT NULL DEFAULT 'card'
                                CHECK (method IN ('card','installment','wallet','invoice')),
            installment_months  INTEGER NOT NULL DEFAULT 0,
            markup_amount       NUMERIC(18,2) NOT NULL DEFAULT 0,
            total_amount        NUMERIC(18,2) NOT NULL,
            provider            TEXT NOT NULL DEFAULT 'sandbox',
            provider_ref        TEXT,
            status              TEXT NOT NULL DEFAULT 'pending'
                                CHECK (status IN ('pending','processing','paid','failed','refunded','cancelled')),
            redirect_url        TEXT,
            return_url          TEXT,
            failure_reason      TEXT,
            metadata            JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
            paid_at             TIMESTAMPTZ
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_mp_payments_actor ON marketplace_payments(actor_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_mp_payments_status ON marketplace_payments(status)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_mp_payments_provider_ref ON marketplace_payments(provider_ref)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS marketplace_payments")
