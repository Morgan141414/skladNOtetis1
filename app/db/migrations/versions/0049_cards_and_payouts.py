"""Saved buyer cards (tokenized) and supplier payout accounts.

PCI-DSS note: no card data is stored here by design. The buyer enters the card
on the acquirer's own page; we persist only the gateway *token* plus a display
mask (brand / last4 / expiry). The same holds for supplier payout cards.

Revision ID: 0049_cards_and_payouts
Revises: 0048_marketplace_payments
"""

from alembic import op

revision = "0049_cards_and_payouts"
down_revision = "0048_marketplace_payments"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Buyer saved cards ────────────────────────────────────────────────────
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS marketplace_payment_methods (
            id              BIGSERIAL PRIMARY KEY,
            actor_id        TEXT NOT NULL,
            provider        TEXT NOT NULL DEFAULT 'sandbox',
            provider_token  TEXT,
            provider_ref    TEXT,
            brand           TEXT,
            last4           TEXT,
            exp_month       INTEGER,
            exp_year        INTEGER,
            holder_name     TEXT,
            is_default      BOOLEAN NOT NULL DEFAULT false,
            status          TEXT NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','active','expired','removed','failed')),
            return_url      TEXT,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_mp_methods_actor ON marketplace_payment_methods(actor_id, status)")

    # ── Supplier payout accounts ─────────────────────────────────────────────
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS supplier_payout_accounts (
            id              BIGSERIAL PRIMARY KEY,
            supplier_id     BIGINT NOT NULL,
            account_type    TEXT NOT NULL DEFAULT 'card'
                            CHECK (account_type IN ('card','bank')),
            provider        TEXT NOT NULL DEFAULT 'sandbox',
            provider_token  TEXT,
            provider_ref    TEXT,
            brand           TEXT,
            last4           TEXT,
            exp_month       INTEGER,
            exp_year        INTEGER,
            holder_name     TEXT,
            bank_name       TEXT,
            iban_last4      TEXT,
            is_default      BOOLEAN NOT NULL DEFAULT false,
            status          TEXT NOT NULL DEFAULT 'pending'
                            CHECK (status IN ('pending','active','rejected','removed','failed')),
            return_url      TEXT,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_payout_accounts_supplier ON supplier_payout_accounts(supplier_id, status)")

    # ── Payout ledger (money out to sellers) ─────────────────────────────────
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS marketplace_payouts (
            id                 BIGSERIAL PRIMARY KEY,
            supplier_id        BIGINT NOT NULL,
            payout_account_id  BIGINT,
            payment_id         BIGINT,
            amount             NUMERIC(18,2) NOT NULL,
            commission_amount  NUMERIC(18,2) NOT NULL DEFAULT 0,
            net_amount         NUMERIC(18,2) NOT NULL,
            currency           TEXT NOT NULL DEFAULT 'KZT',
            provider           TEXT NOT NULL DEFAULT 'sandbox',
            provider_ref       TEXT,
            status             TEXT NOT NULL DEFAULT 'pending'
                               CHECK (status IN ('pending','processing','sent','failed','cancelled')),
            failure_reason     TEXT,
            created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
            sent_at            TIMESTAMPTZ
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_payouts_supplier ON marketplace_payouts(supplier_id, status)")
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS uq_payout_payment_supplier "
        "ON marketplace_payouts(payment_id, supplier_id) WHERE payment_id IS NOT NULL"
    )

    # Let a payment remember which saved card was charged.
    op.execute("ALTER TABLE marketplace_payments ADD COLUMN IF NOT EXISTS payment_method_id BIGINT")


def downgrade() -> None:
    op.execute("ALTER TABLE marketplace_payments DROP COLUMN IF EXISTS payment_method_id")
    op.execute("DROP TABLE IF EXISTS marketplace_payouts")
    op.execute("DROP TABLE IF EXISTS supplier_payout_accounts")
    op.execute("DROP TABLE IF EXISTS marketplace_payment_methods")
