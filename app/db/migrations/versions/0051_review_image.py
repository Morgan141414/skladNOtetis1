"""Add image_url to catalog_item_reviews"""
from alembic import op

revision = "0051_review_image"
down_revision = "0050_merge_heads"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("ALTER TABLE catalog_item_reviews ADD COLUMN IF NOT EXISTS image_url TEXT")
    op.execute("ALTER TABLE catalog_item_reviews ADD COLUMN IF NOT EXISTS reviewer_name TEXT")

def downgrade():
    op.execute("ALTER TABLE catalog_item_reviews DROP COLUMN IF EXISTS image_url")
    op.execute("ALTER TABLE catalog_item_reviews DROP COLUMN IF EXISTS reviewer_name")
