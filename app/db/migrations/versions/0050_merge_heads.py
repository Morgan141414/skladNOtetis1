"""Merge marketplace-orders branch with supplier-offers/inquiry branch"""
from alembic import op

revision = "0050_merge_heads"
down_revision = None
branch_labels = None
depends_on = None

# Merges both heads into one
revises = ("0046_merge_supplier_offers_marketplace_inquiry_source", "0049_online_tracking")


def upgrade():
    pass


def downgrade():
    pass
