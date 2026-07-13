from __future__ import annotations

import json
import math
import uuid
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from sqlite3 import Connection, Row
from typing import Any

from app.domain.enums import (
    AuditAction,
    BatchStatus,
    InventoryStatus,
    MovementType,
    QuarantineReviewStatus,
    ReservationStatus,
    StockDocumentStatus,
    StockDocumentType,
)
from app.domain.errors import (
    BatchUnavailableError,
    ConflictError,
    InsufficientStockError,
    InventoryLockedError,
    NotFoundError,
    ValidationError,
)
from app.domain.schemas import (
    CategoryCreate,
    CategoryUpdate,
    DepartmentReturnDocumentCreate,
    DepartmentReturnCreate,
    InventoryCreate,
    InventoryLineCountUpdate,
    ProductCreate,
    ProductUpdate,
    PurchaseRequestCreate,
    PurchaseRequestStatusUpdate,
    BatchRecallCreate,
    QuarantineReviewUpdate,
    ReceiptCreate,
    ReceiptDocumentCreate,
    RepackDocumentCreate,
    ReservationCreate,
    ReservationUseCreate,
    SensorDeviceCreate,
    SensorDeviceUpdate,
    SensorReadingCreate,
    SupplierApplicationCreate,
    SupplierApplicationReview,
    SupplierCreate,
    SupplierUpdate,
    SupplierReturnDocumentCreate,
    SupplierReturnCreate,
    TransferCreate,
    TransferDocumentCreate,
    WarehouseCreate,
    WarehouseUpdate,
    WriteOffCreate,
    WriteOffFefoCreate,
    WriteOffDocumentCreate,
)
import threading
from app.storage.base import WarehouseDatabase
from app.storage.sqlite import decimal_to_db, insert_and_get_id, now_iso


PRODUCT_UNITS = (
    "шт",
    "уп",
    "рулон",
    "флакон",
    "бут",
    "бутылка",
    "пакет",
    "таблетка",
    "капсула",
    "ампула",
    "мл",
    "л",
    "г",
    "кг",
    "м",
    "см",
    "набор",
    "пара",
)


class WarehouseService:
    def __init__(self, database: WarehouseDatabase) -> None:
        self.database = database

    def _close_connection(self, connection: Any) -> None:
        if getattr(self.database, "path", None) != ":memory:":
            connection.close()

    def _is_postgresql(self, connection: Any) -> bool:
        return getattr(connection, "dialect", None) == "postgresql"

    def _date_from_db(self, value: Any) -> date:
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return date.fromisoformat(str(value))

    def _datetime_from_db(self, value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(str(value))

    def list_product_units(self) -> list[str]:
        return list(PRODUCT_UNITS)

    def _normalize_product_unit(self, unit: str) -> str:
        normalized = unit.strip()
        for allowed_unit in PRODUCT_UNITS:
            if normalized.casefold() == allowed_unit.casefold():
                return allowed_unit
        raise ValidationError(f"Unsupported product unit: {unit}")

    def _validate_marketplace_inquiry_source(self, source: str | None) -> str | None:
        if source is None:
            return None
        if source not in {"marqet", "qpartner", "api"}:
            raise ValidationError("Marketplace inquiry source must be marqet, qpartner, or api")
        return source

    def _validate_marketplace_inquiry_status(self, status: str | None) -> str | None:
        if status is None:
            return None
        if status not in {"pending", "responded", "ordered", "closed"}:
            raise ValidationError("Marketplace inquiry status must be pending, responded, ordered, or closed")
        return status

    def create_category(self, data: CategoryCreate, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            category_id = insert_and_get_id(
                connection, "INSERT INTO categories(name, is_active) VALUES (?, ?)", (data.name, 1)
            )
            self._audit(connection, actor_id, AuditAction.CREATE, "category", category_id, data)
            return self._get_by_id(connection, "categories", category_id)

    def list_categories(
        self, limit: int = 100, offset: int = 0, q: str | None = None
    ) -> list[dict[str, Any]]:
        if not q or not q.strip():
            return self._list_table("categories", "name, id", limit, offset, where="is_active = 1")
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        search = q.strip().casefold()
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT * FROM categories
                WHERE is_active = 1
                ORDER BY name, id
                """
            ).fetchall()
            filtered = [
                dict(row)
                for row in rows
                if search in str(row["name"]).casefold()
            ]
            return filtered[safe_offset : safe_offset + safe_limit]
        finally:
            self._close_connection(connection)

    def update_category(
        self, category_id: int, data: CategoryUpdate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "categories", category_id)
            connection.execute(
                "UPDATE categories SET name = ? WHERE id = ?",
                (data.name, category_id),
            )
            updated = self._get_by_id(connection, "categories", category_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "category",
                category_id,
                {"before": before, "after": updated},
            )
            return updated

    def delete_category(self, category_id: int, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "categories", category_id)
            active_products = connection.execute(
                """
                SELECT COUNT(*) AS total
                FROM products
                WHERE category_id = ? AND is_active = 1
                """,
                (category_id,),
            ).fetchone()
            if active_products and int(active_products["total"]) > 0:
                raise ValidationError("Category has active products")
            connection.execute("UPDATE categories SET is_active = ? WHERE id = ?", (0, category_id))
            updated = self._get_by_id(connection, "categories", category_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.DELETE,
                "category",
                category_id,
                {"before": before, "after": updated},
            )
            return updated

    def create_supplier(self, data: SupplierCreate, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            supplier_id = insert_and_get_id(
                connection,
                """
                INSERT INTO suppliers(
                  name, bin, phone, address, rating, is_preferred,
                  contact_person, email, contract_number, contract_expires_on, payment_terms, notes,
                  lat, lng, city, delivery_days
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.name,
                    data.bin,
                    data.phone,
                    data.address,
                    data.rating,
                    1 if data.is_preferred else 0,
                    data.contact_person,
                    data.email,
                    data.contract_number,
                    data.contract_expires_on.isoformat() if data.contract_expires_on else None,
                    data.payment_terms,
                    data.notes,
                    getattr(data, "lat", None),
                    getattr(data, "lng", None),
                    getattr(data, "city", None),
                    getattr(data, "delivery_days", None),
                ),
            )
            self._audit(connection, actor_id, AuditAction.CREATE, "supplier", supplier_id, data)
            return self._get_by_id(connection, "suppliers", supplier_id)

    def list_suppliers(
        self, limit: int = 100, offset: int = 0, q: str | None = None
    ) -> list[dict[str, Any]]:
        if not q or not q.strip():
            return self._list_table("suppliers", "name, id", limit, offset)
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        search = q.strip().casefold()
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT * FROM suppliers
                ORDER BY name, id
                """
            ).fetchall()
            searchable_fields = (
                "name",
                "bin",
                "phone",
                "address",
                "contact_person",
                "email",
                "contract_number",
                "payment_terms",
                "notes",
            )
            filtered = []
            for row in rows:
                item = dict(row)
                haystack = " ".join(str(item.get(field) or "") for field in searchable_fields).casefold()
                if search in haystack:
                    filtered.append(item)
            return filtered[safe_offset : safe_offset + safe_limit]
        finally:
            self._close_connection(connection)

    def update_supplier(
        self, supplier_id: int, data: SupplierUpdate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "suppliers", supplier_id)
            connection.execute(
                """
                UPDATE suppliers
                SET name = ?,
                    bin = ?,
                    phone = ?,
                    address = ?,
                    rating = ?,
                    is_preferred = ?,
                    contact_person = ?,
                    email = ?,
                    contract_number = ?,
                    contract_expires_on = ?,
                    payment_terms = ?,
                    notes = ?,
                    lat = ?,
                    lng = ?,
                    city = ?,
                    delivery_days = ?
                WHERE id = ?
                """,
                (
                    data.name,
                    data.bin,
                    data.phone,
                    data.address,
                    data.rating,
                    1 if data.is_preferred else 0,
                    data.contact_person,
                    data.email,
                    data.contract_number,
                    data.contract_expires_on.isoformat() if data.contract_expires_on else None,
                    data.payment_terms,
                    data.notes,
                    getattr(data, "lat", None),
                    getattr(data, "lng", None),
                    getattr(data, "city", None),
                    getattr(data, "delivery_days", None),
                    supplier_id,
                ),
            )
            updated = self._get_by_id(connection, "suppliers", supplier_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "supplier",
                supplier_id,
                {"before": before, "after": updated},
            )
            return updated

    def submit_supplier_application(
        self, data: SupplierApplicationCreate, actor_id: str = "public"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            existing = connection.execute(
                """
                SELECT id FROM supplier_applications
                WHERE lower(email) = lower(?)
                  AND status IN ('pending', 'needs_changes')
                """,
                (data.email,),
            ).fetchone()
            if existing:
                raise ValidationError("Active supplier application already exists for this email")
            now = now_iso()
            application_id = insert_and_get_id(
                connection,
                """
                INSERT INTO supplier_applications(
                  actor_id, supplier_id, status, name, bin, phone, email,
                  contact_person, address, city, delivery_days, notes,
                  review_reason, submitted_at, reviewed_by, reviewed_at
                ) VALUES (?, NULL, 'pending', ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, NULL, NULL)
                """,
                (
                    actor_id,
                    data.name,
                    data.bin,
                    data.phone,
                    data.email,
                    data.contact_person,
                    data.address,
                    data.city,
                    data.delivery_days,
                    data.notes,
                    now,
                ),
            )
            application = self._get_supplier_application(connection, application_id)
            self._audit(connection, actor_id, AuditAction.CREATE, "supplier_application", application_id, application)
            return application

    def get_supplier_application(self, application_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_supplier_application(connection, application_id)
        finally:
            self._close_connection(connection)

    def list_supplier_applications(
        self, status: str | None = None, limit: int = 100, offset: int = 0
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        params: tuple[Any, ...] = ()
        where = ""
        if status:
            where = "WHERE sa.status = ?"
            params = (status,)
        connection = self.database.connect()
        try:
            rows = connection.execute(
                f"""
                SELECT sa.*, s.name AS supplier_name
                FROM supplier_applications sa
                LEFT JOIN suppliers s ON s.id = sa.supplier_id
                {where}
                ORDER BY sa.submitted_at DESC, sa.id DESC
                LIMIT ? OFFSET ?
                """,
                (*params, safe_limit, safe_offset),
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_supplier_applications(self, status: str | None = None) -> int:
        connection = self.database.connect()
        try:
            if status:
                row = connection.execute(
                    "SELECT COUNT(*) AS total FROM supplier_applications WHERE status = ?",
                    (status,),
                ).fetchone()
            else:
                row = connection.execute("SELECT COUNT(*) AS total FROM supplier_applications").fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def get_my_supplier_applications(self, actor_id: str) -> list[dict[str, Any]]:
        """Return applications submitted by this actor (tetis-actor:{actor_id} or actor_id directly)."""
        connection = self.database.connect()
        patterns = [f"tetis-actor:{actor_id}", actor_id]
        rows = connection.execute(
            """
            SELECT id, name, bin, email, phone, contact_person, city, address,
                   delivery_days, notes, status, actor_id, review_reason,
                   reviewed_by, reviewed_at, supplier_id, submitted_at
            FROM supplier_applications
            WHERE actor_id IN (?, ?)
            ORDER BY id DESC
            """,
            tuple(patterns),
        ).fetchall()
        return [dict(r) for r in rows]

    def resubmit_supplier_application(
        self, application_id: int, data: dict[str, Any], actor_id: str
    ) -> dict[str, Any]:
        """Update application fields and reset status to pending (only allowed if needs_changes)."""
        with self.database.transaction() as connection:
            app = self._get_supplier_application(connection, application_id)
            # Verify actor owns this application
            expected = [f"tetis-actor:{actor_id}", actor_id]
            if app.get("actor_id") not in expected:
                raise PermissionError("Cannot edit another actor's application")
            if app["status"] != "needs_changes":
                raise ValueError(f"Cannot resubmit application with status '{app['status']}'")
            update_fields = {k: v for k, v in data.items() if k in (
                "name", "bin", "email", "phone", "contact_person",
                "city", "address", "delivery_days", "notes"
            ) if v is not None}
            if update_fields:
                set_clause = ", ".join(f"{k} = ?" for k in update_fields)
                connection.execute(
                    f"UPDATE supplier_applications SET {set_clause}, status = 'pending', review_reason = NULL, reviewed_by = NULL, reviewed_at = NULL WHERE id = ?",
                    (*update_fields.values(), application_id),
                )
            else:
                connection.execute(
                    "UPDATE supplier_applications SET status = 'pending', review_reason = NULL, reviewed_by = NULL, reviewed_at = NULL WHERE id = ?",
                    (application_id,),
                )
            return self._get_supplier_application(connection, application_id)

    def get_supplier_by_id(self, supplier_id: int) -> dict[str, Any]:
        """Get a single supplier record by ID."""
        connection = self.database.connect()
        row = connection.execute(
            """
            SELECT id, name, bin, email, phone, contact_person, city, address,
                   delivery_days, rating, notes, is_preferred, contract_number,
                   contract_expires_on, payment_terms, lat, lng,
                   bank_details, website, inn, is_verified, verified_at, legal_name, verification_comment
            FROM suppliers WHERE id = ?
            """,
            (supplier_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"Supplier {supplier_id} not found")
        return dict(row)

    def update_supplier_self(
        self, supplier_id: int, data: dict[str, Any], actor_id: str
    ) -> dict[str, Any]:
        """Update supplier's own profile — only contact fields, not name/rating/contract."""
        allowed = {"email", "phone", "contact_person", "city", "address", "delivery_days", "notes", "bank_details", "website", "inn"}
        updates = {k: v for k, v in data.items() if k in allowed and v is not None}
        if not updates:
            return self.get_supplier_by_id(supplier_id)
        with self.database.transaction() as connection:
            set_clause = ", ".join(f"{k} = ?" for k in updates)
            connection.execute(
                f"UPDATE suppliers SET {set_clause} WHERE id = ?",
                (*updates.values(), supplier_id),
            )
            row = connection.execute(
                """
                SELECT id, name, bin, email, phone, contact_person, city, address,
                       delivery_days, rating, notes, is_preferred, contract_number,
                       contract_expires_on, payment_terms, lat, lng,
                       bank_details, website, inn
                FROM suppliers WHERE id = ?
                """,
                (supplier_id,),
            ).fetchone()
            return dict(row) if row else {}

    def add_supplier_verification_doc(
        self, supplier_id: int, doc_type: str, file_url: str,
        original_name: str | None, actor_id: str
    ) -> dict:
        with self.database.transaction() as conn:
            doc_id = insert_and_get_id(
                conn,
                """INSERT INTO supplier_verification_docs
                   (supplier_id, doc_type, file_url, original_name, uploaded_by)
                   VALUES (?, ?, ?, ?, ?)""",
                (supplier_id, doc_type, file_url, original_name, actor_id),
            )
            row = conn.execute(
                "SELECT * FROM supplier_verification_docs WHERE id = ?", (doc_id,)
            ).fetchone()
            return dict(row) if row else {}

    def list_supplier_verification_docs(self, supplier_id: int) -> list[dict]:
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """SELECT id, supplier_id, doc_type, file_url, original_name, uploaded_at, uploaded_by
                   FROM supplier_verification_docs
                   WHERE supplier_id = ?
                   ORDER BY uploaded_at""",
                (supplier_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def delete_supplier_verification_doc(self, doc_id: int, supplier_id: int) -> None:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id FROM supplier_verification_docs WHERE id = ? AND supplier_id = ?",
                (doc_id, supplier_id)
            ).fetchone()
            if row is None:
                raise NotFoundError(f"Document {doc_id} not found")
            conn.execute("DELETE FROM supplier_verification_docs WHERE id = ?", (doc_id,))

    def set_supplier_verified(
        self, supplier_id: int, is_verified: bool, comment: str | None, actor_id: str
    ) -> dict:
        with self.database.transaction() as conn:
            if is_verified:
                conn.execute(
                    """UPDATE suppliers SET is_verified = TRUE, verified_at = NOW(),
                       verification_comment = ? WHERE id = ?""",
                    (comment, supplier_id),
                )
            else:
                conn.execute(
                    """UPDATE suppliers SET is_verified = FALSE, verified_at = NULL,
                       verification_comment = ? WHERE id = ?""",
                    (comment, supplier_id),
                )
            row = conn.execute(
                """SELECT id, name, bin, email, phone, city, is_verified, verified_at,
                          legal_name, verification_comment
                   FROM suppliers WHERE id = ?""",
                (supplier_id,)
            ).fetchone()
            return dict(row) if row else {}

    def create_purchase_order(
        self, inquiry_id: int, actor_id: str, buyer_data: dict
    ) -> dict:
        """Create or return existing PO for an inquiry."""
        with self.database.transaction() as conn:
            inq = conn.execute(
                """SELECT mi.*, ci.product_name, ci.unit, s.name AS supplier_name,
                          s.bin AS supplier_bin, s.address AS supplier_address,
                          s.phone AS supplier_phone, s.email AS supplier_email,
                          s.city AS supplier_city
                   FROM marketplace_inquiries mi
                   JOIN supplier_catalog_items ci ON ci.id = mi.catalog_item_id
                   JOIN suppliers s ON s.id = mi.supplier_id
                   WHERE mi.id = ? AND mi.actor_id = ?""",
                (inquiry_id, actor_id)
            ).fetchone()
            if inq is None:
                raise PermissionError("Inquiry not found or not yours")
            # Return existing PO if already created
            existing = conn.execute(
                "SELECT * FROM purchase_orders WHERE inquiry_id = ?", (inquiry_id,)
            ).fetchone()
            if existing:
                return dict(existing)
            # Generate PO number: PO-YYYY-NNNNNN
            from datetime import datetime as _dt
            year = _dt.now().year
            seq = conn.execute("SELECT nextval('purchase_order_seq') AS n").fetchone()["n"]
            po_number = f"PO-{year}-{seq:06d}"
            po_id = insert_and_get_id(
                conn,
                """INSERT INTO purchase_orders
                   (po_number, inquiry_id, buyer_name, buyer_bin, buyer_address,
                    buyer_contact, delivery_address, payment_terms, notes, status,
                    delivery_type, delivery_price, delivery_included, escrow_amount)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?, ?)""",
                (
                    po_number,
                    inquiry_id,
                    buyer_data.get("buyer_name"),
                    buyer_data.get("buyer_bin"),
                    buyer_data.get("buyer_address"),
                    buyer_data.get("buyer_contact"),
                    buyer_data.get("delivery_address"),
                    buyer_data.get("payment_terms", "По договорённости"),
                    buyer_data.get("notes"),
                    buyer_data.get("delivery_type"),
                    buyer_data.get("delivery_price"),
                    buyer_data.get("delivery_included", False),
                    buyer_data.get("escrow_amount"),
                ),
            )
            # Also mark inquiry as ordered if pending/responded
            if inq["status"] in ("pending", "responded"):
                conn.execute(
                    "UPDATE marketplace_inquiries SET status = 'ordered' WHERE id = ?",
                    (inquiry_id,)
                )
            row = conn.execute("SELECT * FROM purchase_orders WHERE id = ?", (po_id,)).fetchone()
            return dict(row) if row else {}

    def get_purchase_order(self, inquiry_id: int, actor_id: str) -> dict:
        connection = self.database.connect()
        try:
            inq = connection.execute(
                """SELECT mi.*, ci.product_name, ci.unit, ci.description AS item_description,
                          ci.image_url,
                          s.name AS supplier_name, s.bin AS supplier_bin,
                          s.address AS supplier_address, s.phone AS supplier_phone,
                          s.email AS supplier_email, s.city AS supplier_city,
                          s.bank_details AS supplier_bank_details,
                          s.inn AS supplier_inn, s.is_verified AS supplier_verified,
                          w.name AS warehouse_name
                   FROM marketplace_inquiries mi
                   JOIN supplier_catalog_items ci ON ci.id = mi.catalog_item_id
                   JOIN suppliers s ON s.id = mi.supplier_id
                   LEFT JOIN warehouses w ON w.id = mi.warehouse_id
                   WHERE mi.id = ? AND mi.actor_id = ?""",
                (inquiry_id, actor_id)
            ).fetchone()
            if inq is None:
                raise PermissionError("Inquiry not found or not yours")
            po = connection.execute(
                "SELECT * FROM purchase_orders WHERE inquiry_id = ?", (inquiry_id,)
            ).fetchone()
            result = {"inquiry": dict(inq), "po": dict(po) if po else None}
            return result
        finally:
            self._close_connection(connection)

    def list_catalog_categories(self, parent_id: int | None = None) -> list[dict]:
        """Return all categories optionally filtered by parent."""
        connection = self.database.connect()
        try:
            if parent_id is not None:
                rows = connection.execute(
                    "SELECT id, parent_id, name, slug, icon, sort_order FROM catalog_categories WHERE parent_id = ? ORDER BY sort_order, name",
                    (parent_id,)
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT id, parent_id, name, slug, icon, sort_order FROM catalog_categories ORDER BY sort_order, name"
                ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def create_catalog_category(self, data: dict, actor_id: str) -> dict:
        import re
        name = (data.get("name") or "").strip()
        if not name:
            raise ValidationError("Category name is required")
        slug = data.get("slug") or re.sub(r"[^a-z0-9-]", "-", name.lower().strip())
        with self.database.transaction() as conn:
            cat_id = insert_and_get_id(
                conn,
                "INSERT INTO catalog_categories (parent_id, name, slug, icon, sort_order) VALUES (?, ?, ?, ?, ?)",
                (data.get("parent_id"), name, slug, data.get("icon"), data.get("sort_order", 0)),
            )
            row = conn.execute("SELECT * FROM catalog_categories WHERE id = ?", (cat_id,)).fetchone()
            return dict(row) if row else {}

    def get_price_tiers(self, catalog_item_id: int) -> list[dict]:
        """Get volume pricing tiers for a catalog item."""
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """SELECT id, catalog_item_id, min_quantity, unit_price, label, created_at
                   FROM catalog_item_price_tiers
                   WHERE catalog_item_id = ?
                   ORDER BY min_quantity""",
                (catalog_item_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def set_price_tiers(self, catalog_item_id: int, supplier_id: int, tiers: list[dict]) -> list[dict]:
        """Replace all price tiers for a catalog item."""
        with self.database.transaction() as conn:
            # Verify ownership
            item = conn.execute(
                "SELECT id FROM supplier_catalog_items WHERE id = ? AND supplier_id = ?",
                (catalog_item_id, supplier_id)
            ).fetchone()
            if item is None:
                raise PermissionError("Catalog item not found or not yours")
            # Validate tiers
            for t in tiers:
                if float(t.get("min_quantity", 0)) <= 0:
                    raise ValidationError("min_quantity must be > 0")
                if float(t.get("unit_price", 0)) <= 0:
                    raise ValidationError("unit_price must be > 0")
            # Replace
            conn.execute(
                "DELETE FROM catalog_item_price_tiers WHERE catalog_item_id = ?",
                (catalog_item_id,)
            )
            for t in tiers:
                conn.execute(
                    """INSERT INTO catalog_item_price_tiers (catalog_item_id, min_quantity, unit_price, label)
                       VALUES (?, ?, ?, ?)""",
                    (catalog_item_id, float(t["min_quantity"]), float(t["unit_price"]), t.get("label"))
                )
            rows = conn.execute(
                "SELECT * FROM catalog_item_price_tiers WHERE catalog_item_id = ? ORDER BY min_quantity",
                (catalog_item_id,)
            ).fetchall()
            return [dict(r) for r in rows]

    def resolve_price_for_quantity(self, catalog_item_id: int, quantity: float) -> float | None:
        """Return best (lowest) unit price for a given quantity using tier pricing."""
        connection = self.database.connect()
        try:
            item = connection.execute(
                "SELECT unit_price FROM supplier_catalog_items WHERE id = ?",
                (catalog_item_id,)
            ).fetchone()
            if item is None:
                return None
            base_price = float(item["unit_price"]) if item["unit_price"] else None
            tiers = connection.execute(
                """SELECT unit_price FROM catalog_item_price_tiers
                   WHERE catalog_item_id = ? AND min_quantity <= ?
                   ORDER BY min_quantity DESC LIMIT 1""",
                (catalog_item_id, quantity)
            ).fetchone()
            if tiers:
                tier_price = float(tiers["unit_price"])
                return tier_price if (base_price is None or tier_price < base_price) else base_price
            return base_price
        finally:
            self._close_connection(connection)

    # ── Supplier catalog (marketplace) ──────────────────────────────────────

    def list_supplier_catalog(
        self,
        supplier_id: int | None = None,
        category: str | None = None,
        search: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        active_only: bool = True,
        sort: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Any]:
        where = []
        params: list[Any] = []
        if active_only:
            where.append("ci.is_active = TRUE")
        if supplier_id is not None:
            where.append("ci.supplier_id = ?")
            params.append(supplier_id)
        if category:
            where.append("ci.category = ?")
            params.append(category)
        if search:
            # Use trigram similarity if available, fallback to ILIKE
            where.append("((ci.product_name || ' ' || COALESCE(ci.sku,'') || ' ' || COALESCE(ci.description,'') || ' ' || COALESCE(ci.category,'')) ILIKE ?)")
            params.extend([f"%{search}%"])
        if min_price is not None:
            where.append("ci.unit_price >= ?")
            params.append(min_price)
        if max_price is not None:
            where.append("ci.unit_price <= ?")
            params.append(max_price)
        where_clause = f"WHERE {' AND '.join(where)}" if where else ""
        _sort_map = {
            "price_asc": "ci.unit_price ASC",
            "price_desc": "ci.unit_price DESC",
            "delivery_asc": "COALESCE(ci.delivery_days, s.delivery_days, 999) ASC",
            "name_asc": "ci.product_name ASC",
        }
        order_clause = _sort_map.get(sort or "", "ci.updated_at DESC")
        connection = self.database.connect()
        try:
            total_row = connection.execute(
                f"SELECT COUNT(*) AS n FROM supplier_catalog_items ci JOIN suppliers s ON s.id = ci.supplier_id {where_clause}", tuple(params)
            ).fetchone()
            total = total_row["n"] if total_row else 0
            rows = connection.execute(
                f"""
                SELECT ci.*, s.name AS supplier_name, s.city AS supplier_city,
                       s.rating AS supplier_rating, s.phone AS supplier_phone,
                       s.email AS supplier_email, s.delivery_days AS supplier_delivery_days,
                       s.is_verified AS supplier_is_verified,
                       p.name AS linked_product_name,
                       r.avg_rating, r.review_count
                FROM supplier_catalog_items ci
                JOIN suppliers s ON s.id = ci.supplier_id
                LEFT JOIN products p ON p.id = ci.product_id
                LEFT JOIN (
                    SELECT catalog_item_id, ROUND(AVG(rating), 1) AS avg_rating, COUNT(*) AS review_count
                    FROM catalog_item_reviews WHERE status = 'approved' GROUP BY catalog_item_id
                ) r ON r.catalog_item_id = ci.id
                {where_clause}
                ORDER BY {order_clause}
                LIMIT ? OFFSET ?
                """,
                tuple(params) + (limit, offset),
            ).fetchall()
            return {"items": [dict(r) for r in rows], "total": total}
        finally:
            self._close_connection(connection)

    def get_catalog_item(self, item_id: int) -> dict[str, Any] | None:
        connection = self.database.connect()
        try:
            row = connection.execute(
                """
                SELECT ci.*, s.name AS supplier_name, s.city AS supplier_city,
                       s.rating AS supplier_rating, s.phone AS supplier_phone,
                       s.email AS supplier_email, s.delivery_days AS supplier_delivery_days,
                       s.is_verified AS supplier_is_verified,
                       r.avg_rating, r.review_count
                FROM supplier_catalog_items ci
                JOIN suppliers s ON s.id = ci.supplier_id
                LEFT JOIN (
                    SELECT catalog_item_id, ROUND(AVG(rating), 1) AS avg_rating, COUNT(*) AS review_count
                    FROM catalog_item_reviews WHERE status = 'approved' GROUP BY catalog_item_id
                ) r ON r.catalog_item_id = ci.id
                WHERE ci.id = ?
                """,
                (item_id,),
            ).fetchone()
            return dict(row) if row else None
        finally:
            self._close_connection(connection)

    # ── Catalog item reviews (product-level ratings, like Kaspi/Amazon) ─────

    def create_catalog_item_review(
        self, catalog_item_id: int, rating: int, comment: str | None, reviewer_id: str
    ) -> dict[str, Any]:
        if not 1 <= rating <= 5:
            raise ValidationError("Rating must be between 1 and 5")
        with self.database.transaction() as connection:
            self._require(connection, "supplier_catalog_items", catalog_item_id)
            row = connection.execute(
                """INSERT INTO catalog_item_reviews (catalog_item_id, rating, comment, reviewer_id, status)
                   VALUES (?, ?, ?, ?, 'approved')
                   RETURNING *""",
                (catalog_item_id, rating, comment, reviewer_id),
            ).fetchone()
            return dict(row)

    def list_catalog_item_reviews(self, catalog_item_id: int, status: str = "approved") -> list[dict[str, Any]]:
        connection = self.database.connect()
        try:
            rows = connection.execute(
                "SELECT * FROM catalog_item_reviews WHERE catalog_item_id = ? AND status = ? ORDER BY created_at DESC",
                (catalog_item_id, status),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def moderate_catalog_item_review(self, review_id: int, action: str) -> dict[str, Any]:
        if action not in ("approve", "reject"):
            raise ValidationError("action must be approve or reject")
        with self.database.transaction() as connection:
            row = connection.execute("SELECT * FROM catalog_item_reviews WHERE id = ?", (review_id,)).fetchone()
            if not row:
                raise NotFoundError(f"catalog_item_reviews#{review_id} not found")
            new_status = "approved" if action == "approve" else "rejected"
            connection.execute("UPDATE catalog_item_reviews SET status = ? WHERE id = ?", (new_status, review_id))
            updated = connection.execute("SELECT * FROM catalog_item_reviews WHERE id = ?", (review_id,)).fetchone()
            return dict(updated)

    def create_catalog_item(self, supplier_id: int, data: dict[str, Any]) -> dict[str, Any]:
        with self.database.transaction() as conn:
            row_id = insert_and_get_id(
                conn,
                """INSERT INTO supplier_catalog_items
                   (supplier_id, product_id, product_name, sku, unit, unit_price,
                    min_order_qty, stock_qty, delivery_days, category, description, is_active,
                    valid_until, condition, delivery_type, delivery_price,
                    delivery_included, delivery_regions)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    supplier_id,
                    data.get("product_id"),
                    data["product_name"],
                    data.get("sku"),
                    data.get("unit", "шт"),
                    data["unit_price"],
                    data.get("min_order_qty", 1),
                    data.get("stock_qty"),
                    data.get("delivery_days"),
                    data.get("category"),
                    data.get("description"),
                    data.get("is_active", True),
                    data.get("valid_until"),
                    data.get("condition", "new"),
                    data.get("delivery_type", "buyer_arranges"),
                    data.get("delivery_price"),
                    data.get("delivery_included", False),
                    data.get("delivery_regions"),
                ),
            )
            row = conn.execute("SELECT * FROM supplier_catalog_items WHERE id = ?", (row_id,)).fetchone()
            return dict(row) if row else {}

    def update_catalog_item(self, item_id: int, supplier_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        allowed = {
            "product_name", "sku", "unit", "unit_price", "min_order_qty",
            "stock_qty", "delivery_days", "category", "description", "is_active", "product_id",
            "valid_until", "condition", "delivery_type", "delivery_price",
            "delivery_included", "delivery_regions",
        }
        updates = {k: v for k, v in data.items() if k in allowed}
        if not updates:
            return self.get_catalog_item(item_id)
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id, supplier_id FROM supplier_catalog_items WHERE id = ?", (item_id,)
            ).fetchone()
            if row is None or row["supplier_id"] != supplier_id:
                return None
            updates["updated_at"] = now_iso()
            set_clause = ", ".join(f"{k} = ?" for k in updates)
            conn.execute(
                f"UPDATE supplier_catalog_items SET {set_clause} WHERE id = ?",
                (*updates.values(), item_id),
            )
            updated = conn.execute("SELECT * FROM supplier_catalog_items WHERE id = ?", (item_id,)).fetchone()
            return dict(updated) if updated else None

    def delete_catalog_item(self, item_id: int, supplier_id: int) -> bool:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id, supplier_id FROM supplier_catalog_items WHERE id = ?", (item_id,)
            ).fetchone()
            if row is None or row["supplier_id"] != supplier_id:
                return False
            conn.execute("DELETE FROM supplier_catalog_items WHERE id = ?", (item_id,))
            return True

    # ── Gov procurement ───────────────────────────────────────────────────────

    _GOV_STATUS_NEXT = {"demand": "accepting", "accepting": "closed"}

    def advance_gov_status(self, request_id: int, actor_id: str) -> dict[str, Any]:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id, is_gov_procurement, gov_status FROM purchase_requests WHERE id = ?",
                (request_id,)
            ).fetchone()
            if row is None:
                raise NotFoundError(f"purchase_requests#{request_id} not found")
            if not row["is_gov_procurement"]:
                raise ValidationError("This request is not a gov procurement request")
            current = row["gov_status"] or "demand"
            nxt = self._GOV_STATUS_NEXT.get(current)
            if nxt is None:
                raise ValidationError(f"Cannot advance from status '{current}'")
            conn.execute(
                "UPDATE purchase_requests SET gov_status = ? WHERE id = ?",
                (nxt, request_id)
            )
            updated = conn.execute("SELECT * FROM purchase_requests WHERE id = ?", (request_id,)).fetchone()
            return dict(updated)

    def add_gov_feedback(
        self, request_id: int, feedback_text: str, rating: int, actor_id: str
    ) -> dict[str, Any]:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id, is_gov_procurement, gov_status FROM purchase_requests WHERE id = ?",
                (request_id,)
            ).fetchone()
            if row is None:
                raise NotFoundError(f"purchase_requests#{request_id} not found")
            if not row["is_gov_procurement"]:
                raise ValidationError("Not a gov procurement request")
            if row["gov_status"] != "closed":
                raise ValidationError("Feedback can only be added when status is 'closed'")
            conn.execute(
                """UPDATE purchase_requests
                   SET gov_feedback_text = ?, gov_feedback_rating = ?, gov_status = 'feedback'
                   WHERE id = ?""",
                (feedback_text, rating, request_id)
            )
            updated = conn.execute("SELECT * FROM purchase_requests WHERE id = ?", (request_id,)).fetchone()
            return dict(updated)

    # ── Purchase Order escrow + delivery ─────────────────────────────────────

    def update_po_escrow(self, inquiry_id: int, action: str, actor_id: str) -> dict[str, Any]:
        import datetime as _dt
        valid = {"reserve", "release", "refund"}
        if action not in valid:
            raise ValidationError(f"action must be one of {valid}")
        with self.database.transaction() as conn:
            inq = conn.execute(
                "SELECT id, actor_id FROM marketplace_inquiries WHERE id = ?", (inquiry_id,)
            ).fetchone()
            if inq is None or inq["actor_id"] != actor_id:
                raise PermissionError("Inquiry not found or not yours")
            po = conn.execute(
                "SELECT id, escrow_status FROM purchase_orders WHERE inquiry_id = ?", (inquiry_id,)
            ).fetchone()
            if po is None:
                raise NotFoundError("Purchase order not found — create it first")
            now = _dt.datetime.now(_dt.UTC).isoformat()
            if action == "reserve":
                conn.execute(
                    """UPDATE purchase_orders
                       SET escrow_status = 'reserved', escrow_reserved_at = ?
                       WHERE id = ?""",
                    (now, po["id"])
                )
            elif action == "release":
                conn.execute(
                    """UPDATE purchase_orders
                       SET escrow_status = 'released', escrow_released_at = ?
                       WHERE id = ?""",
                    (now, po["id"])
                )
            else:  # refund
                conn.execute(
                    """UPDATE purchase_orders
                       SET escrow_status = 'refunded', escrow_released_at = ?
                       WHERE id = ?""",
                    (now, po["id"])
                )
            updated = conn.execute("SELECT * FROM purchase_orders WHERE id = ?", (po["id"],)).fetchone()
            return dict(updated)

    def update_po_delivery(
        self, inquiry_id: int, data: dict[str, Any], actor_id: str
    ) -> dict[str, Any]:
        import datetime as _dt
        with self.database.transaction() as conn:
            inq = conn.execute(
                "SELECT id, actor_id FROM marketplace_inquiries WHERE id = ?", (inquiry_id,)
            ).fetchone()
            if inq is None or inq["actor_id"] != actor_id:
                raise PermissionError("Inquiry not found or not yours")
            po = conn.execute(
                "SELECT id, escrow_status FROM purchase_orders WHERE inquiry_id = ?", (inquiry_id,)
            ).fetchone()
            if po is None:
                raise NotFoundError("Purchase order not found")
            allowed = {
                "delivery_status", "delivery_tracking_number",
                "delivery_type", "delivery_price", "delivery_included",
            }
            updates = {k: v for k, v in data.items() if k in allowed}
            now = _dt.datetime.now(_dt.UTC).isoformat()
            if updates.get("delivery_status") == "shipped":
                updates["delivery_shipped_at"] = now
            elif updates.get("delivery_status") == "delivered":
                updates["delivery_delivered_at"] = now
                if po.get("escrow_status") == "held":
                    updates["escrow_status"] = "released"
                    updates["escrow_released_at"] = now
            if updates:
                set_clause = ", ".join(f"{k} = ?" for k in updates)
                conn.execute(
                    f"UPDATE purchase_orders SET {set_clause} WHERE id = ?",
                    (*updates.values(), po["id"])
                )
            updated = conn.execute("SELECT * FROM purchase_orders WHERE id = ?", (po["id"],)).fetchone()
            return dict(updated)

    # ── Auction escrow ────────────────────────────────────────────────────────

    def update_auction_escrow(self, auction_id: int, action: str, actor_id: str) -> dict[str, Any]:
        import datetime as _dt
        valid = {"reserve", "release", "refund"}
        if action not in valid:
            raise ValidationError(f"action must be one of {valid}")
        with self.database.transaction() as conn:
            auction = conn.execute(
                "SELECT id, status, winner_supplier_id, escrow_status FROM auctions WHERE id = ?",
                (auction_id,)
            ).fetchone()
            if auction is None:
                raise NotFoundError(f"auctions#{auction_id} not found")
            now = _dt.datetime.now(_dt.UTC).isoformat()
            if action == "reserve":
                conn.execute(
                    """UPDATE auctions
                       SET escrow_status = 'reserved', escrow_reserved_at = ?
                       WHERE id = ?""",
                    (now, auction_id)
                )
            elif action == "release":
                conn.execute(
                    """UPDATE auctions
                       SET escrow_status = 'released', escrow_released_at = ?
                       WHERE id = ?""",
                    (now, auction_id)
                )
            else:
                conn.execute(
                    """UPDATE auctions
                       SET escrow_status = 'refunded', escrow_released_at = ?
                       WHERE id = ?""",
                    (now, auction_id)
                )
            updated = conn.execute("SELECT * FROM auctions WHERE id = ?", (auction_id,)).fetchone()
            return dict(updated)

    def list_suppliers_directory(
        self,
        city: str | None = None,
        category: str | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Return all suppliers that are active in the marketplace (portal-enabled or have catalog items)."""
        where = ["(s.portal_access_enabled = TRUE OR EXISTS (SELECT 1 FROM supplier_catalog_items ci2 WHERE ci2.supplier_id = s.id AND ci2.is_active = TRUE))"]
        params: list[Any] = []
        if city:
            where.append("s.city ILIKE ?")
            params.append(f"%{city}%")
        if search:
            where.append("(s.name ILIKE ? OR s.contact_person ILIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        if category:
            where.append("EXISTS (SELECT 1 FROM supplier_catalog_items ci WHERE ci.supplier_id = s.id AND ci.category = ? AND ci.is_active = TRUE)")
            params.append(category)
        where_clause = f"WHERE {' AND '.join(where)}"
        connection = self.database.connect()
        try:
            total_row = connection.execute(f"SELECT COUNT(*) AS n FROM suppliers s {where_clause}", tuple(params)).fetchone()
            total = total_row["n"] if total_row else 0
            rows = connection.execute(
                f"""
                SELECT s.id, s.name, s.city, s.address, s.phone, s.email,
                       s.contact_person, s.delivery_days, s.rating, s.notes,
                       s.is_preferred, s.payment_terms, s.is_verified,
                       COUNT(ci.id) FILTER (WHERE ci.is_active) AS catalog_items_count,
                       MIN(ci.unit_price) AS min_price,
                       MAX(ci.unit_price) AS max_price,
                       array_agg(DISTINCT ci.category) FILTER (WHERE ci.category IS NOT NULL AND ci.is_active) AS categories
                FROM suppliers s
                LEFT JOIN supplier_catalog_items ci ON ci.supplier_id = s.id
                {where_clause}
                GROUP BY s.id
                ORDER BY s.is_preferred DESC, s.rating DESC NULLS LAST, catalog_items_count DESC, s.id
                LIMIT ? OFFSET ?
                """,
                tuple(params) + (limit, offset),
            ).fetchall()
            return {"items": [dict(r) for r in rows], "total": total}
        finally:
            self._close_connection(connection)

    def get_supplier_stats(self, supplier_id: int) -> dict[str, Any]:
        """Return dashboard stats for a supplier."""
        connection = self.database.connect()
        try:
            catalog_row = connection.execute(
                "SELECT COUNT(*) AS total, COUNT(*) FILTER (WHERE is_active) AS active FROM supplier_catalog_items WHERE supplier_id = ?",
                (supplier_id,)
            ).fetchone()
            inquiry_row = connection.execute(
                "SELECT COUNT(*) AS total, COUNT(*) FILTER (WHERE status = 'pending') AS pending FROM marketplace_inquiries WHERE supplier_id = ?",
                (supplier_id,)
            ).fetchone()
            auction_row = connection.execute(
                "SELECT COUNT(*) AS won FROM auctions WHERE winner_supplier_id = ?",
                (supplier_id,)
            ).fetchone()
            review_row = connection.execute(
                "SELECT COUNT(*) AS total, AVG(rating) AS avg FROM supplier_reviews WHERE supplier_id = ? AND status = 'approved'",
                (supplier_id,)
            ).fetchone()
            shipment_row = connection.execute(
                "SELECT COUNT(*) AS active FROM shipments WHERE supplier_id = ? AND status IN ('in_transit','delayed')",
                (supplier_id,)
            ).fetchone()
            return {
                "catalog_total": catalog_row["total"] if catalog_row else 0,
                "catalog_active": catalog_row["active"] if catalog_row else 0,
                "inquiries_total": inquiry_row["total"] if inquiry_row else 0,
                "inquiries_pending": inquiry_row["pending"] if inquiry_row else 0,
                "auctions_won": auction_row["won"] if auction_row else 0,
                "reviews_total": review_row["total"] if review_row else 0,
                "reviews_avg": float(review_row["avg"]) if review_row and review_row["avg"] else None,
                "shipments_active": shipment_row["active"] if shipment_row else 0,
            }
        finally:
            self._close_connection(connection)

    def get_supplier_profile(self, supplier_id: int) -> dict[str, Any] | None:
        """Public storefront view of a supplier: profile, rating, catalog and reviews."""
        connection = self.database.connect()
        try:
            supplier = connection.execute(
                """SELECT id, name, legal_name, city, address, phone, email, contact_person,
                          delivery_days, rating, is_preferred, is_verified, verified_at, payment_terms
                   FROM suppliers WHERE id = ?""",
                (supplier_id,),
            ).fetchone()
            if supplier is None:
                return None
            stats = connection.execute(
                """SELECT COUNT(*) FILTER (WHERE is_active) AS catalog_items_count,
                          MIN(unit_price) FILTER (WHERE is_active) AS min_price,
                          MAX(unit_price) FILTER (WHERE is_active) AS max_price
                   FROM supplier_catalog_items WHERE supplier_id = ?""",
                (supplier_id,),
            ).fetchone()
            review_stats = connection.execute(
                "SELECT COUNT(*) AS total, ROUND(AVG(rating), 1) AS avg FROM supplier_reviews WHERE supplier_id = ? AND status = 'approved'",
                (supplier_id,),
            ).fetchone()
            catalog_items = connection.execute(
                """SELECT id, product_name, sku, unit, unit_price, stock_qty, image_url, category
                   FROM supplier_catalog_items WHERE supplier_id = ? AND is_active = TRUE
                   ORDER BY updated_at DESC LIMIT 24""",
                (supplier_id,),
            ).fetchall()
            reviews = connection.execute(
                """SELECT id, rating, comment, reviewer_id, created_at FROM supplier_reviews
                   WHERE supplier_id = ? AND status = 'approved' ORDER BY created_at DESC LIMIT 10""",
                (supplier_id,),
            ).fetchall()
            result = dict(supplier)
            result["catalog_items_count"] = stats["catalog_items_count"] if stats else 0
            result["min_price"] = stats["min_price"] if stats else None
            result["max_price"] = stats["max_price"] if stats else None
            result["reviews_count"] = review_stats["total"] if review_stats else 0
            result["reviews_avg"] = float(review_stats["avg"]) if review_stats and review_stats["avg"] is not None else None
            result["catalog_items"] = [dict(r) for r in catalog_items]
            result["reviews"] = [dict(r) for r in reviews]
            return result
        finally:
            self._close_connection(connection)

    # ── Marketplace cart (Kaspi/Amazon-style checkout) ──────────────────────

    def get_cart(self, actor_id: str) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """SELECT cc.id, cc.catalog_item_id, cc.quantity, cc.created_at,
                          ci.product_name, ci.sku, ci.unit, ci.unit_price, ci.min_order_qty,
                          ci.image_url, ci.is_active, ci.supplier_id,
                          s.name AS supplier_name, s.city AS supplier_city
                   FROM marketplace_cart_items cc
                   JOIN supplier_catalog_items ci ON ci.id = cc.catalog_item_id
                   JOIN suppliers s ON s.id = ci.supplier_id
                   WHERE cc.actor_id = ?
                   ORDER BY cc.created_at DESC""",
                (actor_id,),
            ).fetchall()
            items = [dict(r) for r in rows]
            total_amount = sum(float(i["unit_price"]) * float(i["quantity"]) for i in items if i["unit_price"] is not None)
            return {"items": items, "total_items": len(items), "total_amount": total_amount}
        finally:
            self._close_connection(connection)

    def add_to_cart(self, actor_id: str, catalog_item_id: int, quantity: float) -> dict[str, Any]:
        if quantity <= 0:
            raise ValidationError("quantity must be > 0")
        with self.database.transaction() as conn:
            self._require_active(conn, "supplier_catalog_items", catalog_item_id)
            existing = conn.execute(
                "SELECT id, quantity FROM marketplace_cart_items WHERE actor_id = ? AND catalog_item_id = ?",
                (actor_id, catalog_item_id),
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE marketplace_cart_items SET quantity = ?, updated_at = NOW() WHERE id = ?",
                    (float(existing["quantity"]) + quantity, existing["id"]),
                )
            else:
                insert_and_get_id(
                    conn,
                    "INSERT INTO marketplace_cart_items (actor_id, catalog_item_id, quantity) VALUES (?, ?, ?)",
                    (actor_id, catalog_item_id, quantity),
                )
        return self.get_cart(actor_id)

    def update_cart_item(self, actor_id: str, cart_item_id: int, quantity: float) -> dict[str, Any]:
        if quantity <= 0:
            raise ValidationError("quantity must be > 0")
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id FROM marketplace_cart_items WHERE id = ? AND actor_id = ?",
                (cart_item_id, actor_id),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"cart item {cart_item_id} not found")
            conn.execute(
                "UPDATE marketplace_cart_items SET quantity = ?, updated_at = NOW() WHERE id = ?",
                (quantity, cart_item_id),
            )
        return self.get_cart(actor_id)

    def remove_from_cart(self, actor_id: str, cart_item_id: int) -> dict[str, Any]:
        with self.database.transaction() as conn:
            conn.execute(
                "DELETE FROM marketplace_cart_items WHERE id = ? AND actor_id = ?",
                (cart_item_id, actor_id),
            )
        return self.get_cart(actor_id)

    def checkout_cart(
        self,
        actor_id: str,
        warehouse_id: int | None,
        notes: str | None,
        source: str = "qpartner",
    ) -> list[dict[str, Any]]:
        """Create one marketplace inquiry per cart item (grouped per supplier offer) and clear the cart."""
        source = self._validate_marketplace_inquiry_source(source) or "qpartner"
        cart = self.get_cart(actor_id)
        if not cart["items"]:
            raise ValidationError("Cart is empty")
        created: list[dict[str, Any]] = []
        errors: list[str] = []
        for entry in cart["items"]:
            try:
                inquiry = self.create_marketplace_inquiry(
                    catalog_item_id=entry["catalog_item_id"],
                    actor_id=actor_id,
                    quantity=float(entry["quantity"]),
                    notes=notes,
                    warehouse_id=warehouse_id,
                    source=source,
                )
                created.append(inquiry)
                with self.database.transaction() as conn:
                    conn.execute("DELETE FROM marketplace_cart_items WHERE id = ?", (entry["id"],))
            except Exception as error:  # noqa: BLE001 - collect per-item failures, keep checkout going
                errors.append(f"{entry['product_name']}: {error}")
        if not created and errors:
            raise ValidationError("; ".join(errors))
        return created

    # ── Production marketplace orders and payments ─────────────────────────

    def create_marketplace_orders_from_cart(
        self,
        actor_id: str,
        *,
        warehouse_id: int | None,
        source: str = "marqet",
        buyer_name: str | None = None,
        buyer_phone: str | None = None,
        buyer_email: str | None = None,
        delivery_address: str | None = None,
        notes: str | None = None,
    ) -> list[dict[str, Any]]:
        source = self._validate_marketplace_inquiry_source(source) or "marqet"
        with self.database.transaction() as conn:
            rows = conn.execute(
                """SELECT cc.id AS cart_item_id, cc.catalog_item_id, cc.quantity,
                          ci.product_id, ci.product_name, ci.sku, ci.unit, ci.unit_price,
                          ci.is_active, ci.supplier_id, s.name AS supplier_name
                   FROM marketplace_cart_items cc
                   JOIN supplier_catalog_items ci ON ci.id = cc.catalog_item_id
                   JOIN suppliers s ON s.id = ci.supplier_id
                   WHERE cc.actor_id = ? AND ci.is_active = TRUE
                   ORDER BY ci.supplier_id, cc.created_at""",
                (actor_id,),
            ).fetchall()
            if not rows:
                raise ValidationError("Cart is empty")

            groups: dict[int, list[dict[str, Any]]] = {}
            for row in rows:
                item = dict(row)
                groups.setdefault(int(item["supplier_id"]), []).append(item)

            created_ids: list[int] = []
            now = now_iso()
            for supplier_id, items in groups.items():
                subtotal = sum(
                    Decimal(str(item["unit_price"] or "0")) * Decimal(str(item["quantity"]))
                    for item in items
                )
                temp_number = f"MQ-TMP-{uuid.uuid4().hex[:16]}"
                order_id = insert_and_get_id(
                    conn,
                    """INSERT INTO marketplace_orders(
                         order_number, actor_id, supplier_id, warehouse_id, source, status,
                         currency, subtotal_amount, delivery_amount, discount_amount, total_amount,
                         buyer_name, buyer_phone, buyer_email, delivery_address, notes,
                         created_at, updated_at
                       ) VALUES (?, ?, ?, ?, ?, 'pending_payment', 'KZT', ?, 0, 0, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        temp_number,
                        actor_id,
                        supplier_id,
                        warehouse_id,
                        source,
                        decimal_to_db(subtotal),
                        decimal_to_db(subtotal),
                        buyer_name,
                        buyer_phone,
                        buyer_email,
                        delivery_address,
                        notes,
                        now,
                        now,
                    ),
                )
                order_number = f"MQ-{100000 + order_id}"
                conn.execute("UPDATE marketplace_orders SET order_number = ? WHERE id = ?", (order_number, order_id))
                for item in items:
                    quantity = Decimal(str(item["quantity"]))
                    unit_price = Decimal(str(item["unit_price"] or "0"))
                    line_total = quantity * unit_price
                    insert_and_get_id(
                        conn,
                        """INSERT INTO marketplace_order_items(
                             order_id, catalog_item_id, product_id, product_name, sku, unit,
                             quantity, unit_price, line_total, created_at
                           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            order_id,
                            item["catalog_item_id"],
                            item.get("product_id"),
                            item["product_name"],
                            item.get("sku"),
                            item.get("unit") or "шт",
                            decimal_to_db(quantity),
                            decimal_to_db(unit_price),
                            decimal_to_db(line_total),
                            now,
                        ),
                    )
                created_ids.append(order_id)

            conn.execute("DELETE FROM marketplace_cart_items WHERE actor_id = ?", (actor_id,))

        return [self.get_marketplace_order(actor_id, order_id) for order_id in created_ids]

    def list_marketplace_orders(
        self,
        actor_id: str,
        *,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        safe_limit = max(1, min(limit, 100))
        safe_offset = max(0, offset)
        where = ["mo.actor_id = ?"]
        params: list[Any] = [actor_id]
        if status:
            where.append("mo.status = ?")
            params.append(status)
        where_clause = " AND ".join(where)
        connection = self.database.connect()
        try:
            total = connection.execute(
                f"SELECT COUNT(*) AS total FROM marketplace_orders mo WHERE {where_clause}",
                tuple(params),
            ).fetchone()["total"]
            rows = connection.execute(
                f"""SELECT mo.*, s.name AS supplier_name,
                           (SELECT COUNT(*) FROM marketplace_order_items oi WHERE oi.order_id = mo.id) AS items_count,
                           (SELECT oi.product_name
                              FROM marketplace_order_items oi
                             WHERE oi.order_id = mo.id
                             ORDER BY oi.id
                             LIMIT 1) AS product_name,
                           (SELECT mp.status
                              FROM marketplace_payments mp
                             WHERE mp.order_id = mo.id
                             ORDER BY mp.created_at DESC, mp.id DESC
                             LIMIT 1) AS payment_status
                    FROM marketplace_orders mo
                    JOIN suppliers s ON s.id = mo.supplier_id
                    WHERE {where_clause}
                    ORDER BY mo.created_at DESC
                    LIMIT ? OFFSET ?""",
                tuple(params + [safe_limit, safe_offset]),
            ).fetchall()
            return {"items": [self._order_list_row(dict(row)) for row in rows], "total": int(total)}
        finally:
            self._close_connection(connection)

    def list_supplier_marketplace_orders(
        self,
        supplier_id: int,
        *,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        safe_limit = max(1, min(limit, 100))
        safe_offset = max(0, offset)
        where = ["mo.supplier_id = ?"]
        params: list[Any] = [supplier_id]
        if status:
            where.append("mo.status = ?")
            params.append(status)
        where_clause = " AND ".join(where)
        connection = self.database.connect()
        try:
            total = connection.execute(
                f"SELECT COUNT(*) AS total FROM marketplace_orders mo WHERE {where_clause}",
                tuple(params),
            ).fetchone()["total"]
            rows = connection.execute(
                f"""SELECT mo.*, s.name AS supplier_name,
                           (SELECT COUNT(*) FROM marketplace_order_items oi WHERE oi.order_id = mo.id) AS items_count,
                           (SELECT oi.product_name
                              FROM marketplace_order_items oi
                             WHERE oi.order_id = mo.id
                             ORDER BY oi.id
                             LIMIT 1) AS product_name,
                           (SELECT mp.status
                              FROM marketplace_payments mp
                             WHERE mp.order_id = mo.id
                             ORDER BY mp.created_at DESC, mp.id DESC
                             LIMIT 1) AS payment_status
                    FROM marketplace_orders mo
                    JOIN suppliers s ON s.id = mo.supplier_id
                    WHERE {where_clause}
                    ORDER BY mo.created_at DESC
                    LIMIT ? OFFSET ?""",
                tuple(params + [safe_limit, safe_offset]),
            ).fetchall()
            return {"items": [self._order_list_row(dict(row)) for row in rows], "total": int(total)}
        finally:
            self._close_connection(connection)

    def get_marketplace_order(self, actor_id: str, order_id: int) -> dict[str, Any]:
        order = self._get_marketplace_order_for_actor(actor_id, order_id)
        return self._marketplace_order_detail(order)

    def get_supplier_marketplace_order(self, supplier_id: int, order_id: int) -> dict[str, Any]:
        order = self._get_marketplace_order_for_supplier(supplier_id, order_id)
        return self._marketplace_order_detail(order)

    def get_supplier_marketplace_wallet(self, supplier_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            account = connection.execute(
                """SELECT supplier_id, currency, available_amount, pending_amount, created_at, updated_at
                   FROM marketplace_seller_accounts
                   WHERE supplier_id = ?""",
                (supplier_id,),
            ).fetchone()
            totals = connection.execute(
                """SELECT
                       COALESCE(SUM(CASE WHEN entry_type = 'credit' AND status = 'posted' THEN amount ELSE 0 END), 0) AS posted_credit,
                       COALESCE(SUM(CASE WHEN entry_type IN ('debit','refund') AND status = 'posted' THEN amount ELSE 0 END), 0) AS posted_debit,
                       COALESCE(SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END), 0) AS pending_ledger,
                       COUNT(*) AS ledger_entries
                   FROM marketplace_seller_ledger
                   WHERE supplier_id = ?""",
                (supplier_id,),
            ).fetchone()
            if account is None:
                return {
                    "supplier_id": supplier_id,
                    "currency": "KZT",
                    "available_amount": 0.0,
                    "pending_amount": 0.0,
                    "posted_credit": float(totals["posted_credit"] or 0),
                    "posted_debit": float(totals["posted_debit"] or 0),
                    "pending_ledger": float(totals["pending_ledger"] or 0),
                    "ledger_entries": int(totals["ledger_entries"] or 0),
                    "created_at": None,
                    "updated_at": None,
                }
            return {
                "supplier_id": int(account["supplier_id"]),
                "currency": account["currency"] or "KZT",
                "available_amount": float(account["available_amount"] or 0),
                "pending_amount": float(account["pending_amount"] or 0),
                "posted_credit": float(totals["posted_credit"] or 0),
                "posted_debit": float(totals["posted_debit"] or 0),
                "pending_ledger": float(totals["pending_ledger"] or 0),
                "ledger_entries": int(totals["ledger_entries"] or 0),
                "created_at": account["created_at"],
                "updated_at": account["updated_at"],
            }
        finally:
            self._close_connection(connection)

    def list_supplier_marketplace_ledger(
        self,
        supplier_id: int,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        safe_limit = max(1, min(limit, 100))
        safe_offset = max(0, offset)
        connection = self.database.connect()
        try:
            total = connection.execute(
                "SELECT COUNT(*) AS total FROM marketplace_seller_ledger WHERE supplier_id = ?",
                (supplier_id,),
            ).fetchone()["total"]
            rows = connection.execute(
                """SELECT l.id, l.order_id, l.payment_id, l.entry_type, l.status, l.amount,
                          l.currency, l.description, l.source_type, l.source_id, l.created_at,
                          mo.order_number, mp.provider, mp.provider_payment_id
                   FROM marketplace_seller_ledger l
                   LEFT JOIN marketplace_orders mo ON mo.id = l.order_id
                   LEFT JOIN marketplace_payments mp ON mp.id = l.payment_id
                   WHERE l.supplier_id = ?
                   ORDER BY l.created_at DESC, l.id DESC
                   LIMIT ? OFFSET ?""",
                (supplier_id, safe_limit, safe_offset),
            ).fetchall()
            return {
                "items": [
                    {
                        "id": row["id"],
                        "order_id": row["order_id"],
                        "order_number": row["order_number"],
                        "payment_id": row["payment_id"],
                        "provider": row["provider"],
                        "provider_payment_id": row["provider_payment_id"],
                        "entry_type": row["entry_type"],
                        "status": row["status"],
                        "amount": float(row["amount"] or 0),
                        "currency": row["currency"] or "KZT",
                        "description": row["description"],
                        "source_type": row["source_type"],
                        "source_id": row["source_id"],
                        "created_at": row["created_at"],
                    }
                    for row in rows
                ],
                "total": int(total),
            }
        finally:
            self._close_connection(connection)

    def bind_marketplace_payment_method(
        self,
        actor_id: str,
        *,
        provider: str,
        provider_token: str,
        brand: str = "unknown",
        last4: str,
        expiry_month: int | None = None,
        expiry_year: int | None = None,
        holder_name: str | None = None,
        is_default: bool = False,
    ) -> dict[str, Any]:
        provider = provider.strip().lower()
        provider_token = provider_token.strip()
        last4 = "".join(ch for ch in last4 if ch.isdigit())[-4:]
        if not provider or not provider_token:
            raise ValidationError("provider and provider_token are required")
        token_digits = "".join(ch for ch in provider_token if ch.isdigit())
        if 12 <= len(token_digits) <= 19 and token_digits == provider_token.replace(" ", "").replace("-", ""):
            raise ValidationError("Raw card numbers are not accepted; use a PSP token")
        if provider_token.isdigit() and len(provider_token) in {3, 4}:
            raise ValidationError("CVV is not accepted")
        if len(last4) != 4:
            raise ValidationError("Only masked card last4 is accepted")
        with self.database.transaction() as conn:
            if is_default:
                conn.execute(
                    "UPDATE marketplace_payment_methods SET is_default = FALSE, updated_at = ? WHERE actor_id = ?",
                    (now_iso(), actor_id),
                )
            method_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_payment_methods(
                     actor_id, provider, provider_token, brand, last4, expiry_month,
                     expiry_year, holder_name, is_default, created_at, updated_at
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    actor_id,
                    provider,
                    provider_token,
                    brand.strip().lower() or "unknown",
                    last4,
                    expiry_month,
                    expiry_year,
                    holder_name,
                    bool(is_default),
                    now_iso(),
                    now_iso(),
                ),
            )
        return self.get_marketplace_payment_method(actor_id, method_id)

    def list_marketplace_payment_methods(self, actor_id: str) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """SELECT id, provider, brand, last4, expiry_month, expiry_year,
                          holder_name, is_default, status, created_at, updated_at
                   FROM marketplace_payment_methods
                   WHERE actor_id = ? AND status <> 'disabled'
                   ORDER BY is_default DESC, created_at DESC""",
                (actor_id,),
            ).fetchall()
            return {"items": [self._payment_method_public(dict(row)) for row in rows]}
        finally:
            self._close_connection(connection)

    def get_marketplace_payment_method(self, actor_id: str, method_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            row = connection.execute(
                """SELECT id, provider, brand, last4, expiry_month, expiry_year,
                          holder_name, is_default, status, created_at, updated_at
                   FROM marketplace_payment_methods
                   WHERE id = ? AND actor_id = ? AND status <> 'disabled'""",
                (method_id, actor_id),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"payment method {method_id} not found")
            return self._payment_method_public(dict(row))
        finally:
            self._close_connection(connection)

    def set_default_marketplace_payment_method(self, actor_id: str, method_id: int) -> dict[str, Any]:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id FROM marketplace_payment_methods WHERE id = ? AND actor_id = ? AND status = 'active'",
                (method_id, actor_id),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"payment method {method_id} not found")
            conn.execute(
                "UPDATE marketplace_payment_methods SET is_default = FALSE, updated_at = ? WHERE actor_id = ?",
                (now_iso(), actor_id),
            )
            conn.execute(
                "UPDATE marketplace_payment_methods SET is_default = TRUE, updated_at = ? WHERE id = ?",
                (now_iso(), method_id),
            )
        return self.get_marketplace_payment_method(actor_id, method_id)

    def delete_marketplace_payment_method(self, actor_id: str, method_id: int) -> None:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id FROM marketplace_payment_methods WHERE id = ? AND actor_id = ?",
                (method_id, actor_id),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"payment method {method_id} not found")
            conn.execute(
                "UPDATE marketplace_payment_methods SET status = 'disabled', is_default = FALSE, updated_at = ? WHERE id = ?",
                (now_iso(), method_id),
            )

    def create_marketplace_payment(
        self,
        actor_id: str,
        order_id: int,
        *,
        provider: str = "manual",
        payment_method_id: int | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        with self.database.transaction() as conn:
            order = self._get_marketplace_order_for_actor_conn(conn, actor_id, order_id)
            if order["status"] not in {"pending_payment", "draft"}:
                raise ValidationError("Order is not awaiting payment")
            if idempotency_key:
                existing = conn.execute(
                    "SELECT * FROM marketplace_payments WHERE actor_id = ? AND idempotency_key = ?",
                    (actor_id, idempotency_key),
                ).fetchone()
                if existing is not None:
                    if int(existing["order_id"]) != int(order_id):
                        raise ConflictError("Idempotency key was already used for another order")
                    return dict(existing)
            if payment_method_id is not None:
                method = conn.execute(
                    "SELECT id, provider FROM marketplace_payment_methods WHERE id = ? AND actor_id = ? AND status = 'active'",
                    (payment_method_id, actor_id),
                ).fetchone()
                if method is None:
                    raise NotFoundError(f"payment method {payment_method_id} not found")
                provider = str(method["provider"])
            payment_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_payments(
                     order_id, actor_id, supplier_id, payment_method_id, provider, method,
                     status, amount, currency, idempotency_key, metadata, created_at, updated_at
                   ) VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, 'KZT', ?, ?, ?, ?)""",
                (
                    order_id,
                    actor_id,
                    order["supplier_id"],
                    payment_method_id,
                    provider.strip().lower() or "manual",
                    "saved_card" if payment_method_id else "redirect",
                    decimal_to_db(Decimal(str(order["total_amount"]))),
                    idempotency_key,
                    {},
                    now_iso(),
                    now_iso(),
                ),
            )
        return self.get_marketplace_payment(actor_id, payment_id)

    def get_marketplace_payment(self, actor_id: str, payment_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT * FROM marketplace_payments WHERE id = ? AND actor_id = ?",
                (payment_id, actor_id),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"payment {payment_id} not found")
            return dict(row)
        finally:
            self._close_connection(connection)

    def apply_marketplace_payment_event(
        self,
        *,
        provider: str,
        provider_event_id: str,
        provider_payment_id: str,
        payment_id: int,
        status: str,
        amount: Decimal,
        currency: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if status not in {"paid", "failed", "cancelled", "refunded", "authorized"}:
            raise ValidationError("Unsupported payment event status")
        provider = provider.strip().lower()
        provider_payment_id = provider_payment_id.strip()
        currency = currency.strip().upper()
        if not provider or not provider_event_id.strip() or not provider_payment_id:
            raise ValidationError("provider, provider_event_id and provider_payment_id are required")
        with self.database.transaction() as conn:
            existing = conn.execute(
                """SELECT payment_id FROM marketplace_payment_events
                   WHERE provider = ? AND provider_event_id = ?""",
                (provider, provider_event_id),
            ).fetchone()
            if existing:
                if int(existing["payment_id"]) != int(payment_id):
                    raise ConflictError("Payment event id is already linked to another payment")
                payment = conn.execute("SELECT * FROM marketplace_payments WHERE id = ?", (payment_id,)).fetchone()
                if payment is None:
                    raise NotFoundError(f"payment {payment_id} not found")
                return dict(payment)
            payment = conn.execute("SELECT * FROM marketplace_payments WHERE id = ?", (payment_id,)).fetchone()
            if payment is None:
                raise NotFoundError(f"payment {payment_id} not found")
            if str(payment["provider"]).lower() != provider:
                raise ValidationError("Payment provider mismatch")
            if str(payment["currency"]).upper() != currency:
                raise ValidationError("Payment currency mismatch")
            if Decimal(str(payment["amount"])) != Decimal(str(amount)):
                raise ValidationError("Payment amount mismatch")
            existing_provider_payment = conn.execute(
                """SELECT id FROM marketplace_payments
                   WHERE provider = ? AND provider_payment_id = ? AND id <> ?""",
                (provider, provider_payment_id, payment_id),
            ).fetchone()
            if existing_provider_payment is not None:
                raise ConflictError("Provider payment id is already linked to another payment")
            event_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_payment_events(
                     payment_id, provider, provider_event_id, event_type, payload, received_at, processed_at
                   ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    payment_id,
                    provider,
                    provider_event_id,
                    status,
                    payload,
                    now_iso(),
                    now_iso(),
                ),
            )
            conn.execute(
                """UPDATE marketplace_payments
                   SET provider_payment_id = COALESCE(provider_payment_id, ?)
                   WHERE id = ?""",
                (provider_payment_id, payment_id),
            )
            timestamp_col = {
                "paid": "paid_at",
                "failed": "failed_at",
                "refunded": "refunded_at",
                "authorized": "authorized_at",
            }.get(status)
            if timestamp_col:
                conn.execute(
                    f"UPDATE marketplace_payments SET status = ?, updated_at = ?, {timestamp_col} = ? WHERE id = ?",
                    (status, now_iso(), now_iso(), payment_id),
                )
            else:
                conn.execute(
                    "UPDATE marketplace_payments SET status = ?, updated_at = ? WHERE id = ?",
                    (status, now_iso(), payment_id),
                )
            if status == "paid" and payment["status"] != "paid":
                self._mark_marketplace_order_paid(conn, int(payment["order_id"]), int(payment["id"]))
            updated = conn.execute("SELECT * FROM marketplace_payments WHERE id = ?", (payment_id,)).fetchone()
            result = dict(updated)
            result["event_id"] = event_id
            return result

    def get_marketplace_account_summary(self, actor_id: str) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            row = connection.execute(
                """SELECT
                     SUM(CASE WHEN status IN ('pending_payment','paid','accepted','preparing','shipped') THEN 1 ELSE 0 END) AS active_orders,
                     SUM(CASE WHEN status IN ('delivered','completed') THEN 1 ELSE 0 END) AS delivered_orders
                   FROM marketplace_orders WHERE actor_id = ?""",
                (actor_id,),
            ).fetchone()
            methods = connection.execute(
                "SELECT COUNT(*) AS n FROM marketplace_payment_methods WHERE actor_id = ? AND status = 'active'",
                (actor_id,),
            ).fetchone()
            return {
                "active_orders": int(row["active_orders"] or 0),
                "delivered_orders": int(row["delivered_orders"] or 0),
                "bonus_points": 0,
                "saved_payment_methods": int(methods["n"] or 0),
                "open_messages": 0,
                "seller_listings": 0,
            }
        finally:
            self._close_connection(connection)

    def create_marketplace_inquiry(
        self, catalog_item_id: int, actor_id: str, quantity: float,
        notes: str | None, warehouse_id: int | None,
        purchase_request_id: int | None = None,
        source: str = "marqet",
    ) -> dict[str, Any]:
        source = self._validate_marketplace_inquiry_source(source) or "marqet"
        connection = self.database.connect()
        try:
            item = connection.execute(
                "SELECT * FROM supplier_catalog_items WHERE id = ? AND is_active = TRUE",
                (catalog_item_id,)
            ).fetchone()
            if item is None:
                raise ValueError(f"Catalog item {catalog_item_id} not found or inactive")
            # Duplicate guard — warn if open inquiry already exists for this actor+supplier+product
            existing = connection.execute(
                """SELECT id FROM marketplace_inquiries
                   WHERE catalog_item_id = ? AND actor_id = ? AND status IN ('pending','responded')
                   LIMIT 1""",
                (catalog_item_id, actor_id),
            ).fetchone()
        finally:
            self._close_connection(connection)
        if existing:
            raise ValidationError(f"Уже есть открытый запрос #{existing['id']} на этот товар у этого поставщика")
        with self.database.transaction() as conn:
            row_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_inquiries
                   (catalog_item_id, supplier_id, warehouse_id, actor_id, quantity, unit_price, notes, purchase_request_id, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    catalog_item_id,
                    item["supplier_id"],
                    warehouse_id,
                    actor_id,
                    quantity,
                    item["unit_price"],
                    notes,
                    purchase_request_id,
                    source,
                ),
            )
            # Auto-link purchase request status if provided
            if purchase_request_id:
                conn.execute(
                    "UPDATE purchase_requests SET status = 'ordered' WHERE id = ? AND status = 'draft'",
                    (purchase_request_id,),
                )
            row = conn.execute("SELECT * FROM marketplace_inquiries WHERE id = ?", (row_id,)).fetchone()
            result = dict(row) if row else {}
            # Seed initial buyer message
            if notes:
                conn.execute(
                    "INSERT INTO inquiry_messages (inquiry_id, actor_id, role, body) VALUES (?, ?, 'buyer', ?)"
,                    (row_id, actor_id, notes),
                )
        # Fire-and-forget email to supplier (outside transaction)
        try:
            supplier = conn.execute("SELECT name, email FROM suppliers WHERE id = ?", (item["supplier_id"],)).fetchone() if False else None
        except Exception:
            supplier = None
        try:
            from app.core.config import get_settings
            from app.services.email_notifier import notify_new_inquiry
            import threading
            _settings = get_settings()
            if _settings.smtp_host:
                _conn2 = self.database.connect()
                try:
                    _sup = _conn2.execute("SELECT name, email FROM suppliers WHERE id = ?", (item["supplier_id"],)).fetchone()
                finally:
                    self._close_connection(_conn2)
                if _sup and _sup["email"]:
                    threading.Thread(
                        target=notify_new_inquiry,
                        args=(_settings, _sup["email"], _sup["name"],
                              item["product_name"], quantity, item["unit"],
                              notes, row_id),
                        daemon=True,
                    ).start()
        except Exception as _email_exc:
            import logging; logging.getLogger(__name__).warning("Email error: %s", _email_exc)
        return result

    def list_marketplace_inquiries(
        self,
        supplier_id: int | None = None,
        actor_id: str | None = None,
        status: str | None = None,
        source: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        source = self._validate_marketplace_inquiry_source(source)
        status = self._validate_marketplace_inquiry_status(status)
        where = []
        params: list[Any] = []
        if supplier_id is not None:
            where.append("mi.supplier_id = ?")
            params.append(supplier_id)
        if actor_id is not None:
            where.append("mi.actor_id = ?")
            params.append(actor_id)
        if status:
            where.append("mi.status = ?")
            params.append(status)
        if source:
            where.append("mi.source = ?")
            params.append(source)
        where_clause = f"WHERE {' AND '.join(where)}" if where else ""
        connection = self.database.connect()
        try:
            total_row = connection.execute(
                f"SELECT COUNT(*) AS n FROM marketplace_inquiries mi {where_clause}", tuple(params)
            ).fetchone()
            total = total_row["n"] if total_row else 0
            rows = connection.execute(
                f"""
                SELECT mi.*, ci.product_name, ci.unit, ci.sku,
                       s.name AS supplier_name, s.phone AS supplier_phone, s.email AS supplier_email,
                       w.name AS warehouse_name
                FROM marketplace_inquiries mi
                JOIN supplier_catalog_items ci ON ci.id = mi.catalog_item_id
                JOIN suppliers s ON s.id = mi.supplier_id
                LEFT JOIN warehouses w ON w.id = mi.warehouse_id
                {where_clause}
                ORDER BY mi.created_at DESC
                LIMIT ? OFFSET ?
                """,
                tuple(params) + (limit, offset),
            ).fetchall()
            items = [dict(r) for r in rows]
            ids = [i["id"] for i in items]
            if ids:
                placeholders = ", ".join(["?"] * len(ids))
                po_rows = connection.execute(
                    f"""SELECT inquiry_id, id, po_number, status, created_at, sent_at, accepted_at
                        FROM purchase_orders WHERE inquiry_id IN ({placeholders})
                        ORDER BY created_at DESC""",
                    tuple(ids),
                ).fetchall()
                po_by_inquiry: dict[int, dict] = {}
                for po in po_rows:
                    po_by_inquiry.setdefault(po["inquiry_id"], dict(po))
                refs = [f"INQ-{i}" for i in ids]
                ref_placeholders = ", ".join(["?"] * len(refs))
                sh_rows = connection.execute(
                    f"""SELECT reference, id, status, current_city, estimated_arrival, updated_at
                        FROM shipments WHERE reference IN ({ref_placeholders})
                        ORDER BY created_at DESC""",
                    tuple(refs),
                ).fetchall()
                sh_by_ref: dict[str, dict] = {}
                for sh in sh_rows:
                    sh_by_ref.setdefault(sh["reference"], dict(sh))
                for item in items:
                    item["purchase_order"] = po_by_inquiry.get(item["id"])
                    item["shipment"] = sh_by_ref.get(f"INQ-{item['id']}")
            return {"items": items, "total": total}
        finally:
            self._close_connection(connection)

    def respond_to_inquiry(
        self, inquiry_id: int, supplier_id: int, response_text: str
    ) -> dict[str, Any]:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id, supplier_id FROM marketplace_inquiries WHERE id = ?", (inquiry_id,)
            ).fetchone()
            if row is None or row["supplier_id"] != supplier_id:
                raise PermissionError("Inquiry not found or not yours")
            conn.execute(
                "UPDATE marketplace_inquiries SET status = 'responded', supplier_response = ?, responded_at = NOW() WHERE id = ?",
                (response_text, inquiry_id),
            )
            # Record supplier reply as chat message
            supplier_actor = f"supplier-actor:{supplier_id}"
            conn.execute(
                "INSERT INTO inquiry_messages (inquiry_id, actor_id, role, body) VALUES (?, ?, 'supplier', ?)"
,                (inquiry_id, supplier_actor, response_text),
            )
            updated = conn.execute(
                """SELECT mi.*, ci.product_name, ci.unit, s.name AS supplier_name
                   FROM marketplace_inquiries mi
                   JOIN supplier_catalog_items ci ON ci.id = mi.catalog_item_id
                   JOIN suppliers s ON s.id = mi.supplier_id
                   WHERE mi.id = ?""",
                (inquiry_id,)
            ).fetchone()
            result2 = dict(updated) if updated else {}
        # Notify buyer by email if we have their email in sklad_users
        try:
            from app.core.config import get_settings
            from app.services.email_notifier import notify_inquiry_response
            import threading
            _settings = get_settings()
            if _settings.smtp_host and result2:
                _actor_id = result2.get("actor_id", "")
                # actor_id format: "tetis-actor:{sub}" → sklad_users.username = "tetis:{sub}"
                _tetis_id = _actor_id.removeprefix("tetis-actor:")
                _conn3 = self.database.connect()
                try:
                    _buyer = _conn3.execute(
                        "SELECT email FROM sklad_users WHERE username = ?",
                        (f"tetis:{_tetis_id}",)
                    ).fetchone()
                finally:
                    self._close_connection(_conn3)
                if _buyer and _buyer["email"]:
                    threading.Thread(
                        target=notify_inquiry_response,
                        args=(_settings, _buyer["email"],
                              result2.get("supplier_name", ""),
                              result2.get("product_name", ""),
                              response_text, inquiry_id),
                        daemon=True,
                    ).start()
        except Exception as _email_exc2:
            import logging; logging.getLogger(__name__).warning("Email error: %s", _email_exc2)
        return result2

    def list_inquiry_messages(
        self, inquiry_id: int, actor_id: str
    ) -> list[dict]:
        """Return all messages for an inquiry. Caller must be the buyer or the supplier."""
        connection = self.database.connect()
        try:
            inq = connection.execute(
                "SELECT actor_id, supplier_id FROM marketplace_inquiries WHERE id = ?",
                (inquiry_id,)
            ).fetchone()
            if inq is None:
                raise NotFoundError(f"Inquiry {inquiry_id} not found")
            # Verify access: buyer (actor_id match) or supplier
            supplier_actor = f"supplier-actor:{inq['supplier_id']}"
            if actor_id != inq["actor_id"] and actor_id != supplier_actor:
                raise PermissionError("Access denied to inquiry messages")
            rows = connection.execute(
                """SELECT id, actor_id, role, body, created_at
                   FROM inquiry_messages
                   WHERE inquiry_id = ?
                   ORDER BY created_at, id""",
                (inquiry_id,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def add_inquiry_message(
        self, inquiry_id: int, actor_id: str, body: str
    ) -> dict:
        """Buyer or supplier sends a follow-up message on an existing inquiry."""
        body = (body or "").strip()
        if not body:
            raise ValidationError("Message body cannot be empty")
        with self.database.transaction() as conn:
            inq = conn.execute(
                "SELECT actor_id, supplier_id, status FROM marketplace_inquiries WHERE id = ?",
                (inquiry_id,)
            ).fetchone()
            if inq is None:
                raise NotFoundError(f"Inquiry {inquiry_id} not found")
            if inq["status"] in ("cancelled", "closed"):
                raise ValidationError("Cannot add message to a closed/cancelled inquiry")
            supplier_actor = f"supplier-actor:{inq['supplier_id']}"
            if actor_id == inq["actor_id"]:
                role = "buyer"
            elif actor_id == supplier_actor:
                role = "supplier"
            else:
                raise PermissionError("Access denied")
            msg_id = insert_and_get_id(
                conn,
                "INSERT INTO inquiry_messages (inquiry_id, actor_id, role, body) VALUES (?, ?, ?, ?)",
                (inquiry_id, actor_id, role, body),
            )
            # Touch inquiry updated_at / status if supplier is replying
            if role == "supplier" and inq["status"] == "pending":
                conn.execute(
                    "UPDATE marketplace_inquiries SET status = 'responded', responded_at = NOW() WHERE id = ?",
                    (inquiry_id,)
                )
            row = conn.execute(
                "SELECT id, inquiry_id, actor_id, role, body, created_at FROM inquiry_messages WHERE id = ?",
                (msg_id,)
            ).fetchone()
            return dict(row) if row else {}

    def update_inquiry_status(
        self, inquiry_id: int, actor_id: str, new_status: str
    ) -> dict[str, Any]:
        """Buyer-side status update — mark inquiry as ordered or closed."""
        if new_status not in ("ordered", "closed"):
            raise ValueError(f"Invalid status: {new_status}")
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id, actor_id FROM marketplace_inquiries WHERE id = ?", (inquiry_id,)
            ).fetchone()
            if row is None or row["actor_id"] != actor_id:
                raise PermissionError("Inquiry not found or not yours")
            conn.execute(
                "UPDATE marketplace_inquiries SET status = ? WHERE id = ?",
                (new_status, inquiry_id),
            )
            updated = conn.execute(
                """SELECT mi.*, ci.product_name, ci.unit, s.name AS supplier_name,
                          s.phone AS supplier_phone, s.email AS supplier_email
                   FROM marketplace_inquiries mi
                   JOIN supplier_catalog_items ci ON ci.id = mi.catalog_item_id
                   JOIN suppliers s ON s.id = mi.supplier_id
                   WHERE mi.id = ?""",
                (inquiry_id,)
            ).fetchone()
            return dict(updated) if updated else {}

    def create_shipment_from_inquiry(
        self, inquiry_id: int, supplier_id: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Supplier creates a shipment record from an accepted inquiry."""
        with self.database.transaction() as conn:
            inq = conn.execute(
                "SELECT * FROM marketplace_inquiries WHERE id = ? AND supplier_id = ?",
                (inquiry_id, supplier_id),
            ).fetchone()
            if inq is None:
                raise PermissionError("Inquiry not found or not yours")
            # Build shipment fields
            warehouse_id = inq["warehouse_id"] or data.get("destination_warehouse_id")
            reference = data.get("reference") or f"INQ-{inquiry_id}"
            notes = data.get("notes") or inq["notes"]
            sid = insert_and_get_id(
                conn,
                """INSERT INTO shipments (supplier_id, reference, status, origin_city,
                   destination_warehouse_id, estimated_arrival, notes)
                   VALUES (?, ?, 'planned', ?, ?, ?, ?)""",
                (
                    supplier_id,
                    reference,
                    data.get("origin_city"),
                    warehouse_id,
                    data.get("estimated_arrival"),
                    notes,
                ),
            )
            conn.execute(
                "UPDATE marketplace_inquiries SET status = 'ordered' WHERE id = ?",
                (inquiry_id,),
            )
            shipment = conn.execute("SELECT * FROM shipments WHERE id = ?", (sid,)).fetchone()
            return dict(shipment) if shipment else {}

    def create_bulk_inquiry(
        self,
        product_name: str,
        actor_id: str,
        quantity: float,
        notes: str | None,
        warehouse_id: int | None,
        source: str = "qpartner",
    ) -> dict[str, Any]:
        """Send inquiry to all suppliers that have matching catalog items."""
        source = self._validate_marketplace_inquiry_source(source) or "qpartner"
        connection = self.database.connect()
        try:
            items = connection.execute(
                """SELECT ci.*, s.name AS supplier_name FROM supplier_catalog_items ci
                   JOIN suppliers s ON s.id = ci.supplier_id
                   WHERE ci.is_active = TRUE AND ci.product_name ILIKE ?
                   ORDER BY ci.unit_price ASC""",
                (f"%{product_name}%",),
            ).fetchall()
        finally:
            self._close_connection(connection)

        if not items:
            return {"items": [], "total": 0}

        # One inquiry per supplier (pick cheapest item per supplier)
        seen_suppliers: set[int] = set()
        created = []
        with self.database.transaction() as conn:
            for item in items:
                sid = item["supplier_id"]
                if sid in seen_suppliers:
                    continue
                seen_suppliers.add(sid)
                row_id = insert_and_get_id(
                    conn,
                    """INSERT INTO marketplace_inquiries
                       (catalog_item_id, supplier_id, warehouse_id, actor_id, quantity, unit_price, notes, source)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (item["id"], sid, warehouse_id, actor_id, quantity, item["unit_price"], notes, source),
                )
                row = conn.execute("SELECT * FROM marketplace_inquiries WHERE id = ?", (row_id,)).fetchone()
                if row:
                    created.append({**dict(row), "supplier_name": item["supplier_name"]})

        return {"items": created, "total": len(created)}

    def import_catalog_csv(
        self, supplier_id: int, rows: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Bulk-insert catalog items from parsed CSV rows."""
        allowed_fields = {"product_name", "sku", "unit", "unit_price", "min_order_qty",
                          "stock_qty", "delivery_days", "category", "description"}
        inserted = 0
        skipped = 0
        errors: list[str] = []
        with self.database.transaction() as conn:
            for i, row in enumerate(rows, 1):
                try:
                    product_name = str(row.get("product_name") or "").strip()
                    unit_price_raw = row.get("unit_price")
                    if not product_name or unit_price_raw is None:
                        skipped += 1
                        errors.append(f"Строка {i}: пропущена (нет названия или цены)")
                        continue
                    unit_price = float(str(unit_price_raw).replace(",", "."))
                    unit = str(row.get("unit") or "шт").strip() or "шт"
                    min_order_qty = float(str(row.get("min_order_qty") or 1).replace(",", ".") or 1)
                    stock_qty_raw = row.get("stock_qty")
                    stock_qty = float(str(stock_qty_raw).replace(",", ".")) if stock_qty_raw not in (None, "") else None
                    delivery_days_raw = row.get("delivery_days")
                    delivery_days = int(float(str(delivery_days_raw).replace(",", "."))) if delivery_days_raw not in (None, "") else None
                    insert_and_get_id(
                        conn,
                        """INSERT INTO supplier_catalog_items
                           (supplier_id, product_name, sku, unit, unit_price, min_order_qty,
                            stock_qty, delivery_days, category, description, is_active)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, TRUE)""",
                        (
                            supplier_id,
                            product_name,
                            str(row.get("sku") or "").strip() or None,
                            unit,
                            unit_price,
                            min_order_qty,
                            stock_qty,
                            delivery_days,
                            str(row.get("category") or "").strip() or None,
                            str(row.get("description") or "").strip() or None,
                        ),
                    )
                    inserted += 1
                except Exception as exc:
                    skipped += 1
                    errors.append(f"Строка {i}: {exc}")
        return {"inserted": inserted, "skipped": skipped, "errors": errors}

    def get_catalog_item_inquiry_stats(self, supplier_id: int) -> list[dict[str, Any]]:
        """Return inquiry counts per catalog item for a supplier."""
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """SELECT ci.id, ci.product_name, ci.unit_price, ci.unit, ci.is_active,
                          COUNT(mi.id) AS inquiries_total,
                          COUNT(mi.id) FILTER (WHERE mi.status = 'pending') AS inquiries_pending,
                          COUNT(mi.id) FILTER (WHERE mi.status IN ('ordered')) AS inquiries_ordered
                   FROM supplier_catalog_items ci
                   LEFT JOIN marketplace_inquiries mi ON mi.catalog_item_id = ci.id
                   WHERE ci.supplier_id = ?
                   GROUP BY ci.id
                   ORDER BY inquiries_total DESC, ci.id""",
                (supplier_id,),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    # ────────────────────────────────────────────────────────────────────────

    def review_supplier_application(
        self,
        application_id: int,
        data: SupplierApplicationReview,
        reviewer_id: str,
        password_hash: str | None = None,
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            application = self._get_supplier_application(connection, application_id)
            supplier_id = data.supplier_id or application.get("supplier_id")
            if data.status == "approved":
                if supplier_id is None:
                    matched = None
                    if application.get("bin"):
                        matched = connection.execute(
                            "SELECT id FROM suppliers WHERE bin = ? ORDER BY id LIMIT 1",
                            (application["bin"],),
                        ).fetchone()
                    if matched is None:
                        matched = connection.execute(
                            "SELECT id FROM suppliers WHERE lower(email) = lower(?) ORDER BY id LIMIT 1",
                            (application["email"],),
                        ).fetchone()
                    supplier_id = int(matched["id"]) if matched else None
                if supplier_id is None:
                    supplier_id = insert_and_get_id(
                        connection,
                        """
                        INSERT INTO suppliers(
                          name, bin, phone, address, rating, is_preferred,
                          contact_person, email, contract_number, contract_expires_on,
                          payment_terms, notes, lat, lng, city, delivery_days
                        ) VALUES (?, ?, ?, ?, NULL, ?, ?, ?, NULL, NULL, NULL, ?, NULL, NULL, ?, ?)
                        """,
                        (
                            application["name"],
                            application.get("bin"),
                            application.get("phone"),
                            application.get("address"),
                            0,
                            application.get("contact_person"),
                            application.get("email"),
                            application.get("notes"),
                            application.get("city"),
                            application.get("delivery_days"),
                        ),
                    )
                else:
                    self._require(connection, "suppliers", supplier_id)
                    connection.execute(
                        """
                        UPDATE suppliers
                        SET name = ?,
                            bin = COALESCE(?, bin),
                            phone = COALESCE(?, phone),
                            address = COALESCE(?, address),
                            contact_person = COALESCE(?, contact_person),
                            email = COALESCE(?, email),
                            notes = COALESCE(?, notes),
                            city = COALESCE(?, city),
                            delivery_days = COALESCE(?, delivery_days)
                        WHERE id = ?
                        """,
                        (
                            application["name"],
                            application.get("bin"),
                            application.get("phone"),
                            application.get("address"),
                            application.get("contact_person"),
                            application.get("email"),
                            application.get("notes"),
                            application.get("city"),
                            application.get("delivery_days"),
                            supplier_id,
                        ),
                    )
                if password_hash:
                    connection.execute(
                        "UPDATE suppliers SET password_hash = ?, portal_access_enabled = TRUE WHERE id = ?",
                        (password_hash, supplier_id),
                    )
                requester = application.get("actor_id") or ""
                if requester.startswith("tetis-actor:"):
                    self._link_requester_to_supplier(connection, requester.removeprefix("tetis-actor:"), supplier_id)
            now = now_iso()
            connection.execute(
                """
                UPDATE supplier_applications
                SET status = ?,
                    supplier_id = ?,
                    review_reason = ?,
                    reviewed_by = ?,
                    reviewed_at = ?
                WHERE id = ?
                """,
                (
                    data.status,
                    supplier_id,
                    data.reason,
                    reviewer_id,
                    now,
                    application_id,
                ),
            )
            updated = self._get_supplier_application(connection, application_id)
            self._audit(
                connection,
                reviewer_id,
                AuditAction.UPDATE,
                "supplier_application",
                application_id,
                {"before": application, "after": updated},
            )
            return updated

    def _link_requester_to_supplier(self, connection, requester_actor_id: str, supplier_id: int) -> None:
        """Auto-link the tetis user who submitted an approved supplier application
        to that supplier, so they can switch into supplier mode without an admin
        having to manually type a supplier ID into the Users screen."""
        import secrets
        if requester_actor_id.isdigit():
            row = connection.execute(
                "SELECT id FROM sklad_users WHERE id = ?", (int(requester_actor_id),)
            ).fetchone()
            if row:
                connection.execute(
                    "UPDATE sklad_users SET supplier_id = ? WHERE id = ?",
                    (supplier_id, row["id"]),
                )
                return
        username = f"tetis:{requester_actor_id}"
        existing = connection.execute(
            "SELECT id FROM sklad_users WHERE username = ?", (username,)
        ).fetchone()
        if existing:
            connection.execute(
                "UPDATE sklad_users SET supplier_id = ? WHERE id = ?",
                (supplier_id, existing["id"]),
            )
            return
        connection.execute(
            "INSERT INTO sklad_users (username, full_name, password_hash, roles, warehouse_ids, supplier_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (username, "Поставщик", secrets.token_hex(32), "warehouse_manager", "[]", supplier_id),
        )

    def create_warehouse(self, data: WarehouseCreate, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            warehouse_id = insert_and_get_id(
                connection,
                """
                INSERT INTO warehouses(
                  name, department, tetis_org_id, external_tetis_id,
                  mis_clinic_id, mis_room_id,
                  storage_zone, capacity_limit, storage_conditions, responsible_person
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.name,
                    data.department,
                    data.tetis_org_id,
                    data.external_tetis_id,
                    data.mis_clinic_id,
                    data.mis_room_id,
                    data.storage_zone,
                    self._optional_decimal_to_db(data.capacity_limit),
                    data.storage_conditions,
                    data.responsible_person,
                ),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "warehouse",
                warehouse_id,
                data,
                warehouse_id=warehouse_id,
            )
            return self._get_by_id(connection, "warehouses", warehouse_id)

    def list_warehouses(
        self, limit: int = 100, offset: int = 0, q: str | None = None
    ) -> list[dict[str, Any]]:
        if not q or not q.strip():
            return self._list_table("warehouses", "name, id", limit, offset)
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        search = q.strip().casefold()
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT * FROM warehouses
                ORDER BY name, id
                """
            ).fetchall()
            searchable_fields = (
                "name",
                "department",
                "tetis_org_id",
                "external_tetis_id",
                "storage_zone",
                "storage_conditions",
                "responsible_person",
            )
            filtered = []
            for row in rows:
                item = dict(row)
                haystack = " ".join(str(item.get(field) or "") for field in searchable_fields).casefold()
                if search in haystack:
                    filtered.append(item)
            return filtered[safe_offset : safe_offset + safe_limit]
        finally:
            self._close_connection(connection)

    def list_warehouse_ids_for_tetis_org(self, tetis_org_id: str) -> list[int]:
        org_id = tetis_org_id.strip()
        if not org_id:
            return []
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT id
                FROM warehouses
                WHERE tetis_org_id = ?
                ORDER BY id
                """,
                (org_id,),
            ).fetchall()
            return [int(row["id"]) for row in rows]
        finally:
            self._close_connection(connection)

    def get_tetis_org_id_for_warehouses(self, warehouse_ids: list[int]) -> str | None:
        """Reverse lookup: given a list of warehouse IDs, return the shared tetis_org_id."""
        if not warehouse_ids:
            return None
        connection = self.database.connect()
        try:
            placeholders = ','.join('?' * len(warehouse_ids))
            row = connection.execute(
                f"SELECT tetis_org_id FROM warehouses WHERE id IN ({placeholders}) AND tetis_org_id IS NOT NULL LIMIT 1",
                warehouse_ids,
            ).fetchone()
            return row["tetis_org_id"] if row else None
        finally:
            self._close_connection(connection)

    def create_sensor_device(
        self, data: SensorDeviceCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        self._validate_sensor_thresholds(data)
        with self.database.transaction() as connection:
            self._require(connection, "warehouses", data.warehouse_id)
            now = now_iso()
            device_id = insert_and_get_id(
                connection,
                """
                INSERT INTO sensor_devices(
                  warehouse_id, name, serial_number, sensor_type,
                  min_temperature_c, max_temperature_c,
                  min_humidity_percent, max_humidity_percent,
                  created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.warehouse_id,
                    data.name,
                    data.serial_number,
                    data.sensor_type,
                    self._optional_decimal_to_db(data.min_temperature_c),
                    self._optional_decimal_to_db(data.max_temperature_c),
                    self._optional_decimal_to_db(data.min_humidity_percent),
                    self._optional_decimal_to_db(data.max_humidity_percent),
                    now,
                    now,
                ),
            )
            device = self._get_by_id(connection, "sensor_devices", device_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "sensor_device",
                device_id,
                device,
                warehouse_id=data.warehouse_id,
            )
            return device

    def list_sensor_devices(
        self, warehouse_id: int | None = None, limit: int = 100, offset: int = 0
    ) -> list[dict[str, Any]]:
        if warehouse_id is None:
            return self._list_table("sensor_devices", "warehouse_id, name, id", limit, offset)
        return self._list_table(
            "sensor_devices",
            "name, id",
            limit,
            offset,
            where="warehouse_id = ?",
            params=(warehouse_id,),
        )

    def update_sensor_device(
        self,
        device_id: int,
        data: SensorDeviceUpdate,
        actor_id: str = "system",
    ) -> dict[str, Any]:
        self._validate_sensor_thresholds(data)
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "sensor_devices", device_id)
            self._require(connection, "warehouses", data.warehouse_id)
            connection.execute(
                """
                UPDATE sensor_devices
                SET warehouse_id = ?,
                    name = ?,
                    serial_number = ?,
                    sensor_type = ?,
                    min_temperature_c = ?,
                    max_temperature_c = ?,
                    min_humidity_percent = ?,
                    max_humidity_percent = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    data.warehouse_id,
                    data.name,
                    data.serial_number,
                    data.sensor_type,
                    self._optional_decimal_to_db(data.min_temperature_c),
                    self._optional_decimal_to_db(data.max_temperature_c),
                    self._optional_decimal_to_db(data.min_humidity_percent),
                    self._optional_decimal_to_db(data.max_humidity_percent),
                    now_iso(),
                    device_id,
                ),
            )
            updated = self._get_by_id(connection, "sensor_devices", device_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "sensor_device",
                device_id,
                {"before": before, "after": updated},
                warehouse_id=updated["warehouse_id"],
            )
            return updated

    def get_sensor_device(self, device_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_by_id(connection, "sensor_devices", device_id)
        finally:
            self._close_connection(connection)

    def record_sensor_reading(
        self, data: SensorReadingCreate, actor_id: str = "sensor"
    ) -> dict[str, Any]:
        self._validate_sensor_reading(data)
        with self.database.transaction() as connection:
            device = self._get_by_id(connection, "sensor_devices", data.device_id)
            recorded_at = data.recorded_at.isoformat() if data.recorded_at else now_iso()
            received_at = now_iso()
            status = self._sensor_reading_status(device, data)
            reading_id = insert_and_get_id(
                connection,
                """
                INSERT INTO sensor_readings(
                  device_id, warehouse_id, temperature_c, humidity_percent,
                  recorded_at, received_at, status, raw_payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.device_id,
                    device["warehouse_id"],
                    self._optional_decimal_to_db(data.temperature_c),
                    self._optional_decimal_to_db(data.humidity_percent),
                    recorded_at,
                    received_at,
                    status,
                    data.raw_payload,
                ),
            )
            reading = self._get_sensor_reading(connection, reading_id)
            if status == "warning":
                self._ensure_sensor_warning_notification(
                    connection,
                    device=device,
                    reading=reading,
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "sensor_reading",
                reading_id,
                {
                    "device_id": data.device_id,
                    "warehouse_id": device["warehouse_id"],
                    "temperature_c": data.temperature_c,
                    "humidity_percent": data.humidity_percent,
                    "status": status,
                },
                warehouse_id=device["warehouse_id"],
            )
            return reading

    def list_sensor_readings(
        self,
        warehouse_id: int | None = None,
        device_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT
              sr.*,
              sd.name AS device_name,
              w.name AS warehouse_name
            FROM sensor_readings sr
            JOIN sensor_devices sd ON sd.id = sr.device_id
            JOIN warehouses w ON w.id = sr.warehouse_id
        """
        params: tuple[Any, ...] = ()
        filters: list[str] = []
        if warehouse_id is not None:
            filters.append("sr.warehouse_id = ?")
            params = (*params, warehouse_id)
        if device_id is not None:
            filters.append("sr.device_id = ?")
            params = (*params, device_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY sr.recorded_at DESC, sr.id DESC LIMIT ? OFFSET ?"
        connection = self.database.connect()
        try:
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_sensor_readings(
        self, warehouse_id: int | None = None, device_id: int | None = None
    ) -> int:
        query = "SELECT COUNT(*) AS total FROM sensor_readings"
        params: tuple[Any, ...] = ()
        filters: list[str] = []
        if warehouse_id is not None:
            filters.append("warehouse_id = ?")
            params = (*params, warehouse_id)
        if device_id is not None:
            filters.append("device_id = ?")
            params = (*params, device_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        connection = self.database.connect()
        try:
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def update_warehouse(
        self, warehouse_id: int, data: WarehouseUpdate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "warehouses", warehouse_id)
            connection.execute(
                """
                UPDATE warehouses
                SET name = ?,
                    department = ?,
                    tetis_org_id = ?,
                    external_tetis_id = ?,
                    mis_clinic_id = ?,
                    mis_room_id = ?,
                    storage_zone = ?,
                    capacity_limit = ?,
                    storage_conditions = ?,
                    responsible_person = ?
                WHERE id = ?
                """,
                (
                    data.name,
                    data.department,
                    data.tetis_org_id,
                    data.external_tetis_id,
                    data.mis_clinic_id,
                    data.mis_room_id,
                    data.storage_zone,
                    self._optional_decimal_to_db(data.capacity_limit),
                    data.storage_conditions,
                    data.responsible_person,
                    warehouse_id,
                ),
            )
            updated = self._get_by_id(connection, "warehouses", warehouse_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "warehouse",
                warehouse_id,
                {"before": before, "after": updated},
                warehouse_id=warehouse_id,
            )
            return updated

    def set_inventory_lock(
        self, warehouse_id: int, locked: bool, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            self._require(connection, "warehouses", warehouse_id)
            connection.execute(
                "UPDATE warehouses SET inventory_lock = ? WHERE id = ?",
                (1 if locked else 0, warehouse_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.INVENTORY_LOCK,
                "warehouse",
                warehouse_id,
                {"inventory_lock": locked},
                warehouse_id=warehouse_id,
            )
            return self._get_by_id(connection, "warehouses", warehouse_id)

    def create_product(self, data: ProductCreate, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            self._require_active(connection, "categories", data.category_id)
            existing_sku = connection.execute(
                "SELECT id FROM products WHERE sku = ?", [data.sku]
            ).fetchone()
            if existing_sku:
                raise ConflictError(f"Товар с кодом «{data.sku}» уже существует")
            unit = self._normalize_product_unit(data.unit)
            product_id = insert_and_get_id(
                connection,
                """
                INSERT INTO products(
                  name, sku, unit, category_id, reorder_point, safety_stock, is_controlled,
                  barcode, description, certificate_ref, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.name,
                    data.sku,
                    unit,
                    data.category_id,
                    decimal_to_db(data.reorder_point),
                    decimal_to_db(data.safety_stock),
                    1 if data.is_controlled else 0,
                    data.barcode,
                    data.description,
                    data.certificate_ref,
                    1,
                ),
            )
            self._audit(connection, actor_id, AuditAction.CREATE, "product", product_id, data)
            return self._get_by_id(connection, "products", product_id)

    def list_products(
        self, limit: int = 100, offset: int = 0, q: str | None = None
    ) -> list[dict[str, Any]]:
        if not q or not q.strip():
            return self._list_table("products", "name, id", limit, offset, where="is_active = 1")
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        search = q.strip().casefold()
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT * FROM products
                WHERE is_active = 1
                ORDER BY name, id
                """
            ).fetchall()
            searchable_fields = ("name", "sku", "barcode", "certificate_ref")
            filtered = []
            for row in rows:
                item = dict(row)
                haystack = " ".join(str(item.get(field) or "") for field in searchable_fields).casefold()
                if search in haystack:
                    filtered.append(item)
            return filtered[safe_offset : safe_offset + safe_limit]
        finally:
            self._close_connection(connection)

    def get_product_by_barcode(self, barcode: str) -> "dict[str, Any] | None":
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT * FROM products WHERE is_active = 1 AND barcode = ?",
                [barcode.strip()],
            ).fetchone()
            return dict(row) if row else None
        finally:
            self._close_connection(connection)

    def get_product_barcode_label(self, product_id: int, symbology: str = "code128") -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._build_product_barcode_label(connection, product_id, symbology=symbology)
        finally:
            self._close_connection(connection)

    def get_product_barcode_labels(self, product_ids: list[int], symbology: str = "code128") -> dict[str, Any]:
        unique_ids = list(dict.fromkeys(product_ids))
        if not unique_ids:
            raise ValidationError("At least one product is required")
        connection = self.database.connect()
        try:
            labels = [
                self._build_product_barcode_label(connection, product_id, symbology=symbology)
                for product_id in unique_ids
            ]
            return {
                "labels": labels,
                "zpl": "\n".join(label["zpl"] for label in labels),
                "epl": "\n".join(label["epl"] for label in labels),
            }
        finally:
            self._close_connection(connection)

    def get_batch_receipt_print_form(self, batch_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            row = connection.execute(
                """
                SELECT
                  b.id AS batch_id,
                  b.lot,
                  b.serial_number,
                  b.expires_on,
                  b.unit_price,
                  b.received_at,
                  p.name AS product_name,
                  p.sku,
                  p.unit,
                  p.barcode,
                  s.name AS supplier_name,
                  w.name AS warehouse_name,
                  sb.quantity
                FROM batches b
                JOIN products p ON p.id = b.product_id
                JOIN suppliers s ON s.id = b.supplier_id
                LEFT JOIN stock_balances sb ON sb.batch_id = b.id
                LEFT JOIN warehouses w ON w.id = sb.warehouse_id
                WHERE b.id = ?
                ORDER BY sb.quantity DESC NULLS LAST
                LIMIT 1
                """,
                (batch_id,),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"batches#{batch_id} not found")
            item = dict(row)
            return {
                "document_type": "receipt",
                "batch_id": batch_id,
                "product_name": item["product_name"],
                "sku": item.get("sku"),
                "lot": item["lot"],
                "serial_number": item.get("serial_number"),
                "expires_on": item.get("expires_on"),
                "unit_price": str(item["unit_price"]),
                "quantity": str(item["quantity"]) if item.get("quantity") is not None else "0",
                "unit": item.get("unit"),
                "warehouse_name": item["warehouse_name"] if item.get("warehouse_name") else "—",
                "supplier_name": item["supplier_name"],
                "received_at": str(item["received_at"]),
                "barcode": item.get("barcode"),
            }
        finally:
            self._close_connection(connection)

    def get_batch_price_label(self, batch_id: int, symbology: str = "code128") -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._build_batch_price_label(connection, batch_id, symbology=symbology)
        finally:
            self._close_connection(connection)

    def get_batch_price_labels(self, batch_ids: list[int], symbology: str = "code128") -> dict[str, Any]:
        unique_ids = list(dict.fromkeys(batch_ids))
        if not unique_ids:
            raise ValidationError("At least one batch is required")
        connection = self.database.connect()
        try:
            labels = [
                self._build_batch_price_label(connection, batch_id, symbology=symbology)
                for batch_id in unique_ids
            ]
            return {
                "labels": labels,
                "zpl": "\n".join(label["zpl"] for label in labels),
                "epl": "\n".join(label["epl"] for label in labels),
            }
        finally:
            self._close_connection(connection)

    def update_product(
        self, product_id: int, data: ProductUpdate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "products", product_id)
            self._require_active(connection, "categories", data.category_id)
            existing_sku = connection.execute(
                "SELECT id FROM products WHERE sku = ? AND id != ?", [data.sku, product_id]
            ).fetchone()
            if existing_sku:
                raise ConflictError(f"Товар с кодом «{data.sku}» уже существует")
            unit = self._normalize_product_unit(data.unit)
            connection.execute(
                """
                UPDATE products
                SET name = ?, sku = ?, unit = ?, category_id = ?,
                    reorder_point = ?, safety_stock = ?, is_controlled = ?,
                    barcode = ?, description = ?, certificate_ref = ?
                WHERE id = ?
                """,
                (
                    data.name,
                    data.sku,
                    unit,
                    data.category_id,
                    decimal_to_db(data.reorder_point),
                    decimal_to_db(data.safety_stock),
                    1 if data.is_controlled else 0,
                    data.barcode,
                    data.description,
                    data.certificate_ref,
                    product_id,
                ),
            )
            updated = self._get_by_id(connection, "products", product_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "product",
                product_id,
                {"before": before, "after": updated},
            )
            return updated


    def update_product_certificate_ref(
        self, product_id: int, certificate_ref: str | None, actor_id: str = "system"
    ) -> dict:
        """Update only the certificate_ref field of a product."""
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "products", product_id)
            connection.execute(
                "UPDATE products SET certificate_ref = ? WHERE id = ?",
                (certificate_ref, product_id),
            )
            updated = self._get_by_id(connection, "products", product_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "product",
                product_id,
                {"before": {"certificate_ref": before.get("certificate_ref")},
                 "after": {"certificate_ref": updated.get("certificate_ref")}},
            )
        return dict(updated)

    def update_product_image_ref(
        self, product_id: int, image_path: str | None, actor_id: str = "system"
    ) -> dict:
        """Update only the image_path field of a product."""
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "products", product_id)
            connection.execute(
                "UPDATE products SET image_path = ? WHERE id = ?",
                (image_path, product_id),
            )
            updated = self._get_by_id(connection, "products", product_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "product",
                product_id,
                {"before": {"image_path": before.get("image_path")},
                 "after": {"image_path": updated.get("image_path")}},
            )
        return dict(updated)

    def delete_product(self, product_id: int, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "products", product_id)
            connection.execute("UPDATE products SET is_active = ? WHERE id = ?", (0, product_id))
            updated = self._get_by_id(connection, "products", product_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.DELETE,
                "product",
                product_id,
                {"before": before, "after": updated},
            )
            return updated

    def receive(self, data: ReceiptCreate, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            batch_id = self._apply_receipt_line(
                connection,
                supplier_id=data.supplier_id,
                warehouse_id=data.warehouse_id,
                product_id=data.product_id,
                quantity=data.quantity,
                unit_price=data.unit_price,
                lot=data.lot,
                serial_number=data.serial_number,
                expires_on=data.expires_on,
                quarantine=data.quarantine,
                actor_id=actor_id,
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.RECEIPT,
                "batch",
                batch_id,
                data,
                warehouse_id=data.warehouse_id,
            )
            return self._get_batch(connection, batch_id)

    def list_supplier_price_history(
        self,
        supplier_id: int,
        product_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT
              h.id,
              h.supplier_id,
              s.name AS supplier_name,
              h.product_id,
              p.name AS product_name,
              p.sku,
              h.batch_id,
              h.lot,
              h.unit_price,
              h.source,
              h.recorded_at
            FROM supplier_price_history h
            JOIN suppliers s ON s.id = h.supplier_id
            JOIN products p ON p.id = h.product_id
            WHERE h.supplier_id = ?
        """
        params: tuple[Any, ...] = (supplier_id,)
        if product_id is not None:
            query += " AND h.product_id = ?"
            params = (*params, product_id)
        query += " ORDER BY h.recorded_at DESC, h.id DESC LIMIT ? OFFSET ?"
        connection = self.database.connect()
        try:
            self._require(connection, "suppliers", supplier_id)
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            history = []
            for row in rows:
                item = dict(row)
                item["unit_price"] = Decimal(str(item["unit_price"]))
                history.append(item)
            return history
        finally:
            self._close_connection(connection)

    def count_supplier_price_history(self, supplier_id: int, product_id: int | None = None) -> int:
        query = "SELECT COUNT(*) AS total FROM supplier_price_history WHERE supplier_id = ?"
        params: tuple[Any, ...] = (supplier_id,)
        if product_id is not None:
            query += " AND product_id = ?"
            params = (*params, product_id)
        connection = self.database.connect()
        try:
            self._require(connection, "suppliers", supplier_id)
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def create_receipt_document(
        self, data: ReceiptDocumentCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        if not data.lines:
            raise ValidationError("Receipt document must contain at least one line")
        with self.database.transaction() as connection:
            self._ensure_warehouse_open(connection, data.warehouse_id)
            self._require(connection, "suppliers", data.supplier_id)
            document_id = self._create_document(
                connection,
                StockDocumentType.RECEIPT,
                data.warehouse_id,
                actor_id,
                supplier_id=data.supplier_id,
                external_ref=getattr(data, "external_ref", None),
                notes=getattr(data, "notes", None),
            )
            for line in data.lines:
                self._require(connection, "products", line.product_id)
                connection.execute(
                    """
                    INSERT INTO stock_document_lines(
                      document_id, product_id, quantity, unit_price, lot, serial_number, expires_on, quarantine
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        document_id,
                        line.product_id,
                        decimal_to_db(line.quantity),
                        decimal_to_db(line.unit_price),
                        line.lot,
                        line.serial_number,
                        line.expires_on.isoformat() if line.expires_on else None,
                        1 if line.quarantine else 0,
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "stock_document",
                document_id,
                data,
                warehouse_id=data.warehouse_id,
            )
            return self._get_document(connection, document_id)

    def create_writeoff_document(
        self, data: WriteOffDocumentCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        if not data.lines:
            raise ValidationError("Write-off document must contain at least one line")
        with self.database.transaction() as connection:
            self._ensure_warehouse_open(connection, data.warehouse_id)
            document_id = self._create_document(
                connection, StockDocumentType.WRITE_OFF, data.warehouse_id, actor_id
            )
            for line in data.lines:
                self._ensure_batch_available(connection, line.batch_id)
                connection.execute(
                    """
                    INSERT INTO stock_document_lines(
                      document_id, batch_id, quantity, reason,
                      patient_id, doctor_id, medical_record_no,
                      second_approver_id, second_approval_note
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        document_id,
                        line.batch_id,
                        decimal_to_db(line.quantity),
                        line.reason,
                        line.patient_id,
                        line.doctor_id,
                        line.medical_record_no,
                        line.second_approver_id,
                        line.second_approval_note,
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "stock_document",
                document_id,
                data,
                warehouse_id=data.warehouse_id,
            )
            return self._get_document(connection, document_id)

    def create_transfer_document(
        self, data: TransferDocumentCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        if not data.lines:
            raise ValidationError("Transfer document must contain at least one line")
        with self.database.transaction() as connection:
            self._ensure_warehouse_open(connection, data.source_warehouse_id)
            document_id = self._create_document(
                connection, StockDocumentType.TRANSFER, data.source_warehouse_id, actor_id
            )
            for line in data.lines:
                if data.source_warehouse_id == line.target_warehouse_id:
                    raise ValidationError("Source and target warehouses must be different")
                self._ensure_warehouse_open(connection, line.target_warehouse_id)
                self._ensure_batch_available(connection, line.batch_id)
                connection.execute(
                    """
                    INSERT INTO stock_document_lines(
                      document_id, batch_id, target_warehouse_id, quantity, reason
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        document_id,
                        line.batch_id,
                        line.target_warehouse_id,
                        decimal_to_db(line.quantity),
                        line.reason,
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "stock_document",
                document_id,
                data,
                warehouse_id=data.source_warehouse_id,
            )
            return self._get_document(connection, document_id)

    def create_department_return_document(
        self, data: DepartmentReturnDocumentCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        if not data.lines:
            raise ValidationError("Department return document must contain at least one line")
        with self.database.transaction() as connection:
            self._ensure_warehouse_open(connection, data.source_warehouse_id)
            document_id = self._create_document(
                connection, StockDocumentType.DEPARTMENT_RETURN, data.source_warehouse_id, actor_id
            )
            for line in data.lines:
                if data.source_warehouse_id == line.target_warehouse_id:
                    raise ValidationError("Source and target warehouses must be different")
                self._ensure_warehouse_open(connection, line.target_warehouse_id)
                self._ensure_batch_available(connection, line.batch_id)
                connection.execute(
                    """
                    INSERT INTO stock_document_lines(
                      document_id, batch_id, target_warehouse_id, quantity, reason
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        document_id,
                        line.batch_id,
                        line.target_warehouse_id,
                        decimal_to_db(line.quantity),
                        line.reason,
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "stock_document",
                document_id,
                data,
                warehouse_id=data.source_warehouse_id,
            )
            return self._get_document(connection, document_id)

    def create_supplier_return_document(
        self, data: SupplierReturnDocumentCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        if not data.lines:
            raise ValidationError("Supplier return document must contain at least one line")
        with self.database.transaction() as connection:
            self._ensure_warehouse_open(connection, data.warehouse_id)
            self._require(connection, "suppliers", data.supplier_id)
            document_id = self._create_document(
                connection,
                StockDocumentType.SUPPLIER_RETURN,
                data.warehouse_id,
                actor_id,
                supplier_id=data.supplier_id,
            )
            for line in data.lines:
                self._ensure_batch_available(connection, line.batch_id)
                connection.execute(
                    """
                    INSERT INTO stock_document_lines(
                      document_id, batch_id, quantity, reason
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (
                        document_id,
                        line.batch_id,
                        decimal_to_db(line.quantity),
                        line.reason,
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "stock_document",
                document_id,
                data,
                warehouse_id=data.warehouse_id,
            )
            return self._get_document(connection, document_id)

    def create_repack_document(
        self, data: RepackDocumentCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        if not data.lines:
            raise ValidationError("Repack document must contain at least one line")
        with self.database.transaction() as connection:
            self._ensure_warehouse_open(connection, data.warehouse_id)
            document_id = self._create_document(
                connection, StockDocumentType.REPACK, data.warehouse_id, actor_id
            )
            for line in data.lines:
                self._validate_repack_numbers(
                    source_quantity=line.quantity,
                    target_quantity=line.target_quantity,
                    conversion_factor=line.conversion_factor,
                    loss_quantity=line.loss_quantity,
                )
                self._ensure_batch_available(connection, line.batch_id)
                self._require(connection, "products", line.target_product_id)
                connection.execute(
                    """
                    INSERT INTO stock_document_lines(
                      document_id, batch_id, target_product_id, quantity,
                      target_quantity, conversion_factor, loss_quantity,
                      target_unit_price, target_lot, target_expires_on,
                      quarantine, reason
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        document_id,
                        line.batch_id,
                        line.target_product_id,
                        decimal_to_db(line.quantity),
                        decimal_to_db(line.target_quantity),
                        decimal_to_db(line.conversion_factor),
                        decimal_to_db(line.loss_quantity),
                        decimal_to_db(line.target_unit_price) if line.target_unit_price is not None else None,
                        line.target_lot,
                        line.target_expires_on.isoformat() if line.target_expires_on else None,
                        1 if line.quarantine else 0,
                        line.reason,
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "stock_document",
                document_id,
                data,
                warehouse_id=data.warehouse_id,
            )
            return self._get_document(connection, document_id)

    def post_stock_document(self, document_id: int, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            document = self._get_document(connection, document_id)
            if document["status"] == StockDocumentStatus.POSTED:
                return document
            if document["status"] not in {StockDocumentStatus.DRAFT, StockDocumentStatus.APPROVED}:
                raise ValidationError(f"Cannot post document in status {document['status']}")
            self._ensure_warehouse_open(connection, document["warehouse_id"])
            lines = connection.execute(
                "SELECT * FROM stock_document_lines WHERE document_id = ? ORDER BY id",
                (document_id,),
            ).fetchall()
            if not lines:
                raise ValidationError("Cannot post empty document")
            if document["document_type"] == StockDocumentType.RECEIPT:
                for line in lines:
                    self._apply_receipt_line(
                        connection,
                        supplier_id=document["supplier_id"],
                        warehouse_id=document["warehouse_id"],
                        product_id=line["product_id"],
                        quantity=Decimal(line["quantity"]),
                        unit_price=Decimal(line["unit_price"]),
                        lot=line["lot"],
                        serial_number=line["serial_number"],
                        expires_on=self._date_from_db(line["expires_on"]) if line["expires_on"] else None,
                        quarantine=bool(line["quarantine"]),
                        actor_id=actor_id,
                    )
            elif document["document_type"] == StockDocumentType.WRITE_OFF:
                for line in lines:
                    self._apply_writeoff_line(
                        connection,
                        batch_id=line["batch_id"],
                        warehouse_id=document["warehouse_id"],
                        quantity=Decimal(line["quantity"]),
                        reason=line["reason"],
                        patient_id=line["patient_id"],
                        doctor_id=line["doctor_id"],
                        medical_record_no=line["medical_record_no"],
                        second_approver_id=line["second_approver_id"],
                        second_approval_note=line["second_approval_note"],
                    )
            elif document["document_type"] == StockDocumentType.TRANSFER:
                for line in lines:
                    self._apply_transfer(
                        connection,
                        TransferCreate(
                            batch_id=line["batch_id"],
                            source_warehouse_id=document["warehouse_id"],
                            target_warehouse_id=line["target_warehouse_id"],
                            quantity=Decimal(line["quantity"]),
                            reason=line["reason"],
                        ),
                    )
            elif document["document_type"] == StockDocumentType.DEPARTMENT_RETURN:
                for line in lines:
                    self._apply_transfer(
                        connection,
                        TransferCreate(
                            batch_id=line["batch_id"],
                            source_warehouse_id=document["warehouse_id"],
                            target_warehouse_id=line["target_warehouse_id"],
                            quantity=Decimal(line["quantity"]),
                            reason=f"Возврат от отделения: {line['reason']}",
                        ),
                    )
            elif document["document_type"] == StockDocumentType.SUPPLIER_RETURN:
                for line in lines:
                    self._apply_supplier_return_line(
                        connection,
                        batch_id=line["batch_id"],
                        warehouse_id=document["warehouse_id"],
                        supplier_id=document["supplier_id"],
                        quantity=Decimal(line["quantity"]),
                        reason=line["reason"],
                    )
            elif document["document_type"] == StockDocumentType.REPACK:
                for line in lines:
                    self._apply_repack_line(
                        connection,
                        document_id=document_id,
                        warehouse_id=document["warehouse_id"],
                        source_batch_id=line["batch_id"],
                        target_product_id=line["target_product_id"],
                        source_quantity=Decimal(line["quantity"]),
                        target_quantity=Decimal(line["target_quantity"]),
                        conversion_factor=Decimal(line["conversion_factor"]),
                        loss_quantity=Decimal(line["loss_quantity"] or "0"),
                        target_unit_price=Decimal(line["target_unit_price"]) if line["target_unit_price"] is not None else None,
                        target_lot=line["target_lot"],
                        target_expires_on=self._date_from_db(line["target_expires_on"]) if line["target_expires_on"] else None,
                        quarantine=bool(line["quarantine"]),
                        reason=line["reason"],
                        actor_id=actor_id,
                    )
            else:
                raise ValidationError(f"Unsupported document type: {document['document_type']}")
            connection.execute(
                """
                UPDATE stock_documents
                SET status = ?, posted_at = ?
                WHERE id = ?
                """,
                (StockDocumentStatus.POSTED, now_iso(), document_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.REPACK if document["document_type"] == StockDocumentType.REPACK else AuditAction.UPDATE,
                "stock_document",
                document_id,
                {"status": StockDocumentStatus.POSTED},
                warehouse_id=document["warehouse_id"],
            )
            return self._get_document(connection, document_id)

    def approve_stock_document(self, document_id: int, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            document = self._get_document(connection, document_id)
            if document["status"] == StockDocumentStatus.APPROVED:
                return document
            if document["status"] != StockDocumentStatus.DRAFT:
                raise ValidationError(f"Cannot approve document in status {document['status']}")
            connection.execute(
                """
                UPDATE stock_documents
                SET status = ?, approved_by = ?, approved_at = ?
                WHERE id = ?
                """,
                (StockDocumentStatus.APPROVED, actor_id, now_iso(), document_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "stock_document",
                document_id,
                {"status": StockDocumentStatus.APPROVED},
                warehouse_id=document["warehouse_id"],
            )
            return self._get_document(connection, document_id)

    def cancel_stock_document(self, document_id: int, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            document = self._get_document(connection, document_id)
            if document["status"] == StockDocumentStatus.CANCELLED:
                return document
            if document["status"] not in {StockDocumentStatus.DRAFT, StockDocumentStatus.APPROVED}:
                raise ValidationError(f"Cannot cancel document in status {document['status']}")
            connection.execute(
                """
                UPDATE stock_documents
                SET status = ?
                WHERE id = ?
                """,
                (StockDocumentStatus.CANCELLED, document_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "stock_document",
                document_id,
                {"status": StockDocumentStatus.CANCELLED},
                warehouse_id=document["warehouse_id"],
            )
            return self._get_document(connection, document_id)

    def update_batch_status(
        self, batch_id: int, status: BatchStatus, reason: str | None, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            self._require(connection, "batches", batch_id)
            warehouse_ids = self._batch_warehouse_ids(connection, batch_id)
            if not warehouse_ids:
                raise ValidationError("Batch has no stock balances")
            batch = self._get_batch(connection, batch_id)
            if batch["status"] == status:
                return batch
            connection.execute("UPDATE batches SET status = ? WHERE id = ?", (status, batch_id))
            if status == BatchStatus.QUARANTINE:
                for warehouse_id in warehouse_ids:
                    self._ensure_quarantine_review(
                        connection,
                        batch_id=batch_id,
                        warehouse_id=warehouse_id,
                        actor_id=actor_id,
                    )
            elif status == BatchStatus.AVAILABLE:
                self._close_open_quarantine_reviews(
                    connection,
                    batch_id=batch_id,
                    status=QuarantineReviewStatus.APPROVED,
                    actor_id=actor_id,
                    reason=reason,
                )
            elif status == BatchStatus.BLOCKED:
                self._close_open_quarantine_reviews(
                    connection,
                    batch_id=batch_id,
                    status=QuarantineReviewStatus.REJECTED,
                    actor_id=actor_id,
                    reason=reason,
                )
            payload = {"status": status, "reason": reason, "warehouse_ids": warehouse_ids}
            for warehouse_id in warehouse_ids:
                self._audit(
                    connection,
                    actor_id,
                    AuditAction.UPDATE,
                    "batch",
                    batch_id,
                    payload,
                    warehouse_id=warehouse_id,
                )
            return self._get_batch(connection, batch_id)

    def recall_batch(
        self, batch_id: int, data: BatchRecallCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            batch = dict(self._require(connection, "batches", batch_id))
            balances = self._batch_balances(connection, batch_id)
            affected_balances = [
                balance
                for balance in balances
                if Decimal(balance["total_quantity"]) > Decimal("0")
            ]
            if not affected_balances:
                raise ValidationError("Cannot recall a batch with no stock balances")
            connection.execute(
                "UPDATE batches SET status = ? WHERE id = ?",
                (BatchStatus.BLOCKED, batch_id),
            )
            recall_id = insert_and_get_id(
                connection,
                """
                INSERT INTO batch_recalls(
                  batch_id, product_id, reason, source, reference, created_by, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    batch_id,
                    batch["product_id"],
                    data.reason,
                    data.source,
                    data.reference,
                    actor_id,
                    now_iso(),
                ),
            )
            notifications = [
                self._ensure_recall_notification(
                    connection,
                    batch_id=batch_id,
                    product_id=batch["product_id"],
                    warehouse_id=balance["warehouse_id"],
                    lot=batch["lot"],
                    reason=data.reason,
                    free_quantity=balance["free_quantity"],
                )
                for balance in affected_balances
            ]
            payload = {
                "reason": data.reason,
                "source": data.source,
                "reference": data.reference,
                "affected_warehouse_ids": [row["warehouse_id"] for row in affected_balances],
            }
            for balance in affected_balances:
                self._audit(
                    connection,
                    actor_id,
                    AuditAction.RECALL,
                    "batch",
                    batch_id,
                    payload,
                    warehouse_id=balance["warehouse_id"],
                )
            return {
                "recall": self._get_batch_recall(connection, recall_id),
                "batch": self._get_batch(connection, batch_id),
                "affected_warehouses": affected_balances,
                "notifications": notifications,
            }

    def list_batch_recalls(
        self,
        batch_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        connection = self.database.connect()
        try:
            return self._batch_recalls(
                connection,
                batch_id=batch_id,
                limit=safe_limit,
                offset=safe_offset,
            )
        finally:
            self._close_connection(connection)

    def count_batch_recalls(self, batch_id: int | None = None) -> int:
        connection = self.database.connect()
        try:
            query = "SELECT COUNT(*) AS total FROM batch_recalls"
            params: tuple[Any, ...] = ()
            if batch_id is not None:
                query += " WHERE batch_id = ?"
                params = (batch_id,)
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def unblock_batch(self, batch_id: int, reason: str = "", actor_id: str = "system") -> dict:
        with self.database.transaction() as connection:
            batch = dict(self._require(connection, "batches", batch_id))
            if batch["status"] != "blocked":
                from app.domain.errors import ValidationError as VE
                raise VE(f"Batch {batch_id} is not blocked (status={batch['status']})")
            connection.execute(
                "UPDATE batches SET status = ? WHERE id = ?",
                ("active", batch_id),
            )
            payload = {"reason": reason, "prev_status": "blocked"}
            # Audit in all warehouses that hold this batch
            balances = self._batch_balances(connection, batch_id)
            warehouse_ids = list({b["warehouse_id"] for b in balances})
            for wid in warehouse_ids:
                self._audit(connection, actor_id, "unblock", "batch", batch_id, payload, warehouse_id=wid)
            return self._get_batch(connection, batch_id)

    def get_recall_stats(self) -> dict:
        with self.database.transaction() as connection:
            total = (connection.execute("SELECT COUNT(*) AS c FROM batch_recalls").fetchone() or {}).get("c", 0)
            blocked = (connection.execute("SELECT COUNT(*) AS c FROM batches WHERE status = 'blocked'").fetchone() or {}).get("c", 0)
            by_source = connection.execute(
                "SELECT source, COUNT(*) AS cnt FROM batch_recalls GROUP BY source ORDER BY cnt DESC"
            ).fetchall() or []
            recent = connection.execute(
                "SELECT br.id, br.batch_id, br.reason, br.source, br.reference, br.created_by, br.created_at, "
                "p.name AS product_name, b.lot, b.serial_number, b.status AS batch_status "
                "FROM batch_recalls br "
                "JOIN batches b ON b.id = br.batch_id "
                "JOIN products p ON p.id = br.product_id "
                "ORDER BY br.created_at DESC LIMIT 5"
            ).fetchall() or []
        return {
            "total_recalls": int(total),
            "blocked_batches": int(blocked),
            "by_source": [dict(r) for r in by_source],
            "recent": [dict(r) for r in recent],
        }

    def list_quarantine_reviews(
        self,
        warehouse_id: int | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        with self.database.transaction() as connection:
            self._ensure_quarantine_reviews_for_open_batches(connection, warehouse_id=warehouse_id)
            query = """
                SELECT
                  qr.*,
                  b.product_id,
                  b.lot,
                  p.name AS product_name
                FROM quarantine_reviews qr
                JOIN batches b ON b.id = qr.batch_id
                JOIN products p ON p.id = b.product_id
            """
            params: tuple[Any, ...] = ()
            filters: list[str] = []
            if warehouse_id is not None:
                filters.append("qr.warehouse_id = ?")
                params = (*params, warehouse_id)
            if status is not None:
                filters.append("qr.status = ?")
                params = (*params, status)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            query += " ORDER BY qr.due_at IS NULL, qr.due_at, qr.created_at DESC, qr.id DESC LIMIT ? OFFSET ?"
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            return [dict(row) for row in rows]

    def count_quarantine_reviews(
        self, warehouse_id: int | None = None, status: str | None = None
    ) -> int:
        with self.database.transaction() as connection:
            self._ensure_quarantine_reviews_for_open_batches(connection, warehouse_id=warehouse_id)
            query = "SELECT COUNT(*) AS total FROM quarantine_reviews"
            params: tuple[Any, ...] = ()
            filters: list[str] = []
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if status is not None:
                filters.append("status = ?")
                params = (*params, status)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            row = connection.execute(query, params).fetchone()
            return int(row["total"])

    def get_quarantine_review(self, review_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_quarantine_review(connection, review_id)
        finally:
            self._close_connection(connection)

    def get_quarantine_review_protocol(self, review_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            review = self._get_quarantine_review(connection, review_id)
            warehouse = dict(self._require(connection, "warehouses", review["warehouse_id"]))
            protocol = {
                "review_id": review["id"],
                "batch_id": review["batch_id"],
                "product_name": review["product_name"],
                "lot": review["lot"],
                "warehouse_id": review["warehouse_id"],
                "warehouse_name": warehouse["name"],
                "status": review["status"],
                "responsible_id": review["responsible_id"],
                "due_at": review["due_at"],
                "decision_reason": review["decision_reason"],
                "created_by": review["created_by"],
                "decided_by": review["decided_by"],
                "created_at": review["created_at"],
                "updated_at": review["updated_at"],
                "decided_at": review["decided_at"],
            }
            return {**protocol, "csv": self._quarantine_protocol_csv(protocol)}
        finally:
            self._close_connection(connection)

    def update_quarantine_review(
        self,
        review_id: int,
        data: QuarantineReviewUpdate,
        actor_id: str = "system",
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_quarantine_review(connection, review_id)
            if data.status in {QuarantineReviewStatus.APPROVED, QuarantineReviewStatus.REJECTED}:
                if not data.decision_reason or not data.decision_reason.strip():
                    raise ValidationError("Decision reason is required for quarantine decision")
            now = now_iso()
            decided_by = actor_id if data.status in {
                QuarantineReviewStatus.APPROVED,
                QuarantineReviewStatus.REJECTED,
            } else None
            decided_at = now if decided_by else None
            commission_json = json.dumps(data.commission_members) if data.commission_members else None
            resolution_type = data.resolution_type
            disposal_quantity = data.disposal_quantity
            connection.execute(
                """
                UPDATE quarantine_reviews
                SET status = ?,
                    responsible_id = ?,
                    due_at = ?,
                    decision_reason = ?,
                    decided_by = ?,
                    updated_at = ?,
                    decided_at = ?,
                    commission_members = ?,
                    resolution_type = ?,
                    disposal_quantity = ?
                WHERE id = ?
                """,
                (
                    data.status,
                    data.responsible_id,
                    data.due_at.isoformat() if data.due_at else None,
                    data.decision_reason,
                    decided_by,
                    now,
                    decided_at,
                    commission_json,
                    resolution_type,
                    disposal_quantity,
                    review_id,
                ),
            )
            if data.status == QuarantineReviewStatus.APPROVED:
                new_batch_status = BatchStatus.AVAILABLE
            elif data.status == QuarantineReviewStatus.REJECTED:
                new_batch_status = BatchStatus.BLOCKED
            else:
                new_batch_status = BatchStatus.QUARANTINE
            connection.execute(
                "UPDATE batches SET status = ? WHERE id = ?",
                (new_batch_status, before["batch_id"]),
            )
            # Auto-disposal: when rejected with resolution_type=disposal, write off the stock
            if (
                data.status == QuarantineReviewStatus.REJECTED
                and resolution_type == "disposal"
                and disposal_quantity and disposal_quantity > 0
            ):
                try:
                    self._apply_writeoff_line(
                        connection,
                        batch_id=before["batch_id"],
                        warehouse_id=before["warehouse_id"],
                        quantity=Decimal(str(disposal_quantity)),
                        reason=f"Утилизация по результатам карантинной проверки #{review_id}: {data.decision_reason or ''}",
                        patient_id=None,
                        doctor_id=None,
                        medical_record_no=None,
                        second_approver_id=None,
                        second_approval_note=None,
                    )
                except Exception:
                    logger.exception("Failed to auto-dispose quarantine batch %s", before["batch_id"])
            updated = self._get_quarantine_review(connection, review_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "quarantine_review",
                review_id,
                {"before": before, "after": updated},
                warehouse_id=updated["warehouse_id"],
            )
            return updated

    def write_off(self, data: WriteOffCreate, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            movement_id = self._apply_writeoff_line(
                connection,
                batch_id=data.batch_id,
                warehouse_id=data.warehouse_id,
                quantity=data.quantity,
                reason=data.reason,
                patient_id=data.patient_id,
                doctor_id=data.doctor_id,
                medical_record_no=data.medical_record_no,
                second_approver_id=data.second_approver_id,
                second_approval_note=data.second_approval_note,
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.WRITE_OFF,
                "movement",
                movement_id,
                data,
                warehouse_id=data.warehouse_id,
            )
            batch_row = connection.execute(
                "SELECT product_id FROM batches WHERE id = ?", (data.batch_id,)
            ).fetchone()
            if batch_row:
                self._check_and_create_reorder_requests(
                    connection, data.warehouse_id, [int(batch_row["product_id"])]
                )
            return self._get_by_id(connection, "stock_movements", movement_id)

    def write_off_fefo(
        self, data: WriteOffFefoCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            return self._write_off_fefo_within(
                connection,
                actor_id=actor_id,
                product_id=data.product_id,
                warehouse_id=data.warehouse_id,
                quantity=data.quantity,
                reason=data.reason,
                patient_id=data.patient_id,
                doctor_id=data.doctor_id,
                medical_record_no=data.medical_record_no,
                second_approver_id=data.second_approver_id,
                second_approval_note=data.second_approval_note,
            )

    def _write_off_fefo_within(
        self,
        connection: Connection,
        *,
        actor_id: str,
        product_id: int,
        warehouse_id: int,
        quantity: Decimal,
        reason: str,
        patient_id: str | None = None,
        doctor_id: str | None = None,
        medical_record_no: str | None = None,
        second_approver_id: str | None = None,
        second_approval_note: str | None = None,
    ) -> dict[str, Any]:
        self._ensure_warehouse_open(connection, warehouse_id)
        self._require(connection, "products", product_id)
        self._require_controlled_writeoff_metadata(
            connection,
            product_id=product_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            medical_record_no=medical_record_no,
            second_approver_id=second_approver_id,
        )
        rows = connection.execute(
            """
            SELECT
              sb.batch_id,
              sb.quantity,
              sb.reserved_quantity
            FROM stock_balances sb
            JOIN batches b ON b.id = sb.batch_id
            WHERE b.product_id = ?
              AND sb.warehouse_id = ?
              AND b.status = ?
              AND CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL) > 0
            ORDER BY b.expires_on IS NULL, b.expires_on, sb.batch_id
            """,
            (product_id, warehouse_id, BatchStatus.AVAILABLE),
        ).fetchall()
        remaining = quantity
        movement_ids: list[int] = []
        for row in rows:
            if remaining <= 0:
                break
            free = Decimal(row["quantity"]) - Decimal(row["reserved_quantity"])
            line_quantity = min(free, remaining)
            movement_ids.append(
                self._apply_writeoff_line(
                    connection,
                    batch_id=row["batch_id"],
                    warehouse_id=warehouse_id,
                    quantity=line_quantity,
                    reason=reason,
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    medical_record_no=medical_record_no,
                    second_approver_id=second_approver_id,
                    second_approval_note=second_approval_note,
                )
            )
            remaining -= line_quantity
        if remaining > 0:
            raise InsufficientStockError("Not enough FEFO stock for write-off")
        self._audit(
            connection,
            actor_id,
            AuditAction.WRITE_OFF,
            "product",
            product_id,
            {
                "request": {
                    "product_id": product_id,
                    "warehouse_id": warehouse_id,
                    "quantity": decimal_to_db(quantity),
                    "reason": reason,
                },
                "movement_ids": movement_ids,
            },
            warehouse_id=warehouse_id,
        )
        return {
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "quantity": decimal_to_db(quantity),
            "movement_ids": movement_ids,
        }

    def transfer(self, data: TransferCreate, actor_id: str = "system") -> dict[str, Any]:
        if data.source_warehouse_id == data.target_warehouse_id:
            raise ValidationError("Source and target warehouses must be different")
        with self.database.transaction() as connection:
            result = self._apply_transfer(connection, data)
            self._audit(
                connection,
                actor_id,
                AuditAction.TRANSFER,
                "batch",
                data.batch_id,
                {
                    "request": data,
                    "out_movement_id": result["out_movement_id"],
                    "in_movement_id": result["in_movement_id"],
                },
                warehouse_id=data.source_warehouse_id,
            )
            return result

    def return_from_department(
        self, data: DepartmentReturnCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            transfer = self._apply_transfer(
                connection,
                TransferCreate(
                    batch_id=data.batch_id,
                    source_warehouse_id=data.source_warehouse_id,
                    target_warehouse_id=data.target_warehouse_id,
                    quantity=data.quantity,
                    reason=f"Возврат от отделения: {data.reason}",
                ),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.RETURN,
                "batch",
                data.batch_id,
                {"return_type": "from_department", "request": data, "transfer": transfer},
                warehouse_id=data.source_warehouse_id,
            )
            return transfer

    def return_to_supplier(
        self, data: SupplierReturnCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            result = self._apply_supplier_return_line(
                connection,
                batch_id=data.batch_id,
                warehouse_id=data.warehouse_id,
                supplier_id=data.supplier_id,
                quantity=data.quantity,
                reason=data.reason,
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.RETURN,
                "batch",
                data.batch_id,
                {
                    "return_type": "to_supplier",
                    "request": data,
                    "movement_id": result["movement_id"],
                },
                warehouse_id=data.warehouse_id,
            )
            return result

    def reserve(self, data: ReservationCreate, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            self._ensure_warehouse_open(connection, data.warehouse_id)
            self._ensure_batch_available(connection, data.batch_id)
            balance = self._balance_for_update(connection, data.batch_id, data.warehouse_id)
            free = Decimal(balance["quantity"]) - Decimal(balance["reserved_quantity"])
            if free < data.quantity:
                raise InsufficientStockError("Not enough free stock for reservation")
            reservation_id = insert_and_get_id(
                connection,
                """
                INSERT INTO reservations(
                  batch_id, warehouse_id, quantity, reserved_for, status, expires_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.batch_id,
                    data.warehouse_id,
                    decimal_to_db(data.quantity),
                    data.reserved_for,
                    ReservationStatus.RESERVED,
                    data.expires_at.isoformat() if data.expires_at else None,
                    now_iso(),
                ),
            )
            reserved = Decimal(balance["reserved_quantity"]) + data.quantity
            connection.execute(
                """
                UPDATE stock_balances
                SET reserved_quantity = ?
                WHERE batch_id = ? AND warehouse_id = ?
                """,
                (decimal_to_db(reserved), data.batch_id, data.warehouse_id),
            )
            self._movement(
                connection, MovementType.RESERVE, data.batch_id, data.warehouse_id, data.quantity
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.RESERVE,
                "reservation",
                reservation_id,
                data,
                warehouse_id=data.warehouse_id,
            )
            return self._get_by_id(connection, "reservations", reservation_id)

    def release_reservation(
        self, reservation_id: int, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            return self._release_reservation(connection, reservation_id, actor_id)

    def use_reservation(
        self, reservation_id: int, data: ReservationUseCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            reservation = self._require(connection, "reservations", reservation_id)
            if reservation["status"] != ReservationStatus.RESERVED:
                return dict(reservation)
            self._ensure_warehouse_open(connection, reservation["warehouse_id"])
            self._ensure_batch_available(connection, reservation["batch_id"])
            self._require_controlled_writeoff_metadata(
                connection,
                batch_id=reservation["batch_id"],
                patient_id=data.patient_id,
                doctor_id=data.doctor_id,
                medical_record_no=data.medical_record_no,
                second_approver_id=data.second_approver_id,
            )
            balance = self._balance_for_update(
                connection, reservation["batch_id"], reservation["warehouse_id"]
            )
            quantity = Decimal(reservation["quantity"])
            total = Decimal(balance["quantity"])
            reserved = Decimal(balance["reserved_quantity"])
            if total < quantity or reserved < quantity:
                raise InsufficientStockError("Not enough reserved stock for write-off")
            new_total = total - quantity
            new_reserved = reserved - quantity
            connection.execute(
                """
                UPDATE stock_balances
                SET quantity = ?, reserved_quantity = ?
                WHERE batch_id = ? AND warehouse_id = ?
                """,
                (
                    decimal_to_db(new_total),
                    decimal_to_db(new_reserved),
                    reservation["batch_id"],
                    reservation["warehouse_id"],
                ),
            )
            movement_id = self._movement(
                connection,
                MovementType.WRITE_OFF,
                reservation["batch_id"],
                reservation["warehouse_id"],
                quantity,
                reason=data.reason,
                patient_id=data.patient_id,
                doctor_id=data.doctor_id,
                medical_record_no=data.medical_record_no,
                second_approver_id=data.second_approver_id,
                second_approval_note=data.second_approval_note,
            )
            connection.execute(
                "UPDATE reservations SET status = ? WHERE id = ?",
                (ReservationStatus.USED, reservation_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.WRITE_OFF,
                "reservation",
                reservation_id,
                {"status": ReservationStatus.USED, "request": data, "movement_id": movement_id},
                warehouse_id=reservation["warehouse_id"],
            )
            return self._get_by_id(connection, "reservations", reservation_id)

    def expire_reservations(
        self,
        now: datetime | None = None,
        actor_id: str = "system",
        warehouse_id: int | None = None,
    ) -> list[dict[str, Any]]:
        cutoff = (now or datetime.now(UTC)).astimezone(UTC).isoformat()
        with self.database.transaction() as connection:
            params: tuple[Any, ...] = (ReservationStatus.RESERVED, cutoff)
            warehouse_filter = ""
            if warehouse_id is not None:
                self._require(connection, "warehouses", warehouse_id)
                warehouse_filter = " AND warehouse_id = ?"
                params = (*params, warehouse_id)
            rows = connection.execute(
                f"""
                SELECT id FROM reservations
                WHERE status = ?
                  AND expires_at IS NOT NULL
                  AND expires_at <= ?
                  {warehouse_filter}
                ORDER BY expires_at, id
                """,
                params,
            ).fetchall()
            return [self._release_reservation(connection, row["id"], actor_id) for row in rows]

    def create_inventory_session(
        self, data: InventoryCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            warehouse = self._require(connection, "warehouses", data.warehouse_id)
            if int(warehouse["inventory_lock"]):
                raise InventoryLockedError("Warehouse already has active inventory lock")
            connection.execute(
                "UPDATE warehouses SET inventory_lock = 1 WHERE id = ?",
                (data.warehouse_id,),
            )
            session_id = insert_and_get_id(
                connection,
                """
                INSERT INTO inventory_sessions(warehouse_id, status, started_by, started_at)
                VALUES (?, ?, ?, ?)
                """,
                (data.warehouse_id, InventoryStatus.IN_PROGRESS, actor_id, now_iso()),
            )
            responsible_ids = list(dict.fromkeys(item.strip() for item in data.responsible_ids if item.strip()))
            category_ids = list(dict.fromkeys(data.category_ids))
            for category_id in category_ids:
                self._require(connection, "categories", category_id)
                connection.execute(
                    """
                    INSERT INTO inventory_session_categories(session_id, category_id)
                    VALUES (?, ?)
                    """,
                    (session_id, category_id),
                )
            for responsible_id in responsible_ids:
                connection.execute(
                    """
                    INSERT INTO inventory_responsibles(session_id, responsible_id)
                    VALUES (?, ?)
                    """,
                    (session_id, responsible_id),
                )
            category_filter = ""
            params: tuple[Any, ...] = (data.warehouse_id,)
            if category_ids:
                placeholders = ", ".join("?" for _ in category_ids)
                category_filter = f" AND p.category_id IN ({placeholders})"
                params = (*params, *category_ids)
            balances = connection.execute(
                f"""
                SELECT b.product_id, sb.batch_id, sb.quantity
                FROM stock_balances sb
                JOIN batches b ON b.id = sb.batch_id
                JOIN products p ON p.id = b.product_id
                WHERE sb.warehouse_id = ?
                  {category_filter}
                ORDER BY b.product_id, sb.batch_id
                """,
                params,
            ).fetchall()
            for balance in balances:
                connection.execute(
                    """
                    INSERT INTO inventory_lines(
                      session_id, product_id, batch_id, expected_quantity
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (
                        session_id,
                        balance["product_id"],
                        balance["batch_id"],
                        balance["quantity"],
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.INVENTORY_LOCK,
                "inventory_session",
                session_id,
                {
                    "warehouse_id": data.warehouse_id,
                    "line_count": len(balances),
                    "responsible_ids": responsible_ids,
                    "category_ids": category_ids,
                },
                warehouse_id=data.warehouse_id,
            )
            return self._get_inventory_session(connection, session_id)

    def get_inventory_session(self, session_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_inventory_session(connection, session_id)
        finally:
            self._close_connection(connection)

    def get_inventory_print_form(self, session_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            session = self._get_inventory_session(connection, session_id)
            warehouse = dict(self._require(connection, "warehouses", session["warehouse_id"]))
            rows = connection.execute(
                """
                SELECT
                  il.id,
                  il.product_id,
                  il.batch_id,
                  il.expected_quantity,
                  il.actual_quantity,
                  il.difference_quantity,
                  p.name AS product_name,
                  p.sku,
                  p.unit,
                  b.lot,
                  b.expires_on
                FROM inventory_lines il
                JOIN products p ON p.id = il.product_id
                JOIN batches b ON b.id = il.batch_id
                WHERE il.session_id = ?
                ORDER BY p.name, p.sku, b.expires_on, b.id
                """,
                (session_id,),
            ).fetchall()
            lines = [
                {
                    "line_no": index,
                    "product_id": row["product_id"],
                    "product_name": row["product_name"],
                    "sku": row["sku"],
                    "unit": row["unit"],
                    "batch_id": row["batch_id"],
                    "lot": row["lot"],
                    "expires_on": row["expires_on"],
                    "expected_quantity": row["expected_quantity"],
                    "actual_quantity": row["actual_quantity"],
                    "difference_quantity": row["difference_quantity"],
                }
                for index, row in enumerate(rows, start=1)
            ]
            return {
                "session_id": session["id"],
                "warehouse_id": session["warehouse_id"],
                "warehouse_name": warehouse["name"],
                "status": session["status"],
                "started_by": session["started_by"],
                "posted_by": session["posted_by"],
                "started_at": session["started_at"],
                "posted_at": session["posted_at"],
                "summary": session["summary"],
                "count_sheet_csv": self._inventory_print_csv(lines, include_actual=False),
                "reconciliation_csv": self._inventory_print_csv(lines, include_actual=True),
                "lines": lines,
            }
        finally:
            self._close_connection(connection)

    def list_inventory_sessions(
        self, warehouse_id: int | None = None, limit: int = 100, offset: int = 0
    ) -> list[dict[str, Any]]:
        return self._list_table(
            "inventory_sessions",
            "started_at DESC, id DESC",
            limit,
            offset,
            where="warehouse_id = ?",
            params=(warehouse_id,),
        ) if warehouse_id is not None else self._list_table(
            "inventory_sessions", "started_at DESC, id DESC", limit, offset
        )

    def update_inventory_line_count(
        self,
        session_id: int,
        line_id: int,
        data: InventoryLineCountUpdate,
        actor_id: str = "system",
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            session = self._get_inventory_session(connection, session_id)
            if session["status"] != InventoryStatus.IN_PROGRESS:
                raise ValidationError(f"Cannot update inventory in status {session['status']}")
            line = self._require(connection, "inventory_lines", line_id)
            if line["session_id"] != session_id:
                raise NotFoundError("Inventory line not found in session")
            difference = data.actual_quantity - Decimal(line["expected_quantity"])
            connection.execute(
                """
                UPDATE inventory_lines
                SET actual_quantity = ?, difference_quantity = ?
                WHERE id = ?
                """,
                (decimal_to_db(data.actual_quantity), decimal_to_db(difference), line_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "inventory_line",
                line_id,
                {"actual_quantity": data.actual_quantity, "difference_quantity": difference},
                warehouse_id=session["warehouse_id"],
            )
            return self._get_inventory_line(connection, line_id)

    def post_inventory_session(
        self, session_id: int, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            session = self._get_inventory_session(connection, session_id)
            if session["status"] == InventoryStatus.POSTED:
                return session
            if session["status"] != InventoryStatus.IN_PROGRESS:
                raise ValidationError(f"Cannot post inventory in status {session['status']}")
            lines = connection.execute(
                "SELECT * FROM inventory_lines WHERE session_id = ? ORDER BY id",
                (session_id,),
            ).fetchall()
            if not lines:
                raise ValidationError("Inventory session has no lines")
            for line in lines:
                if line["actual_quantity"] is None:
                    raise ValidationError("All inventory lines must have actual quantity")
                balance = self._balance_for_update(
                    connection, line["batch_id"], session["warehouse_id"]
                )
                actual = Decimal(line["actual_quantity"])
                reserved = Decimal(balance["reserved_quantity"])
                if actual < reserved:
                    raise ValidationError("Actual quantity cannot be below reserved quantity")
            for line in lines:
                balance = self._balance_for_update(
                    connection, line["batch_id"], session["warehouse_id"]
                )
                actual = Decimal(line["actual_quantity"])
                expected = Decimal(balance["quantity"])
                difference = actual - expected
                if difference == 0:
                    continue
                connection.execute(
                    """
                    UPDATE stock_balances
                    SET quantity = ?
                    WHERE batch_id = ? AND warehouse_id = ?
                    """,
                    (decimal_to_db(actual), line["batch_id"], session["warehouse_id"]),
                )
                movement_type = MovementType.RECEIPT if difference > 0 else MovementType.WRITE_OFF
                self._movement(
                    connection,
                    movement_type,
                    line["batch_id"],
                    session["warehouse_id"],
                    abs(difference),
                    reason=f"Инвентаризация #{session_id}",
                )
            connection.execute(
                """
                UPDATE inventory_sessions
                SET status = ?, posted_by = ?, posted_at = ?
                WHERE id = ?
                """,
                (InventoryStatus.POSTED, actor_id, now_iso(), session_id),
            )
            connection.execute(
                "UPDATE warehouses SET inventory_lock = 0 WHERE id = ?",
                (session["warehouse_id"],),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.INVENTORY_POST,
                "inventory_session",
                session_id,
                {"status": InventoryStatus.POSTED},
                warehouse_id=session["warehouse_id"],
            )
            return self._get_inventory_session(connection, session_id)

    def cancel_inventory_session(
        self, session_id: int, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            session = self._get_inventory_session(connection, session_id)
            if session["status"] in (InventoryStatus.POSTED, InventoryStatus.CANCELLED):
                return session
            connection.execute(
                """
                UPDATE inventory_sessions
                SET status = ?, cancelled_at = ?
                WHERE id = ?
                """,
                (InventoryStatus.CANCELLED, now_iso(), session_id),
            )
            connection.execute(
                "UPDATE warehouses SET inventory_lock = 0 WHERE id = ?",
                (session["warehouse_id"],),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.INVENTORY_CANCEL,
                "inventory_session",
                session_id,
                {"status": InventoryStatus.CANCELLED},
                warehouse_id=session["warehouse_id"],
            )
            return self._get_inventory_session(connection, session_id)

    def list_balances(
        self,
        product_id: int | None = None,
        warehouse_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT
              b.product_id,
              sb.batch_id,
              sb.warehouse_id,
              sb.quantity AS total_quantity,
              sb.reserved_quantity,
              b.status AS batch_status,
              b.expires_on
            FROM stock_balances sb
            JOIN batches b ON b.id = sb.batch_id
        """
        params: tuple[Any, ...] = ()
        filters: list[str] = []
        if product_id is not None:
            filters.append("b.product_id = ?")
            params = (*params, product_id)
        if warehouse_id is not None:
            filters.append("sb.warehouse_id = ?")
            params = (*params, warehouse_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY b.expires_on IS NULL, b.expires_on, sb.batch_id LIMIT ? OFFSET ?"
        params = (*params, safe_limit, safe_offset)
        connection = self.database.connect()
        try:
            rows = connection.execute(query, params).fetchall()
            return [self._balance_payload(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_balances(
        self, product_id: int | None = None, warehouse_id: int | None = None
    ) -> int:
        query = """
            SELECT COUNT(*) AS total
            FROM stock_balances sb
            JOIN batches b ON b.id = sb.batch_id
        """
        params: tuple[Any, ...] = ()
        filters: list[str] = []
        if product_id is not None:
            filters.append("b.product_id = ?")
            params = (*params, product_id)
        if warehouse_id is not None:
            filters.append("sb.warehouse_id = ?")
            params = (*params, warehouse_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        connection = self.database.connect()
        try:
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def list_stock_movements(
        self,
        batch_id: int | None = None,
        product_id: int | None = None,
        warehouse_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT sm.*
            FROM stock_movements sm
            JOIN batches b ON b.id = sm.batch_id
        """
        filters: list[str] = []
        params: tuple[Any, ...] = ()
        if batch_id is not None:
            filters.append("sm.batch_id = ?")
            params = (*params, batch_id)
        if product_id is not None:
            filters.append("b.product_id = ?")
            params = (*params, product_id)
        if warehouse_id is not None:
            filters.append("sm.warehouse_id = ?")
            params = (*params, warehouse_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY sm.created_at DESC, sm.id DESC LIMIT ? OFFSET ?"
        params = (*params, safe_limit, safe_offset)
        connection = self.database.connect()
        try:
            rows = connection.execute(query, params).fetchall()
            movements = [dict(row) for row in rows]
            for movement in movements:
                self._redact_movement_payload(movement)
            return movements
        finally:
            self._close_connection(connection)

    def count_stock_movements(
        self,
        batch_id: int | None = None,
        product_id: int | None = None,
        warehouse_id: int | None = None,
    ) -> int:
        query = """
            SELECT COUNT(*) AS total
            FROM stock_movements sm
            JOIN batches b ON b.id = sm.batch_id
        """
        filters: list[str] = []
        params: tuple[Any, ...] = ()
        if batch_id is not None:
            filters.append("sm.batch_id = ?")
            params = (*params, batch_id)
        if product_id is not None:
            filters.append("b.product_id = ?")
            params = (*params, product_id)
        if warehouse_id is not None:
            filters.append("sm.warehouse_id = ?")
            params = (*params, warehouse_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        connection = self.database.connect()
        try:
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def abc_xyz_analysis(
        self, analysis_days: int = 90, warehouse_id: int | None = None
    ) -> dict[str, Any]:
        if analysis_days < 1:
            raise ValidationError("Analysis period must be at least one day")
        generated_at = datetime.now(UTC)
        since = generated_at - timedelta(days=analysis_days)
        bucket_count = 3
        bucket_seconds = max(1, analysis_days * 24 * 60 * 60 / bucket_count)
        connection = self.database.connect()
        try:
            if warehouse_id is not None:
                self._require(connection, "warehouses", warehouse_id)
            products = [
                dict(row)
                for row in connection.execute(
                    """
                    SELECT id, name, sku, reorder_point, safety_stock
                    FROM products
                    ORDER BY name, id
                    """
                ).fetchall()
            ]
            balance_filter = ""
            balance_params: tuple[Any, ...] = ()
            if warehouse_id is not None:
                balance_filter = " WHERE sb.warehouse_id = ?"
                balance_params = (warehouse_id,)
            balance_rows = connection.execute(
                f"""
                SELECT b.product_id,
                       SUM(CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL))
                         AS free_quantity
                FROM stock_balances sb
                JOIN batches b ON b.id = sb.batch_id
                {balance_filter}
                GROUP BY b.product_id
                """,
                balance_params,
            ).fetchall()
            free_by_product = {
                row["product_id"]: Decimal(str(row["free_quantity"] or 0))
                for row in balance_rows
            }

            movement_filters = [
                "sm.movement_type IN (?, ?, ?)",
                "sm.created_at >= ?",
            ]
            movement_params: tuple[Any, ...] = (
                MovementType.WRITE_OFF,
                MovementType.TRANSFER_OUT,
                MovementType.RETURN_TO_SUPPLIER,
                since.isoformat(),
            )
            if warehouse_id is not None:
                movement_filters.append("sm.warehouse_id = ?")
                movement_params = (*movement_params, warehouse_id)
            movement_rows = connection.execute(
                f"""
                SELECT
                  b.product_id,
                  sm.quantity,
                  sm.created_at,
                  b.unit_price
                FROM stock_movements sm
                JOIN batches b ON b.id = sm.batch_id
                WHERE {" AND ".join(movement_filters)}
                ORDER BY sm.created_at, sm.id
                """,
                movement_params,
            ).fetchall()
        finally:
            self._close_connection(connection)

        stats: dict[int, dict[str, Any]] = {
            product["id"]: {
                "quantity": Decimal("0"),
                "value": Decimal("0"),
                "buckets": [Decimal("0") for _ in range(bucket_count)],
                "movement_count": 0,
            }
            for product in products
        }
        for row in movement_rows:
            product_id = row["product_id"]
            if product_id not in stats:
                continue
            quantity = Decimal(row["quantity"])
            unit_price = Decimal(row["unit_price"])
            movement_created_at = self._datetime_from_db(row["created_at"]).astimezone(UTC)
            bucket_index = int((movement_created_at - since).total_seconds() // bucket_seconds)
            bucket_index = max(0, min(bucket_count - 1, bucket_index))
            stats[product_id]["quantity"] += quantity
            stats[product_id]["value"] += quantity * unit_price
            stats[product_id]["buckets"][bucket_index] += quantity
            stats[product_id]["movement_count"] += 1

        total_value = sum((item["value"] for item in stats.values()), Decimal("0"))
        sorted_products = sorted(
            products,
            key=lambda product: (
                -stats[product["id"]]["value"],
                product["name"],
                product["id"],
            ),
        )
        cumulative_value = Decimal("0")
        items: list[dict[str, Any]] = []
        for product in sorted_products:
            product_stats = stats[product["id"]]
            if total_value <= 0 or product_stats["value"] <= 0:
                abc_class = "C"
            else:
                cumulative_share_before = cumulative_value / total_value
                if cumulative_share_before < Decimal("0.80"):
                    abc_class = "A"
                elif cumulative_share_before < Decimal("0.95"):
                    abc_class = "B"
                else:
                    abc_class = "C"
            cumulative_value += product_stats["value"]
            xyz_class = self._xyz_class(product_stats["buckets"])
            current_free = free_by_product.get(product["id"], Decimal("0"))
            reorder_point = Decimal(product["reorder_point"])
            safety_stock = Decimal(product["safety_stock"])
            recommended_order = max(
                Decimal("0"),
                reorder_point + safety_stock - current_free,
            )
            items.append(
                {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "sku": product["sku"],
                    "abc_class": abc_class,
                    "xyz_class": xyz_class,
                    "consumption_quantity": self._report_decimal(product_stats["quantity"]),
                    "consumption_value": self._report_decimal(product_stats["value"]),
                    "current_free_quantity": self._report_decimal(current_free),
                    "reorder_point": product["reorder_point"],
                    "safety_stock": product["safety_stock"],
                    "recommended_order_quantity": self._report_decimal(recommended_order),
                    "recommendation": self._abc_xyz_recommendation(
                        abc_class, xyz_class, recommended_order
                    ),
                    "movement_count": product_stats["movement_count"],
                    "suggested_reorder_point": self._report_decimal(
                        self._xyz_suggested_reorder_point(xyz_class, product_stats["quantity"], analysis_days)
                    ),
                }
            )
        return {
            "items": items,
            "analysis_days": analysis_days,
            "warehouse_id": warehouse_id,
            "generated_at": generated_at.isoformat(),
        }


    def apply_xyz_reorder_suggestions(
        self, analysis_days=90, warehouse_id=None, actor_id="system"
    ):
        """Update product reorder_points based on XYZ-analysis suggestions."""
        analysis = self.abc_xyz_analysis(analysis_days=analysis_days, warehouse_id=warehouse_id)
        updated = []
        with self.database.transaction() as connection:
            for item in analysis["items"]:
                suggested = Decimal(str(item["suggested_reorder_point"] or 0))
                current = Decimal(str(item["reorder_point"] or 0))
                if suggested <= 0 or suggested == current:
                    continue
                connection.execute(
                    "UPDATE products SET reorder_point = ? WHERE id = ?",
                    (decimal_to_db(suggested), item["product_id"]),
                )
                self._audit(
                    connection, actor_id, AuditAction.UPDATE, "product", item["product_id"],
                    {"reorder_point": {"from": str(current), "to": str(suggested), "source": "xyz_suggestion"}},
                )
                updated.append({"product_id": item["product_id"], "product_name": item["product_name"], "old_reorder_point": str(current), "new_reorder_point": str(suggested), "xyz_class": item["xyz_class"]})
        return {"updated": len(updated), "items": updated}
    def save_abc_xyz_analysis_snapshot(
        self,
        analysis_days: int = 90,
        warehouse_id: int | None = None,
        actor_id: str = "system",
        source: str = "manual",
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> dict[str, Any]:
        if source not in {"manual", "background"}:
            raise ValidationError("ABC/XYZ source must be manual or background")
        analysis = self.abc_xyz_analysis(analysis_days=analysis_days, warehouse_id=warehouse_id)
        generated_at = self._datetime_from_db(analysis["generated_at"])
        if period_end is None:
            period_end = generated_at
        if period_start is None:
            period_start = period_end - timedelta(days=analysis_days)
        if period_start >= period_end:
            raise ValidationError("ABC/XYZ period start must be before period end")
        with self.database.transaction() as connection:
            if warehouse_id is not None:
                self._require(connection, "warehouses", warehouse_id)
            existing = connection.execute(
                """
                SELECT id
                FROM abc_xyz_runs
                WHERE COALESCE(warehouse_id, 0) = COALESCE(?, 0)
                  AND analysis_days = ?
                  AND period_start = ?
                  AND period_end = ?
                  AND source = ?
                  AND status = 'succeeded'
                """,
                (warehouse_id, analysis_days, period_start.isoformat(), period_end.isoformat(), source),
            ).fetchone()
            if existing:
                return self._get_abc_xyz_run(connection, int(existing["id"]))
            run_id = insert_and_get_id(
                connection,
                """
                INSERT INTO abc_xyz_runs(
                  warehouse_id, analysis_days, period_start, period_end, source, status,
                  items_count, error, generated_by, generated_at
                ) VALUES (?, ?, ?, ?, ?, 'succeeded', ?, NULL, ?, ?)
                """,
                (
                    warehouse_id,
                    analysis_days,
                    period_start.isoformat(),
                    period_end.isoformat(),
                    source,
                    len(analysis["items"]),
                    actor_id,
                    generated_at.isoformat(),
                ),
            )
            for item in analysis["items"]:
                connection.execute(
                    """
                    INSERT INTO abc_xyz_run_items(
                      run_id, product_id, product_name, sku, abc_class, xyz_class,
                      consumption_quantity, consumption_value, current_free_quantity,
                      reorder_point, safety_stock, recommended_order_quantity,
                      recommendation, movement_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        item["product_id"],
                        item["product_name"],
                        item["sku"],
                        item["abc_class"],
                        item["xyz_class"],
                        decimal_to_db(item["consumption_quantity"]),
                        decimal_to_db(item["consumption_value"]),
                        decimal_to_db(item["current_free_quantity"]),
                        decimal_to_db(item["reorder_point"]),
                        decimal_to_db(item["safety_stock"]),
                        decimal_to_db(item["recommended_order_quantity"]),
                        item["recommendation"],
                        item["movement_count"],
                    ),
                )
            self._audit(
                connection,
                actor_id,
                AuditAction.CREATE,
                "abc_xyz_run",
                run_id,
                {
                    "warehouse_id": warehouse_id,
                    "analysis_days": analysis_days,
                    "source": source,
                    "items_count": len(analysis["items"]),
                },
                warehouse_id=warehouse_id,
            )
            return self._get_abc_xyz_run(connection, run_id)

    def save_monthly_abc_xyz_analysis_snapshot(
        self,
        *,
        warehouse_id: int | None = None,
        analysis_days: int = 90,
        actor_id: str = "system-scheduler",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        current = now or datetime.now(UTC)
        current = current.astimezone(UTC)
        period_start = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if period_start.month == 12:
            period_end = period_start.replace(year=period_start.year + 1, month=1)
        else:
            period_end = period_start.replace(month=period_start.month + 1)
        return self.save_abc_xyz_analysis_snapshot(
            analysis_days=analysis_days,
            warehouse_id=warehouse_id,
            actor_id=actor_id,
            source="background",
            period_start=period_start,
            period_end=period_end,
        )

    def list_abc_xyz_runs(
        self,
        warehouse_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = "SELECT * FROM abc_xyz_runs"
        params: tuple[Any, ...] = ()
        if warehouse_id is not None:
            query += " WHERE warehouse_id = ?"
            params = (warehouse_id,)
        query += " ORDER BY generated_at DESC, id DESC LIMIT ? OFFSET ?"
        connection = self.database.connect()
        try:
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_abc_xyz_runs(self, warehouse_id: int | None = None) -> int:
        query = "SELECT COUNT(*) AS total FROM abc_xyz_runs"
        params: tuple[Any, ...] = ()
        if warehouse_id is not None:
            query += " WHERE warehouse_id = ?"
            params = (warehouse_id,)
        connection = self.database.connect()
        try:
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def get_abc_xyz_run(self, run_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_abc_xyz_run(connection, run_id)
        finally:
            self._close_connection(connection)

    def _report_decimal(self, value: Decimal) -> str:
        normalized = value.normalize()
        if normalized == normalized.to_integral():
            return str(normalized.quantize(Decimal("1")))
        return format(normalized, "f")

    def _xyz_class(self, buckets: list[Decimal]) -> str:
        total = sum(buckets, Decimal("0"))
        if total <= 0:
            return "Z"
        mean = total / Decimal(len(buckets))
        if mean <= 0:
            return "Z"
        variance = sum((bucket - mean) ** 2 for bucket in buckets) / Decimal(len(buckets))
        coefficient = Decimal(str(math.sqrt(float(variance)))) / mean
        if coefficient <= Decimal("0.50"):
            return "X"
        if coefficient <= Decimal("1.00"):
            return "Y"
        return "Z"

    def _xyz_suggested_reorder_point(
        self, xyz_class: str, total_consumption: Decimal, analysis_days: int
    ) -> Decimal:
        """Suggest reorder point based on XYZ class: X=7d, Y=14d, Z=21d buffer."""
        if analysis_days <= 0 or total_consumption <= 0:
            return Decimal("0")
        daily = total_consumption / Decimal(str(analysis_days))
        buffer_days = {"X": 7, "Y": 14, "Z": 21}.get(xyz_class, 14)
        return (daily * Decimal(str(buffer_days))).quantize(Decimal("0.001"))

    def _abc_xyz_recommendation(
        self, abc_class: str, xyz_class: str, recommended_order: Decimal
    ) -> str:
        if recommended_order > 0:
            if abc_class == "A":
                return "Заказать в первую очередь"
            return "Пополнить запас"
        if abc_class == "A" and xyz_class == "Z":
            return "Проверить нестабильный спрос"
        if abc_class == "A":
            return "Держать под постоянным контролем"
        if xyz_class == "Z":
            return "Наблюдать за нерегулярным спросом"
        return "Запас достаточный"

    def create_purchase_request(
        self, data: PurchaseRequestCreate, actor_id: str = "system"
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            self._require(connection, "warehouses", data.warehouse_id)
            product = self._require(connection, "products", data.product_id)
            current_free = self._current_free_quantity(
                connection, data.product_id, data.warehouse_id
            )
            reorder_point = Decimal(product["reorder_point"])
            safety_stock = Decimal(product["safety_stock"])
            existing = connection.execute(
                """
                SELECT id FROM purchase_requests
                WHERE warehouse_id = ?
                  AND product_id = ?
                  AND status = 'draft'
                """,
                (data.warehouse_id, data.product_id),
            ).fetchone()
            if existing:
                connection.execute(
                    """
                    UPDATE purchase_requests
                    SET current_free_quantity = ?,
                        reorder_point = ?,
                        safety_stock = ?,
                        recommended_quantity = ?,
                        reason = ?,
                        source = ?,
                        created_by = ?
                    WHERE id = ?
                    """,
                    (
                        self._report_decimal(current_free),
                        self._report_decimal(reorder_point),
                        self._report_decimal(safety_stock),
                        self._report_decimal(data.quantity),
                        data.reason,
                        data.source,
                        actor_id,
                        existing["id"],
                    ),
                )
                request_id = existing["id"]
                action = AuditAction.UPDATE
            elif self._is_postgresql(connection):
                request_id = self._upsert_purchase_request_postgresql(
                    connection,
                    warehouse_id=data.warehouse_id,
                    product_id=data.product_id,
                    current_free=current_free,
                    reorder_point=reorder_point,
                    safety_stock=safety_stock,
                    recommended_quantity=data.quantity,
                    reason=data.reason,
                    source=data.source,
                    actor_id=actor_id,
                )
                action = AuditAction.CREATE
            else:
                request_id = insert_and_get_id(
                    connection,
                    """
                    INSERT INTO purchase_requests(
                      warehouse_id, product_id, status, current_free_quantity,
                      reorder_point, safety_stock, recommended_quantity,
                      reason, source, created_by, created_at
                    ) VALUES (?, ?, 'draft', ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        data.warehouse_id,
                        data.product_id,
                        self._report_decimal(current_free),
                        self._report_decimal(reorder_point),
                        self._report_decimal(safety_stock),
                        self._report_decimal(data.quantity),
                        data.reason,
                        data.source,
                        actor_id,
                        now_iso(),
                    ),
                )
                action = AuditAction.CREATE
            # Set gov-procurement fields (not in ON CONFLICT upsert above)
            condition_accepted = getattr(data, "condition_accepted", "any") or "any"
            is_gov = getattr(data, "is_gov_procurement", False) or False
            connection.execute(
                """UPDATE purchase_requests
                   SET condition_accepted = ?, is_gov_procurement = ?,
                       gov_status = CASE WHEN ? THEN COALESCE(gov_status, 'demand') ELSE gov_status END
                   WHERE id = ?""",
                (condition_accepted, is_gov, is_gov, request_id),
            )
            self._audit(
                connection,
                actor_id,
                action,
                "purchase_request",
                request_id,
                {
                    "warehouse_id": data.warehouse_id,
                    "product_id": data.product_id,
                    "recommended_quantity": data.quantity,
                    "reason": data.reason,
                    "source": data.source,
                    "condition_accepted": condition_accepted,
                    "is_gov_procurement": is_gov,
                },
                warehouse_id=data.warehouse_id,
            )
            return self._get_purchase_request(connection, request_id)

    def _upsert_purchase_request_postgresql(
        self,
        connection: Connection,
        *,
        warehouse_id: int,
        product_id: int,
        current_free: Decimal,
        reorder_point: Decimal,
        safety_stock: Decimal,
        recommended_quantity: Decimal,
        reason: str,
        source: str,
        actor_id: str,
    ) -> int:
        row = connection.execute(
            """
            INSERT INTO purchase_requests(
              warehouse_id, product_id, status, current_free_quantity,
              reorder_point, safety_stock, recommended_quantity,
              reason, source, created_by, created_at
            ) VALUES (?, ?, 'draft', ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (warehouse_id, product_id) WHERE status = 'draft'
            DO UPDATE SET
              current_free_quantity = EXCLUDED.current_free_quantity,
              reorder_point = EXCLUDED.reorder_point,
              safety_stock = EXCLUDED.safety_stock,
              recommended_quantity = EXCLUDED.recommended_quantity,
              reason = EXCLUDED.reason,
              source = EXCLUDED.source,
              created_by = EXCLUDED.created_by
            RETURNING id
            """,
            (
                warehouse_id,
                product_id,
                self._report_decimal(current_free),
                self._report_decimal(reorder_point),
                self._report_decimal(safety_stock),
                self._report_decimal(recommended_quantity),
                reason,
                source,
                actor_id,
                now_iso(),
            ),
        ).fetchone()
        if row is None:
            raise RuntimeError("PostgreSQL purchase request upsert did not return an id")
        return int(row["id"])

    def _insert_purchase_request_if_absent_postgresql(
        self,
        connection: Connection,
        *,
        warehouse_id: int,
        product_id: int,
        current_free: Decimal,
        reorder_point: Decimal,
        safety_stock: Decimal,
        recommended_quantity: Decimal,
        reason: str,
        actor_id: str,
    ) -> int | None:
        row = connection.execute(
            """
            INSERT INTO purchase_requests(
              warehouse_id, product_id, status, current_free_quantity,
              reorder_point, safety_stock, recommended_quantity,
              reason, source, created_by, created_at
            ) VALUES (?, ?, 'draft', ?, ?, ?, ?, ?, 'auto', ?, ?)
            ON CONFLICT (warehouse_id, product_id) WHERE status = 'draft'
            DO NOTHING
            RETURNING id
            """,
            (
                warehouse_id,
                product_id,
                self._report_decimal(current_free),
                self._report_decimal(reorder_point),
                self._report_decimal(safety_stock),
                self._report_decimal(recommended_quantity),
                reason,
                actor_id,
                now_iso(),
            ),
        ).fetchone()
        return None if row is None else int(row["id"])

    def generate_purchase_requests(
        self, warehouse_id: int, actor_id: str = "system"
    ) -> list[dict[str, Any]]:
        with self.database.transaction() as connection:
            self._require(connection, "warehouses", warehouse_id)
            rows = connection.execute(
                """
                SELECT
                  p.id AS product_id,
                  p.reorder_point,
                  p.safety_stock,
                  COALESCE(SUM(
                    CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL)
                  ), 0) AS free_quantity
                FROM products p
                LEFT JOIN batches b ON b.product_id = p.id
                LEFT JOIN stock_balances sb
                  ON sb.batch_id = b.id AND sb.warehouse_id = ?
                GROUP BY p.id
                HAVING CAST(p.reorder_point AS REAL) > 0
                   AND COALESCE(SUM(
                    CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL)
                  ), 0) < CAST(p.reorder_point AS REAL)
                ORDER BY p.name, p.id
                """,
                (warehouse_id,),
            ).fetchall()
            requests: list[dict[str, Any]] = []
            for row in rows:
                existing = connection.execute(
                    """
                    SELECT id FROM purchase_requests
                    WHERE warehouse_id = ?
                      AND product_id = ?
                      AND status = 'draft'
                    """,
                    (warehouse_id, row["product_id"]),
                ).fetchone()
                if existing:
                    requests.append(self._get_purchase_request(connection, existing["id"]))
                    continue

                current_free = Decimal(str(row["free_quantity"] or 0))
                reorder_point = Decimal(row["reorder_point"])
                safety_stock = Decimal(row["safety_stock"])
                recommended_quantity = max(
                    Decimal("0"),
                    reorder_point + safety_stock - current_free,
                )
                if self._is_postgresql(connection):
                    request_id = self._insert_purchase_request_if_absent_postgresql(
                        connection,
                        warehouse_id=warehouse_id,
                        product_id=row["product_id"],
                        current_free=current_free,
                        reorder_point=reorder_point,
                        safety_stock=safety_stock,
                        recommended_quantity=recommended_quantity,
                        reason="Ниже точки заказа",
                        actor_id=actor_id,
                    )
                    if request_id is None:
                        existing = connection.execute(
                            """
                            SELECT id FROM purchase_requests
                            WHERE warehouse_id = ?
                              AND product_id = ?
                              AND status = 'draft'
                            """,
                            (warehouse_id, row["product_id"]),
                        ).fetchone()
                        if existing is None:
                            raise RuntimeError("Draft purchase request conflict was not recoverable")
                        requests.append(self._get_purchase_request(connection, existing["id"]))
                        continue
                else:
                    request_id = insert_and_get_id(
                        connection,
                        """
                        INSERT INTO purchase_requests(
                          warehouse_id, product_id, status, current_free_quantity,
                          reorder_point, safety_stock, recommended_quantity,
                          reason, source, created_by, created_at
                        ) VALUES (?, ?, 'draft', ?, ?, ?, ?, ?, 'auto', ?, ?)
                        """,
                        (
                            warehouse_id,
                            row["product_id"],
                            self._report_decimal(current_free),
                            self._report_decimal(reorder_point),
                            self._report_decimal(safety_stock),
                            self._report_decimal(recommended_quantity),
                            "Ниже точки заказа",
                            actor_id,
                            now_iso(),
                        ),
                    )
                self._audit(
                    connection,
                    actor_id,
                    AuditAction.CREATE,
                    "purchase_request",
                    request_id,
                    {
                        "warehouse_id": warehouse_id,
                        "product_id": row["product_id"],
                        "recommended_quantity": recommended_quantity,
                    },
                    warehouse_id=warehouse_id,
                )
                requests.append(self._get_purchase_request(connection, request_id))
            return requests

    def list_purchase_requests(
        self,
        warehouse_id: int | None = None,
        status: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT
              pr.*,
              p.name AS product_name,
              p.sku
            FROM purchase_requests pr
            JOIN products p ON p.id = pr.product_id
        """
        params: tuple[Any, ...] = ()
        filters: list[str] = []
        if warehouse_id is not None:
            filters.append("pr.warehouse_id = ?")
            params = (*params, warehouse_id)
        if status is not None:
            filters.append("pr.status = ?")
            params = (*params, status)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY pr.created_at DESC, pr.id DESC LIMIT ? OFFSET ?"
        connection = self.database.connect()
        try:
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def get_purchase_request(self, request_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_purchase_request(connection, request_id)
        finally:
            self._close_connection(connection)

    def update_purchase_request_status(
        self,
        request_id: int,
        data: PurchaseRequestStatusUpdate,
        actor_id: str = "system",
    ) -> dict[str, Any]:
        if data.status not in {"ordered", "cancelled"}:
            raise ValidationError("Purchase request can only be ordered or cancelled")
        with self.database.transaction() as connection:
            before = self._get_purchase_request(connection, request_id)
            if before["status"] == data.status:
                return before
            if before["status"] != "draft":
                raise ValidationError("Only draft purchase requests can change status")
            connection.execute(
                "UPDATE purchase_requests SET status = ? WHERE id = ?",
                (data.status, request_id),
            )
            updated = self._get_purchase_request(connection, request_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "purchase_request",
                request_id,
                {"before": before, "after": updated},
                warehouse_id=updated["warehouse_id"],
            )
            if data.status == "ordered":
                self._fire_accounting_webhook(updated)
            return updated

    def list_batches(
        self,
        warehouse_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
        product_id: int | None = None,
        supplier_id: int | None = None,
        status: str | None = None,
        expires_before: date | None = None,
        expires_after: date | None = None,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = "SELECT DISTINCT b.* FROM batches b"
        filters: list[str] = []
        params: tuple[Any, ...] = ()
        if warehouse_id is not None:
            query += " JOIN stock_balances sb ON sb.batch_id = b.id"
            filters.append("sb.warehouse_id = ?")
            params = (*params, warehouse_id)
        if product_id is not None:
            filters.append("b.product_id = ?")
            params = (*params, product_id)
        if supplier_id is not None:
            filters.append("b.supplier_id = ?")
            params = (*params, supplier_id)
        if status is not None:
            filters.append("b.status = ?")
            params = (*params, status)
        if expires_before is not None:
            filters.append("b.expires_on IS NOT NULL AND b.expires_on <= ?")
            params = (*params, expires_before.isoformat())
        if expires_after is not None:
            filters.append("b.expires_on IS NOT NULL AND b.expires_on >= ?")
            params = (*params, expires_after.isoformat())
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY b.received_at DESC, b.id DESC LIMIT ? OFFSET ?"
        connection = self.database.connect()
        try:
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def list_stock_documents(
        self,
        warehouse_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
        document_type: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        connection = self.database.connect()
        try:
            query = "SELECT * FROM stock_documents"
            filters: list[str] = []
            params: tuple[Any, ...] = ()
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if document_type is not None:
                filters.append("document_type = ?")
                params = (*params, document_type)
            if status is not None:
                filters.append("status = ?")
                params = (*params, status)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            query += " ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?"
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_stock_documents(
        self,
        warehouse_id: int | None = None,
        document_type: str | None = None,
        status: str | None = None,
    ) -> int:
        connection = self.database.connect()
        try:
            query = "SELECT COUNT(*) AS total FROM stock_documents"
            filters: list[str] = []
            params: tuple[Any, ...] = ()
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if document_type is not None:
                filters.append("document_type = ?")
                params = (*params, document_type)
            if status is not None:
                filters.append("status = ?")
                params = (*params, status)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def list_reservations(
        self, warehouse_id: int | None = None, limit: int = 100, offset: int = 0
    ) -> list[dict[str, Any]]:
        return self._list_table(
            "reservations",
            "created_at DESC, id DESC",
            limit,
            offset,
            where="warehouse_id = ?",
            params=(warehouse_id,),
        ) if warehouse_id is not None else self._list_table(
            "reservations", "created_at DESC, id DESC", limit, offset
        )

    def get_batch(self, batch_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_batch(connection, batch_id)
        finally:
            self._close_connection(connection)

    def get_batch_detail(
        self, batch_id: int, movement_limit: int = 100, movement_offset: int = 0
    ) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            batch = self._get_batch(connection, batch_id)
            balances = self._batch_balances(connection, batch_id)
            movements = self._batch_movements(
                connection, batch_id, movement_limit, movement_offset
            )
            return {"batch": batch, "balances": balances, "movements": movements}
        finally:
            self._close_connection(connection)

    def get_batch_traceability(
        self, batch_id: int, movement_limit: int = 100, movement_offset: int = 0
    ) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            batch = self._get_batch(connection, batch_id)
            balances = self._batch_balances(connection, batch_id)
            movements = self._batch_movements(
                connection, batch_id, movement_limit, movement_offset
            )
            document_rows = connection.execute(
                """
                SELECT DISTINCT sd.id
                FROM stock_documents sd
                JOIN stock_document_lines sdl ON sdl.document_id = sd.id
                WHERE sdl.batch_id = ?
                ORDER BY sd.created_at DESC, sd.id DESC
                """,
                (batch_id,),
            ).fetchall()
            documents = [self._get_document(connection, int(row["id"])) for row in document_rows]
            return {
                "batch": batch,
                "balances": balances,
                "movements": movements,
                "documents": documents,
                "transformations": self._batch_transformations(connection, batch_id=batch_id),
                "recalls": self._batch_recalls(connection, batch_id=batch_id),
            }
        finally:
            self._close_connection(connection)

    def list_batch_transformations(
        self,
        warehouse_id: int | None = None,
        batch_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        connection = self.database.connect()
        try:
            return self._batch_transformations(
                connection,
                warehouse_id=warehouse_id,
                batch_id=batch_id,
                limit=safe_limit,
                offset=safe_offset,
            )
        finally:
            self._close_connection(connection)

    def count_batch_transformations(
        self,
        warehouse_id: int | None = None,
        batch_id: int | None = None,
    ) -> int:
        connection = self.database.connect()
        try:
            query = "SELECT COUNT(*) AS total FROM batch_transformations"
            filters: list[str] = []
            params: tuple[Any, ...] = ()
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if batch_id is not None:
                filters.append("(source_batch_id = ? OR target_batch_id = ?)")
                params = (*params, batch_id, batch_id)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def get_batch_warehouse_ids(self, batch_id: int) -> list[int]:
        connection = self.database.connect()
        try:
            self._require(connection, "batches", batch_id)
            return self._batch_warehouse_ids(connection, batch_id)
        finally:
            self._close_connection(connection)

    def get_stock_document(self, document_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_document(connection, document_id)
        finally:
            self._close_connection(connection)

    def get_repack_print_form(self, document_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            document = self._get_document(connection, document_id)
            if document["document_type"] != StockDocumentType.REPACK:
                raise ValidationError("Print form is available only for repack documents")
            warehouse = dict(self._require(connection, "warehouses", document["warehouse_id"]))
            transformation_rows = {
                int(row["source_batch_id"]): dict(row)
                for row in connection.execute(
                    """
                    SELECT * FROM batch_transformations
                    WHERE document_id = ?
                    ORDER BY id
                    """,
                    (document_id,),
                ).fetchall()
            }
            rows = connection.execute(
                """
                SELECT
                  sdl.id,
                  sdl.batch_id AS source_batch_id,
                  sdl.target_product_id,
                  sdl.quantity AS source_quantity,
                  sdl.target_quantity,
                  sdl.conversion_factor,
                  sdl.loss_quantity,
                  sdl.target_unit_price,
                  sdl.target_lot,
                  sdl.reason,
                  sb.lot AS source_lot,
                  sp.name AS source_product_name,
                  tp.name AS target_product_name
                FROM stock_document_lines sdl
                JOIN batches sb ON sb.id = sdl.batch_id
                JOIN products sp ON sp.id = sb.product_id
                JOIN products tp ON tp.id = sdl.target_product_id
                WHERE sdl.document_id = ?
                ORDER BY sdl.id
                """,
                (document_id,),
            ).fetchall()
            lines = []
            for index, row in enumerate(rows, start=1):
                item = dict(row)
                transformation = transformation_rows.get(int(item["source_batch_id"]))
                target_batch_id = transformation["target_batch_id"] if transformation else None
                lines.append(
                    {
                        "line_no": index,
                        "source_batch_id": item["source_batch_id"],
                        "source_product_name": item["source_product_name"],
                        "source_lot": item["source_lot"],
                        "target_batch_id": target_batch_id,
                        "target_product_name": item["target_product_name"],
                        "target_lot": item["target_lot"],
                        "source_quantity": item["source_quantity"],
                        "target_quantity": item["target_quantity"],
                        "conversion_factor": item["conversion_factor"],
                        "loss_quantity": item["loss_quantity"],
                        "target_unit_price": item["target_unit_price"],
                        "reason": item["reason"],
                    }
                )
            return {
                "document_id": document_id,
                "status": document["status"],
                "warehouse_id": document["warehouse_id"],
                "warehouse_name": warehouse["name"],
                "created_by": document["created_by"],
                "created_at": document["created_at"],
                "posted_at": document["posted_at"],
                "csv": self._repack_print_csv(lines),
                "lines": lines,
            }
        finally:
            self._close_connection(connection)

    def get_transfer_print_form(self, document_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            document = self._get_document(connection, document_id)
            if document["document_type"] != StockDocumentType.TRANSFER:
                raise ValidationError("Print form is available only for transfer documents")
            source_warehouse = dict(self._require(connection, "warehouses", document["warehouse_id"]))
            rows = connection.execute(
                """
                SELECT
                  sdl.id,
                  sdl.batch_id,
                  sdl.target_warehouse_id,
                  sdl.quantity,
                  sdl.reason,
                  b.lot,
                  p.name AS product_name,
                  source.name AS source_warehouse_name,
                  target.name AS target_warehouse_name
                FROM stock_document_lines sdl
                JOIN batches b ON b.id = sdl.batch_id
                JOIN products p ON p.id = b.product_id
                JOIN warehouses source ON source.id = ?
                JOIN warehouses target ON target.id = sdl.target_warehouse_id
                WHERE sdl.document_id = ?
                ORDER BY sdl.id
                """,
                (document["warehouse_id"], document_id),
            ).fetchall()
            lines = []
            for index, row in enumerate(rows, start=1):
                item = dict(row)
                lines.append(
                    {
                        "line_no": index,
                        "batch_id": item["batch_id"],
                        "product_name": item["product_name"],
                        "lot": item["lot"],
                        "source_warehouse_id": document["warehouse_id"],
                        "source_warehouse_name": item["source_warehouse_name"],
                        "target_warehouse_id": item["target_warehouse_id"],
                        "target_warehouse_name": item["target_warehouse_name"],
                        "quantity": item["quantity"],
                        "reason": item["reason"],
                    }
                )
            return {
                "document_id": document_id,
                "status": document["status"],
                "source_warehouse_id": document["warehouse_id"],
                "source_warehouse_name": source_warehouse["name"],
                "created_by": document["created_by"],
                "created_at": document["created_at"],
                "approved_by": document["approved_by"],
                "approved_at": document["approved_at"],
                "posted_at": document["posted_at"],
                "csv": self._transfer_print_csv(lines),
                "lines": lines,
            }
        finally:
            self._close_connection(connection)

    def get_reservation(self, reservation_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_by_id(connection, "reservations", reservation_id)
        finally:
            self._close_connection(connection)

    def list_controlled_substance_ledger(
        self,
        warehouse_id: int | None = None,
        product_id: int | None = None,
        batch_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT
              sm.id AS movement_id,
              sm.movement_type,
              p.id AS product_id,
              p.name AS product_name,
              p.sku,
              b.id AS batch_id,
              b.lot,
              sm.warehouse_id,
              sm.quantity,
              sm.reason,
              sm.patient_id,
              sm.doctor_id,
              sm.medical_record_no,
              sm.second_approver_id,
              sm.second_approval_note,
              sm.created_at
            FROM stock_movements sm
            JOIN batches b ON b.id = sm.batch_id
            JOIN products p ON p.id = b.product_id
            WHERE p.is_controlled = ?
        """
        params: tuple[Any, ...] = (True,)
        if warehouse_id is not None:
            query += " AND sm.warehouse_id = ?"
            params = (*params, warehouse_id)
        if product_id is not None:
            query += " AND p.id = ?"
            params = (*params, product_id)
        if batch_id is not None:
            query += " AND b.id = ?"
            params = (*params, batch_id)
        query += " ORDER BY sm.created_at DESC, sm.id DESC LIMIT ? OFFSET ?"
        params = (*params, safe_limit, safe_offset)
        connection = self.database.connect()
        try:
            rows = connection.execute(query, params).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_controlled_substance_ledger(
        self,
        warehouse_id: int | None = None,
        product_id: int | None = None,
        batch_id: int | None = None,
    ) -> int:
        query = """
            SELECT COUNT(*) AS total
            FROM stock_movements sm
            JOIN batches b ON b.id = sm.batch_id
            JOIN products p ON p.id = b.product_id
            WHERE p.is_controlled = ?
        """
        params: tuple[Any, ...] = (True,)
        if warehouse_id is not None:
            query += " AND sm.warehouse_id = ?"
            params = (*params, warehouse_id)
        if product_id is not None:
            query += " AND p.id = ?"
            params = (*params, product_id)
        if batch_id is not None:
            query += " AND b.id = ?"
            params = (*params, batch_id)
        connection = self.database.connect()
        try:
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def export_controlled_substance_ledger(
        self,
        warehouse_id: int | None = None,
        product_id: int | None = None,
        batch_id: int | None = None,
    ) -> dict[str, Any]:
        rows = self.list_controlled_substance_ledger(
            warehouse_id=warehouse_id,
            product_id=product_id,
            batch_id=batch_id,
            limit=500,
            offset=0,
        )
        columns = [
            "Дата",
            "Движение",
            "Товар",
            "SKU",
            "Партия",
            "Склад",
            "Количество",
            "Причина",
            "Пациент",
            "Врач",
            "История болезни",
            "Второе подтверждение",
        ]
        csv_rows: list[list[Any]] = [columns]
        for row in rows:
            csv_rows.append(
                [
                    row["created_at"],
                    row["movement_type"],
                    row["product_name"],
                    row["sku"],
                    row["lot"],
                    row["warehouse_id"],
                    self._report_decimal(Decimal(str(row["quantity"]))),
                    row["reason"] or "",
                    row["patient_id"] or "",
                    row["doctor_id"] or "",
                    row["medical_record_no"] or "",
                    row["second_approver_id"] or "",
                ]
            )
        return {
            "filename": "sklad-controlled-substances-ledger.csv",
            "csv": "\n".join(";".join(self._csv_cell(cell) for cell in csv_row) for csv_row in csv_rows),
        }

    def generate_low_stock_notifications(
        self, warehouse_id: int | None = None
    ) -> list[dict[str, Any]]:
        with self.database.transaction() as connection:
            if warehouse_id is not None:
                self._require(connection, "warehouses", warehouse_id)
            params: tuple[Any, ...] = ()
            warehouse_filter = ""
            if warehouse_id is not None:
                warehouse_filter = " WHERE w.id = ?"
                params = (warehouse_id,)
            rows = connection.execute(
                f"""
                SELECT
                  p.id AS product_id,
                  p.name AS product_name,
                  p.reorder_point,
                  w.id AS warehouse_id,
                  COALESCE(SUM(
                    CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL)
                  ), 0) AS free_quantity
                FROM products p
                CROSS JOIN warehouses w
                LEFT JOIN batches b ON b.product_id = p.id
                LEFT JOIN stock_balances sb ON sb.batch_id = b.id AND sb.warehouse_id = w.id
                {warehouse_filter}
                GROUP BY p.id, p.name, p.reorder_point, w.id
                HAVING CAST(p.reorder_point AS REAL) > 0
                   AND COALESCE(SUM(
                    CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL)
                  ), 0) < CAST(p.reorder_point AS REAL)
                ORDER BY p.name, w.id
                """,
                params,
            ).fetchall()
            notifications: list[dict[str, Any]] = []
            for row in rows:
                existing = connection.execute(
                    """
                    SELECT id FROM notifications
                    WHERE notification_type = 'low_stock'
                      AND product_id = ?
                      AND warehouse_id = ?
                      AND is_read = 0
                    """,
                    (row["product_id"], row["warehouse_id"]),
                ).fetchone()
                if existing:
                    notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                    continue
                title = f"Низкий остаток: {row['product_name']}"
                message = (
                    f"Свободный остаток {Decimal(str(row['free_quantity']))} "
                    f"ниже точки заказа {Decimal(row['reorder_point'])}."
                )
                if self._is_postgresql(connection):
                    notification_id = self._insert_low_stock_notification_if_absent_postgresql(
                        connection,
                        product_id=row["product_id"],
                        warehouse_id=row["warehouse_id"],
                        title=title,
                        message=message,
                    )
                    if notification_id is None:
                        existing = connection.execute(
                            """
                            SELECT id FROM notifications
                            WHERE notification_type = 'low_stock'
                              AND product_id = ?
                              AND warehouse_id = ?
                              AND is_read = 0
                            """,
                            (row["product_id"], row["warehouse_id"]),
                        ).fetchone()
                        if existing is None:
                            raise RuntimeError("Low-stock notification conflict was not recoverable")
                        notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                        continue
                else:
                    notification_id = insert_and_get_id(
                        connection,
                        """
                        INSERT INTO notifications(
                          notification_type, product_id, warehouse_id, title, message, created_at
                        ) VALUES ('low_stock', ?, ?, ?, ?, ?)
                        """,
                        (row["product_id"], row["warehouse_id"], title, message, now_iso()),
                    )
                notifications.append(self._get_by_id(connection, "notifications", notification_id))
            return notifications

    def _insert_low_stock_notification_if_absent_postgresql(
        self,
        connection: Connection,
        *,
        product_id: int,
        warehouse_id: int,
        title: str,
        message: str,
    ) -> int | None:
        row = connection.execute(
            """
            INSERT INTO notifications(
              notification_type, product_id, warehouse_id, title, message, created_at
            ) VALUES ('low_stock', ?, ?, ?, ?, ?)
            ON CONFLICT (warehouse_id, product_id)
              WHERE notification_type = 'low_stock' AND is_read = FALSE
            DO NOTHING
            RETURNING id
            """,
            (product_id, warehouse_id, title, message, now_iso()),
        ).fetchone()
        return None if row is None else int(row["id"])

    def _insert_expiry_notification_if_absent_postgresql(
        self,
        connection: Connection,
        *,
        product_id: int,
        batch_id: int,
        warehouse_id: int,
        title: str,
        message: str,
    ) -> int | None:
        row = connection.execute(
            """
            INSERT INTO notifications(
              notification_type, product_id, batch_id, warehouse_id, title, message, created_at
            ) VALUES ('expiry', ?, ?, ?, ?, ?, ?)
            ON CONFLICT (warehouse_id, batch_id)
              WHERE notification_type = 'expiry' AND is_read = FALSE
            DO NOTHING
            RETURNING id
            """,
            (product_id, batch_id, warehouse_id, title, message, now_iso()),
        ).fetchone()
        return None if row is None else int(row["id"])

    def generate_expiry_notifications(
        self, days: int = 30, warehouse_id: int | None = None
    ) -> list[dict[str, Any]]:
        if days < 0:
            raise ValidationError("Expiry reminder window cannot be negative")
        today = datetime.now(UTC).date()
        cutoff = today + timedelta(days=days)
        with self.database.transaction() as connection:
            if warehouse_id is not None:
                self._require(connection, "warehouses", warehouse_id)
            self._ensure_quarantine_reviews_for_open_batches(connection, warehouse_id=warehouse_id)
            params: tuple[Any, ...] = (cutoff.isoformat(),)
            warehouse_filter = ""
            if warehouse_id is not None:
                warehouse_filter = " AND sb.warehouse_id = ?"
                params = (*params, warehouse_id)
            rows = connection.execute(
                f"""
                SELECT
                  b.id AS batch_id,
                  b.product_id,
                  b.lot,
                  b.expires_on,
                  p.name AS product_name,
                  sb.warehouse_id,
                  sb.quantity,
                  sb.reserved_quantity
                FROM stock_balances sb
                JOIN batches b ON b.id = sb.batch_id
                JOIN products p ON p.id = b.product_id
                WHERE b.expires_on IS NOT NULL
                  AND b.expires_on <= ?
                  AND CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL) > 0
                  {warehouse_filter}
                ORDER BY b.expires_on, b.id, sb.warehouse_id
                """,
                params,
            ).fetchall()
            notifications: list[dict[str, Any]] = []
            for row in rows:
                existing = connection.execute(
                    """
                    SELECT id FROM notifications
                    WHERE notification_type = 'expiry'
                      AND batch_id = ?
                      AND warehouse_id = ?
                      AND is_read = 0
                    """,
                    (row["batch_id"], row["warehouse_id"]),
                ).fetchone()
                if existing:
                    notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                    continue
                days_left = (self._date_from_db(row["expires_on"]) - today).days
                if days_left < 0:
                    title = f"Просрочен срок: {row['product_name']}"
                    message = (
                        f"Партия #{row['batch_id']} серия {row['lot']} годна до {row['expires_on']}. "
                        f"Просрочено дней: {abs(days_left)}."
                    )
                else:
                    title = f"Скоро истекает срок: {row['product_name']}"
                    message = (
                        f"Партия #{row['batch_id']} серия {row['lot']} годна до {row['expires_on']}. "
                        f"Осталось дней: {days_left}."
                    )
                if self._is_postgresql(connection):
                    notification_id = self._insert_expiry_notification_if_absent_postgresql(
                        connection,
                        product_id=row["product_id"],
                        batch_id=row["batch_id"],
                        warehouse_id=row["warehouse_id"],
                        title=title,
                        message=message,
                    )
                    if notification_id is None:
                        existing = connection.execute(
                            """
                            SELECT id FROM notifications
                            WHERE notification_type = 'expiry'
                              AND batch_id = ?
                              AND warehouse_id = ?
                              AND is_read = 0
                            """,
                            (row["batch_id"], row["warehouse_id"]),
                        ).fetchone()
                        if existing is None:
                            raise RuntimeError("Expiry notification conflict was not recoverable")
                        notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                        continue
                else:
                    notification_id = insert_and_get_id(
                        connection,
                        """
                        INSERT INTO notifications(
                          notification_type, product_id, batch_id, warehouse_id, title, message, created_at
                        ) VALUES ('expiry', ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            row["product_id"],
                            row["batch_id"],
                            row["warehouse_id"],
                            title,
                            message,
                            now_iso(),
                        ),
                    )
                notifications.append(self._get_by_id(connection, "notifications", notification_id))
            return notifications



    def list_controlled_limits(self, warehouse_id):
        connection = self.database.connect()
        try:
            rows = connection.execute(
                "SELECT cl.*, p.name AS product_name, p.sku FROM controlled_substance_limits cl JOIN products p ON p.id = cl.product_id WHERE cl.warehouse_id = ? ORDER BY p.name",
                (warehouse_id,),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def upsert_controlled_limit(self, warehouse_id, product_id, max_quantity, unit=None):
        with self.database.transaction() as connection:
            self._require(connection, "warehouses", warehouse_id)
            self._require(connection, "products", product_id)
            existing = connection.execute(
                "SELECT id FROM controlled_substance_limits WHERE warehouse_id = ? AND product_id = ?",
                (warehouse_id, product_id),
            ).fetchone()
            if existing:
                connection.execute(
                    "UPDATE controlled_substance_limits SET max_quantity = ?, unit = ?, updated_at = ? WHERE id = ?",
                    (decimal_to_db(Decimal(str(max_quantity))), unit, now_iso(), existing["id"]),
                )
                return self._get_by_id(connection, "controlled_substance_limits", existing["id"])
            else:
                new_id = insert_and_get_id(
                    connection,
                    "INSERT INTO controlled_substance_limits(warehouse_id, product_id, max_quantity, unit, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (warehouse_id, product_id, decimal_to_db(Decimal(str(max_quantity))), unit, now_iso(), now_iso()),
                )
                return self._get_by_id(connection, "controlled_substance_limits", new_id)

    def delete_controlled_limit(self, limit_id):
        with self.database.transaction() as connection:
            self._require(connection, "controlled_substance_limits", limit_id)
            connection.execute("DELETE FROM controlled_substance_limits WHERE id = ?", (limit_id,))

    def check_controlled_limit_violations(self, warehouse_id):
        connection = self.database.connect()
        try:
            rows = connection.execute(
                """
                SELECT cl.product_id, cl.max_quantity, cl.unit, p.name AS product_name,
                       COALESCE(SUM(CAST(sb.quantity AS REAL)), 0) AS current_quantity
                FROM controlled_substance_limits cl
                JOIN products p ON p.id = cl.product_id
                LEFT JOIN batches b ON b.product_id = cl.product_id
                LEFT JOIN stock_balances sb ON sb.batch_id = b.id AND sb.warehouse_id = cl.warehouse_id
                WHERE cl.warehouse_id = ?
                GROUP BY cl.product_id, cl.max_quantity, cl.unit, p.name
                HAVING COALESCE(SUM(CAST(sb.quantity AS REAL)), 0) > CAST(cl.max_quantity AS REAL)
                """,
                (warehouse_id,),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)
    def generate_controlled_inventory_reminder(
        self, warehouse_id=None
    ):
        """Create monthly ПКУ inventory reminder notifications."""
        with self.database.transaction() as connection:
            params = ()
            wf = ""
            if warehouse_id is not None:
                self._require(connection, "warehouses", warehouse_id)
                wf = " AND sb.warehouse_id = ?"
                params = (warehouse_id,)
            rows = connection.execute(
                f"""
                SELECT DISTINCT p.id AS product_id, p.name AS product_name, sb.warehouse_id
                FROM products p
                JOIN batches b ON b.product_id = p.id
                JOIN stock_balances sb ON sb.batch_id = b.id
                WHERE p.is_controlled = 1
                  AND CAST(sb.quantity AS REAL) > 0
                  {wf}
                ORDER BY p.name, sb.warehouse_id
                """,
                params,
            ).fetchall()
            notif_type = "low_stock"
            notifications = []
            for row in rows:
                existing = connection.execute(
                    "SELECT id FROM notifications WHERE notification_type = ? AND product_id = ? AND warehouse_id = ? AND title LIKE ? AND is_read = 0",
                    (notif_type, row["product_id"], row["warehouse_id"], "% ПКУ %"),
                ).fetchone()
                if existing:
                    notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                    continue
                notif_id = insert_and_get_id(
                    connection,
                    "INSERT INTO notifications(notification_type, warehouse_id, product_id, title, message, is_read, created_at) VALUES (?, ?, ?, ?, ?, 0, ?)",
                    (notif_type, row["warehouse_id"], row["product_id"],
                     f"Плановая ПКУ инвентаризация: {row[product_name]}",
                     f"Требуется провести ежемесячную инвентаризацию ПКУ по товару {row[product_name]}.",
                     now_iso()),
                )
                notifications.append(self._get_by_id(connection, "notifications", notif_id))
            return notifications
    def generate_quarantine_notifications(
        self, days: int = 3, warehouse_id: int | None = None
    ) -> list[dict[str, Any]]:
        if days < 0:
            raise ValidationError("Quarantine reminder window cannot be negative")
        cutoff = datetime.now(UTC) - timedelta(days=days)
        with self.database.transaction() as connection:
            if warehouse_id is not None:
                self._require(connection, "warehouses", warehouse_id)
            params: tuple[Any, ...] = (cutoff.isoformat(),)
            warehouse_filter = ""
            if warehouse_id is not None:
                warehouse_filter = " AND sb.warehouse_id = ?"
                params = (*params, warehouse_id)
            rows = connection.execute(
                f"""
                SELECT
                  b.id AS batch_id,
                  b.product_id,
                  b.lot,
                  b.received_at,
                  p.name AS product_name,
                  sb.warehouse_id,
                  sb.quantity,
                  sb.reserved_quantity
                FROM stock_balances sb
                JOIN batches b ON b.id = sb.batch_id
                JOIN products p ON p.id = b.product_id
                WHERE b.status = 'quarantine'
                  AND b.received_at <= ?
                  AND CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL) > 0
                  {warehouse_filter}
                ORDER BY b.received_at, b.id, sb.warehouse_id
                """,
                params,
            ).fetchall()
            notifications: list[dict[str, Any]] = []
            for row in rows:
                existing = connection.execute(
                    """
                    SELECT id FROM notifications
                    WHERE notification_type = 'quarantine'
                      AND batch_id = ?
                      AND warehouse_id = ?
                      AND is_read = 0
                    """,
                    (row["batch_id"], row["warehouse_id"]),
                ).fetchone()
                if existing:
                    notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                    continue
                received_at = self._datetime_from_db(row["received_at"])
                age_days = max(0, (datetime.now(UTC) - received_at).days)
                title = f"Партия в карантине: {row['product_name']}"
                message = (
                    f"Партия #{row['batch_id']} серия {row['lot']} находится в карантине "
                    f"{age_days} дн. Проверьте документы и статус партии."
                )
                notification_id = insert_and_get_id(
                    connection,
                    """
                    INSERT INTO notifications(
                      notification_type, product_id, batch_id, warehouse_id, title, message, created_at
                    ) VALUES ('quarantine', ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row["product_id"],
                        row["batch_id"],
                        row["warehouse_id"],
                        title,
                        message,
                        now_iso(),
                    ),
                )
                notifications.append(self._get_by_id(connection, "notifications", notification_id))
            return notifications

    def generate_quarantine_review_overdue_notifications(
        self, days: int = 7
    ) -> list[dict[str, Any]]:
        """Notify when a quarantine review has been stuck in in_review for more than `days` days."""
        if days < 1:
            raise ValidationError("Overdue days must be at least 1")
        cutoff = (datetime.now(UTC) - timedelta(days=days)).isoformat()
        with self.database.transaction() as connection:
            rows = connection.execute(
                """
                SELECT
                  qr.id AS review_id,
                  qr.batch_id,
                  p.name AS product_name,
                  qr.responsible_id,
                  qr.updated_at AS started_at,
                  b.lot,
                  qr.warehouse_id
                FROM quarantine_reviews qr
                JOIN batches b ON b.id = qr.batch_id
                JOIN products p ON p.id = b.product_id
                WHERE qr.status = 'in_review'
                  AND qr.updated_at <= ?
                ORDER BY qr.updated_at, qr.id
                """,
                (cutoff,),
            ).fetchall()
            notifications: list[dict[str, Any]] = []
            for row in rows:
                existing = connection.execute(
                    """
                    SELECT id FROM notifications
                    WHERE notification_type = 'quarantine'
                      AND batch_id = ?
                      AND is_read = 0
                      AND title LIKE '%проверка%просрочена%'
                    """,
                    (row["batch_id"],),
                ).fetchone()
                if existing:
                    notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                    continue
                started = self._datetime_from_db(row["started_at"])
                age = max(0, (datetime.now(UTC) - started).days)
                title = f"Карантинная проверка просрочена: {row['product_name']}"
                message = (
                    f"Проверка #{row['review_id']} по партии {row['lot']} находится в статусе"
                    f" «На проверке» уже {age} дн. Ответственный: {row['responsible_id'] or '—'}."
                )
                wh = row["warehouse_id"] or 0
                notification_id = insert_and_get_id(
                    connection,
                    """
                    INSERT INTO notifications(
                      notification_type, batch_id, warehouse_id, title, message, created_at
                    ) VALUES ('quarantine', ?, ?, ?, ?, ?)
                    """,
                    (row["batch_id"], wh, title, message, now_iso()),
                )
                notifications.append(self._get_by_id(connection, "notifications", notification_id))
            return notifications


    def generate_supplier_contract_expiry_notifications(
        self, days: int = 30
    ) -> "list[dict[str, Any]]":
        """Notify when a supplier contract expires within the next `days` days."""
        if days < 0:
            raise ValidationError("Expiry window cannot be negative")
        today = datetime.now(UTC).date()
        cutoff = (today + timedelta(days=days)).isoformat()
        today_str = today.isoformat()
        with self.database.transaction() as connection:
            rows = connection.execute(
                """
                SELECT id, name, contract_expires_on
                FROM suppliers
                WHERE contract_expires_on IS NOT NULL
                  AND contract_expires_on >= ?
                  AND contract_expires_on <= ?
                ORDER BY contract_expires_on, id
                """,
                (today_str, cutoff),
            ).fetchall()
            notifications: list[dict[str, Any]] = []
            for row in rows:
                existing = connection.execute(
                    """
                    SELECT id FROM notifications
                    WHERE notification_type = 'supplier_contract_expiry'
                      AND title LIKE ?
                      AND is_read = 0
                    """,
                    (f"%{row['name']}%",),
                ).fetchone()
                if existing:
                    notifications.append(self._get_by_id(connection, "notifications", existing["id"]))
                    continue
                expires = row["contract_expires_on"]
                try:
                    from datetime import date as _date
                    exp_date = _date.fromisoformat(str(expires))
                    days_left = max(0, (exp_date - today).days)
                except Exception:
                    days_left = days
                title = f"Истекает договор поставщика: {row['name']}"
                message = (
                    f"Договор с поставщиком «{row['name']}» истекает {expires} "
                    f"(через {days_left} дн.). Свяжитесь с поставщиком для продления."
                )
                notification_id = insert_and_get_id(
                    connection,
                    """INSERT INTO notifications(
                      notification_type, title, message, created_at
                    ) VALUES ('supplier_contract_expiry', ?, ?, ?)""",
                    (title, message, now_iso()),
                )
                notifications.append(self._get_by_id(connection, "notifications", notification_id))
            return notifications

    def _ensure_sensor_warning_notification(
        self,
        connection: Connection,
        *,
        device: dict[str, Any],
        reading: dict[str, Any],
    ) -> dict[str, Any]:
        title = f"Нарушены условия хранения: {device['name']}"
        details = self._sensor_warning_details(device, reading)
        warehouse_name = reading.get("warehouse_name") or f"склад #{reading['warehouse_id']}"
        message = (
            f"{warehouse_name}. {'; '.join(details)}. "
            f"Время показания: {reading['recorded_at']}. Проверьте помещение, питание оборудования "
            "и перенесите чувствительные партии при необходимости."
        )
        if self._is_postgresql(connection):
            notification_id = self._upsert_sensor_warning_notification_postgresql(
                connection,
                device_id=reading["device_id"],
                sensor_reading_id=reading["id"],
                warehouse_id=reading["warehouse_id"],
                title=title,
                message=message,
            )
            return self._get_by_id(connection, "notifications", notification_id)

        existing = connection.execute(
            """
            SELECT id FROM notifications
            WHERE notification_type = 'sensor_warning'
              AND device_id = ?
              AND is_read = 0
            """,
            (reading["device_id"],),
        ).fetchone()
        if existing:
            connection.execute(
                """
                UPDATE notifications
                SET sensor_reading_id = ?,
                    warehouse_id = ?,
                    title = ?,
                    message = ?,
                    created_at = ?
                WHERE id = ?
                """,
                (
                    reading["id"],
                    reading["warehouse_id"],
                    title,
                    message,
                    now_iso(),
                    existing["id"],
                ),
            )
            return self._get_by_id(connection, "notifications", existing["id"])

        notification_id = insert_and_get_id(
            connection,
            """
            INSERT INTO notifications(
              notification_type, device_id, sensor_reading_id, warehouse_id,
              title, message, created_at
            ) VALUES ('sensor_warning', ?, ?, ?, ?, ?, ?)
            """,
            (
                reading["device_id"],
                reading["id"],
                reading["warehouse_id"],
                title,
                message,
                now_iso(),
            ),
        )
        return self._get_by_id(connection, "notifications", notification_id)

    def _upsert_sensor_warning_notification_postgresql(
        self,
        connection: Connection,
        *,
        device_id: int,
        sensor_reading_id: int,
        warehouse_id: int,
        title: str,
        message: str,
    ) -> int:
        row = connection.execute(
            """
            INSERT INTO notifications(
              notification_type, device_id, sensor_reading_id, warehouse_id,
              title, message, created_at
            ) VALUES ('sensor_warning', ?, ?, ?, ?, ?, ?)
            ON CONFLICT (device_id)
              WHERE notification_type = 'sensor_warning' AND is_read = FALSE
            DO UPDATE SET
              sensor_reading_id = EXCLUDED.sensor_reading_id,
              warehouse_id = EXCLUDED.warehouse_id,
              title = EXCLUDED.title,
              message = EXCLUDED.message,
              created_at = EXCLUDED.created_at
            RETURNING id
            """,
            (device_id, sensor_reading_id, warehouse_id, title, message, now_iso()),
        ).fetchone()
        if row is None:
            raise RuntimeError("Sensor warning notification conflict was not recoverable")
        return int(row["id"])

    def get_stats_summary(self) -> "dict[str, Any]":
        connection = self.database.connect()
        try:
            def scalar(sql: str, default: int = 0) -> int:
                try:
                    row = connection.execute(sql).fetchone()
                except Exception:
                    return default
                if row is None:
                    return default
                row_dict = dict(row) if hasattr(row, "keys") else {}
                val = list(row_dict.values())[0] if row_dict else (row[0] if row else default)
                try:
                    return int(float(val or 0))
                except (TypeError, ValueError):
                    return default

            return {
                "products": scalar("SELECT COUNT(*) FROM products WHERE is_active = 1"),
                "batches": scalar("SELECT COUNT(*) FROM batches"),
                "batches_available": scalar("SELECT COUNT(*) FROM batches WHERE status = 'available'"),
                "batches_quarantine": scalar("SELECT COUNT(*) FROM batches WHERE status = 'quarantine'"),
                "warehouses": scalar("SELECT COUNT(*) FROM warehouses"),
                "total_free_quantity": scalar("SELECT COALESCE(SUM(CAST(quantity AS REAL) - CAST(reserved_quantity AS REAL)), 0) FROM stock_balances"),
                "unread_notifications": scalar("SELECT COUNT(*) FROM notifications WHERE is_read = 0"),
                "pending_writeoffs": scalar("SELECT COUNT(*) FROM pending_controlled_writeoffs WHERE status = 'pending'"),
                "active_inventory_sessions": scalar("SELECT COUNT(*) FROM inventory_sessions WHERE status = 'in_progress'"),
            }
        finally:
            self._close_connection(connection)

    def create_grafana_alert_notification(
        self,
        title: str,
        message: str,
        severity: str = "warning",
    ) -> "dict[str, Any]":
        with self.database.transaction() as connection:
            notification_id = insert_and_get_id(
                connection,
                "INSERT INTO notifications(notification_type, title, message, created_at) VALUES ('grafana_alert', ?, ?, ?)",
                (title[:255], message[:1000], now_iso()),
            )
            return self._get_by_id(connection, "notifications", notification_id)

    def list_notifications(
        self,
        unread_only: bool = False,
        limit: int = 100,
        offset: int = 0,
        warehouse_id: int | None = None,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        connection = self.database.connect()
        try:
            query = "SELECT * FROM notifications"
            params: tuple[Any, ...] = ()
            filters: list[str] = []
            if unread_only:
                filters.append("is_read = 0")
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            query += " ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?"
            params = (*params, safe_limit, safe_offset)
            return [dict(row) for row in connection.execute(query, params).fetchall()]
        finally:
            self._close_connection(connection)

    def count_notifications(
        self, unread_only: bool = False, warehouse_id: int | None = None
    ) -> int:
        connection = self.database.connect()
        try:
            query = "SELECT COUNT(*) AS total FROM notifications"
            params: tuple[Any, ...] = ()
            filters: list[str] = []
            if unread_only:
                filters.append("is_read = 0")
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def list_audit_log(
        self,
        entity_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
        warehouse_id: int | None = None,
        actor_id: str | None = None,
        action: str | None = None,
    ) -> list[dict[str, Any]]:
        connection = self.database.connect()
        try:
            safe_limit = max(1, min(limit, 500))
            safe_offset = max(0, offset)
            query = "SELECT * FROM audit_log"
            params: tuple[Any, ...] = ()
            filters: list[str] = []
            if entity_type:
                filters.append("entity_type = ?")
                params = (*params, entity_type)
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if actor_id:
                filters.append("actor_id = ?")
                params = (*params, actor_id)
            if action:
                filters.append("action = ?")
                params = (*params, action)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            query += " ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?"
            params = (*params, safe_limit, safe_offset)
            rows = connection.execute(query, params).fetchall()
            result: list[dict[str, Any]] = []
            for row in rows:
                item = dict(row)
                payload = item["payload"]
                if isinstance(payload, str):
                    payload = json.loads(payload)
                item["payload"] = self._redact_audit_payload(payload)
                result.append(item)
            return result
        finally:
            self._close_connection(connection)

    def count_audit_log(
        self,
        entity_type: str | None = None,
        warehouse_id: int | None = None,
        actor_id: str | None = None,
        action: str | None = None,
    ) -> int:
        connection = self.database.connect()
        try:
            query = "SELECT COUNT(*) AS total FROM audit_log"
            params: tuple[Any, ...] = ()
            filters: list[str] = []
            if entity_type:
                filters.append("entity_type = ?")
                params = (*params, entity_type)
            if warehouse_id is not None:
                filters.append("warehouse_id = ?")
                params = (*params, warehouse_id)
            if actor_id:
                filters.append("actor_id = ?")
                params = (*params, actor_id)
            if action:
                filters.append("action = ?")
                params = (*params, action)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            row = connection.execute(query, params).fetchone()
            return int(row["total"])
        finally:
            self._close_connection(connection)

    def get_notification(self, notification_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_by_id(connection, "notifications", notification_id)
        finally:
            self._close_connection(connection)

    def mark_notification_read(self, notification_id: int, is_read: bool = True) -> dict[str, Any]:
        with self.database.transaction() as connection:
            self._require(connection, "notifications", notification_id)
            connection.execute(
                "UPDATE notifications SET is_read = ?, read_at = ? WHERE id = ?",
                (1 if is_read else 0, now_iso() if is_read else None, notification_id),
            )
            return self._get_by_id(connection, "notifications", notification_id)

    def _create_document(
        self,
        connection: Connection,
        document_type: StockDocumentType,
        warehouse_id: int,
        actor_id: str,
        supplier_id: int | None = None,
        external_ref: str | None = None,
        notes: str | None = None,
    ) -> int:
        if external_ref is not None or notes is not None:
            return insert_and_get_id(
                connection,
                """
                INSERT INTO stock_documents(
                  document_type, status, warehouse_id, supplier_id, created_by, created_at,
                  external_ref, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document_type,
                    StockDocumentStatus.DRAFT,
                    warehouse_id,
                    supplier_id,
                    actor_id,
                    now_iso(),
                    external_ref,
                    notes,
                ),
            )
        return insert_and_get_id(
            connection,
            """
            INSERT INTO stock_documents(
              document_type, status, warehouse_id, supplier_id, created_by, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                document_type,
                StockDocumentStatus.DRAFT,
                warehouse_id,
                supplier_id,
                actor_id,
                now_iso(),
            ),
        )


    # ── ПКУ pending (двойная подпись) ──────────────────────────────────────────

    def create_pending_controlled_writeoff(
        self,
        batch_id: int,
        warehouse_id: int,
        quantity: "Decimal",
        reason: str | None,
        patient_id: str,
        doctor_id: str,
        medical_record_no: str,
        requested_by: str,
    ) -> dict:
        """
        Шаг 1: врач/медсестра подаёт заявку на списание ПКУ.
        Фактического движения нет — ждёт подтверждения second_approver.
        """
        with self.database.transaction() as connection:
            self._ensure_batch_available(connection, batch_id)
            # Validate it's a controlled product
            self._require_controlled_writeoff_metadata(
                connection,
                batch_id=batch_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                medical_record_no=medical_record_no,
                second_approver_id="__pending__",  # bypass: will be filled on confirm
            )
            balance = self._balance_for_update(connection, batch_id, warehouse_id)
            free = Decimal(str(balance["quantity"])) - Decimal(str(balance["reserved_quantity"]))
            if free < quantity:
                raise InsufficientStockError("Insufficient free stock for controlled write-off")

            # Reserve the quantity while pending
            connection.execute(
                """
                UPDATE stock_balances
                SET reserved_quantity = reserved_quantity + ?
                WHERE batch_id = ? AND warehouse_id = ?
                """,
                (decimal_to_db(quantity), batch_id, warehouse_id),
            )

            row_id = insert_and_get_id(
                connection,
                """
                INSERT INTO pending_controlled_writeoffs(
                    batch_id, warehouse_id, quantity, reason,
                    patient_id, doctor_id, medical_record_no,
                    requested_by, requested_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
                """,
                (
                    batch_id,
                    warehouse_id,
                    decimal_to_db(quantity),
                    reason,
                    patient_id,
                    doctor_id,
                    medical_record_no,
                    requested_by,
                    now_iso(),
                ),
            )
            self._audit(
                connection,
                requested_by,
                AuditAction.UPDATE,
                "batch",
                batch_id,
                {
                    "action": "pending_controlled_writeoff_created",
                    "pending_id": row_id,
                    "quantity": str(quantity),
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "medical_record_no": medical_record_no,
                },
                warehouse_id=warehouse_id,
            )
            # Notify warehouse managers that a new ПКУ request needs approval
            try:
                batch_row = connection.execute(
                    "SELECT b.id, p.name AS product_name FROM batches b JOIN products p ON p.id = b.product_id WHERE b.id = ?",
                    (batch_id,),
                ).fetchone()
                pname = batch_row["product_name"] if batch_row else f"партия #{batch_id}"
                insert_and_get_id(
                    connection,
                    """
                    INSERT INTO notifications(
                        notification_type, product_id, batch_id, warehouse_id,
                        title, message, is_read, created_at
                    ) VALUES ('pku_pending', ?, ?, ?, ?, ?, 0, ?)
                    """,
                    (
                        batch_row["id"] if batch_row else batch_id,
                        batch_id,
                        warehouse_id,
                        f"Заявка на списание ПКУ: {pname}",
                        f"Пациент: {patient_id} | Врач: {doctor_id} | ИБ: {medical_record_no} | Запросил: {requested_by} | Кол-во: {quantity}. Требуется подтверждение второго подписанта.",
                        now_iso(),
                    ),
                )
            except Exception:
                pass  # notification failure must not break the writeoff workflow
        return self.get_pending_controlled_writeoff(row_id)

    def confirm_pending_controlled_writeoff(
        self,
        pending_id: int,
        second_approver_id: str,
        note: str | None,
        actor_id: str,
    ) -> dict:
        """
        Шаг 2: второй подписант (старшая медсестра) подтверждает заявку.
        Выполняет фактическое движение.
        """
        with self.database.transaction() as connection:
            pending = self._get_pending_writeoff(connection, pending_id)
            if pending["status"] != "pending":
                raise ValidationError(f"Cannot confirm writeoff in status '{pending['status']}'")
            if second_approver_id.strip() == pending["doctor_id"].strip():
                raise ValidationError("Second approver must be different from the doctor")
            if second_approver_id.strip() == pending["requested_by"].strip():
                raise ValidationError("Second approver must be different from the requester")

            quantity = Decimal(str(pending["quantity"]))
            batch_id = pending["batch_id"]
            warehouse_id = pending["warehouse_id"]

            # Release the reservation
            connection.execute(
                """
                UPDATE stock_balances
                SET reserved_quantity = GREATEST(0, reserved_quantity - ?)
                WHERE batch_id = ? AND warehouse_id = ?
                """,
                (decimal_to_db(quantity), batch_id, warehouse_id),
            )

            # Perform the actual write-off
            movement_id = self._apply_writeoff_line(
                connection,
                batch_id=batch_id,
                warehouse_id=warehouse_id,
                quantity=quantity,
                reason=pending.get("reason"),
                patient_id=pending["patient_id"],
                doctor_id=pending["doctor_id"],
                medical_record_no=pending["medical_record_no"],
                second_approver_id=second_approver_id,
                second_approval_note=note,
            )

            connection.execute(
                """
                UPDATE pending_controlled_writeoffs
                SET status = 'confirmed',
                    second_approver_id = ?,
                    second_approval_note = ?,
                    second_approved_at = ?,
                    writeoff_movement_id = ?
                WHERE id = ?
                """,
                (second_approver_id, note, now_iso(), movement_id, pending_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.WRITE_OFF,
                "batch",
                batch_id,
                {
                    "action": "pending_controlled_writeoff_confirmed",
                    "pending_id": pending_id,
                    "second_approver_id": second_approver_id,
                    "movement_id": movement_id,
                },
                warehouse_id=warehouse_id,
            )
            # Auto-create reorder if needed
            self._check_and_create_reorder_requests(connection, warehouse_id, [int(batch_id)])
        return self.get_pending_controlled_writeoff(pending_id)

    def reject_pending_controlled_writeoff(
        self,
        pending_id: int,
        rejected_reason: str,
        actor_id: str,
    ) -> dict:
        """Второй подписант отклоняет заявку — снимает резерв."""
        with self.database.transaction() as connection:
            pending = self._get_pending_writeoff(connection, pending_id)
            if pending["status"] != "pending":
                raise ValidationError(f"Cannot reject writeoff in status '{pending['status']}'")

            quantity = Decimal(str(pending["quantity"]))

            # Release reservation
            connection.execute(
                """
                UPDATE stock_balances
                SET reserved_quantity = GREATEST(0, reserved_quantity - ?)
                WHERE batch_id = ? AND warehouse_id = ?
                """,
                (decimal_to_db(quantity), pending["batch_id"], pending["warehouse_id"]),
            )
            connection.execute(
                """
                UPDATE pending_controlled_writeoffs
                SET status = 'rejected', rejected_reason = ?
                WHERE id = ?
                """,
                (rejected_reason, pending_id),
            )
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "batch",
                pending["batch_id"],
                {"action": "pending_controlled_writeoff_rejected", "pending_id": pending_id, "reason": rejected_reason},
                warehouse_id=pending["warehouse_id"],
            )
        return self.get_pending_controlled_writeoff(pending_id)

    def list_pending_controlled_writeoffs(
        self,
        warehouse_id: int | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        connection = self.database.connect()
        try:
            wheres = []
            params: list = []
            if warehouse_id is not None:
                wheres.append("p.warehouse_id = ?")
                params.append(warehouse_id)
            if status:
                wheres.append("p.status = ?")
                params.append(status)
            where_sql = ("WHERE " + " AND ".join(wheres)) if wheres else ""
            rows = connection.execute(
                f"""
                SELECT p.*,
                       pr.name AS product_name, pr.sku,
                       b.lot, b.unit_price,
                       w.name AS warehouse_name
                FROM pending_controlled_writeoffs p
                JOIN batches b ON b.id = p.batch_id
                JOIN products pr ON pr.id = b.product_id
                JOIN warehouses w ON w.id = p.warehouse_id
                {where_sql}
                ORDER BY p.requested_at DESC
                LIMIT ? OFFSET ?
                """,
                params + [limit, offset],
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def get_pending_controlled_writeoff(self, pending_id: int) -> dict:
        connection = self.database.connect()
        try:
            row = connection.execute(
                """
                SELECT p.*,
                       pr.name AS product_name, pr.sku,
                       b.lot, b.unit_price,
                       w.name AS warehouse_name
                FROM pending_controlled_writeoffs p
                JOIN batches b ON b.id = p.batch_id
                JOIN products pr ON pr.id = b.product_id
                JOIN warehouses w ON w.id = p.warehouse_id
                WHERE p.id = ?
                """,
                (pending_id,),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"pending_controlled_writeoff#{pending_id} not found")
            return dict(row)
        finally:
            self._close_connection(connection)

    def _get_pending_writeoff(self, connection: "Connection", pending_id: int) -> "Row":
        row = connection.execute(
            "SELECT * FROM pending_controlled_writeoffs WHERE id = ?",
            (pending_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"pending_controlled_writeoff#{pending_id} not found")
        return row

    def _apply_receipt_line(
        self,
        connection: Connection,
        supplier_id: int,
        warehouse_id: int,
        product_id: int,
        quantity: Decimal,
        unit_price: Decimal,
        lot: str,
        serial_number: str | None,
        expires_on: date | None,
        quarantine: bool,
        actor_id: str = "system",
    ) -> int:
        self._ensure_warehouse_open(connection, warehouse_id)
        self._require(connection, "products", product_id)
        self._require(connection, "suppliers", supplier_id)
        status = BatchStatus.QUARANTINE if quarantine else BatchStatus.AVAILABLE
        batch_id = insert_and_get_id(
            connection,
            """
            INSERT INTO batches(
              product_id, supplier_id, received_at, lot, serial_number, expires_on, unit_price, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                product_id,
                supplier_id,
                now_iso(),
                lot,
                serial_number,
                expires_on.isoformat() if expires_on else None,
                decimal_to_db(unit_price),
                status,
            ),
        )
        connection.execute(
            """
            INSERT INTO stock_balances(batch_id, warehouse_id, quantity, reserved_quantity)
            VALUES (?, ?, ?, '0')
            """,
            (batch_id, warehouse_id, decimal_to_db(quantity)),
        )
        self._movement(connection, MovementType.RECEIPT, batch_id, warehouse_id, quantity)
        self._record_supplier_price_history(
            connection,
            supplier_id=supplier_id,
            product_id=product_id,
            batch_id=batch_id,
            lot=lot,
            unit_price=unit_price,
            source="receipt",
        )
        # Auto-flag product label for reprint when price differs from last receipt
        last_price_row = connection.execute(
            """
            SELECT unit_price FROM batches
            WHERE product_id = ? AND id != ?
            ORDER BY id DESC LIMIT 1
            """,
            (product_id, batch_id),
        ).fetchone()
        if last_price_row is not None:
            last_price = Decimal(str(last_price_row["unit_price"]))
            if last_price != unit_price:
                connection.execute(
                    "UPDATE products SET label_needs_reprint = 1 WHERE id = ?",
                    (product_id,),
                )

        if quarantine:
            self._ensure_quarantine_review(
                connection,
                batch_id=batch_id,
                warehouse_id=warehouse_id,
                actor_id=actor_id,
            )
        return batch_id

    def _apply_writeoff_line(
        self,
        connection: Connection,
        batch_id: int,
        warehouse_id: int,
        quantity: Decimal,
        reason: str | None,
        patient_id: str | None = None,
        doctor_id: str | None = None,
        medical_record_no: str | None = None,
        second_approver_id: str | None = None,
        second_approval_note: str | None = None,
    ) -> int:
        self._ensure_warehouse_open(connection, warehouse_id)
        self._ensure_batch_available(connection, batch_id)
        self._require_controlled_writeoff_metadata(
            connection,
            batch_id=batch_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            medical_record_no=medical_record_no,
            second_approver_id=second_approver_id,
        )
        balance = self._balance_for_update(connection, batch_id, warehouse_id)
        free = Decimal(balance["quantity"]) - Decimal(balance["reserved_quantity"])
        if free < quantity:
            raise InsufficientStockError("Not enough free stock for write-off")
        new_quantity = Decimal(balance["quantity"]) - quantity
        connection.execute(
            "UPDATE stock_balances SET quantity = ? WHERE batch_id = ? AND warehouse_id = ?",
            (decimal_to_db(new_quantity), batch_id, warehouse_id),
        )
        return self._movement(
            connection,
            MovementType.WRITE_OFF,
            batch_id,
            warehouse_id,
            quantity,
            reason=reason,
            patient_id=patient_id,
            doctor_id=doctor_id,
            medical_record_no=medical_record_no,
            second_approver_id=second_approver_id,
            second_approval_note=second_approval_note,
        )

    def _require_controlled_writeoff_metadata(
        self,
        connection: Connection,
        *,
        patient_id: str | None,
        doctor_id: str | None,
        medical_record_no: str | None,
        second_approver_id: str | None = None,
        batch_id: int | None = None,
        product_id: int | None = None,
    ) -> None:
        if product_id is None:
            if batch_id is None:
                raise ValidationError("Batch or product is required for write-off validation")
            row = connection.execute(
                """
                SELECT p.is_controlled
                FROM batches b
                JOIN products p ON p.id = b.product_id
                WHERE b.id = ?
                """,
                (batch_id,),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"batches id={batch_id} not found")
            is_controlled = bool(row["is_controlled"])
        else:
            product = self._require(connection, "products", product_id)
            is_controlled = bool(product["is_controlled"])
        if not is_controlled:
            return
        required_fields = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "medical_record_no": medical_record_no,
            "second_approver_id": second_approver_id,
        }
        missing = [
            field
            for field, value in required_fields.items()
            if value is None or not value.strip()
        ]
        if missing:
            raise ValidationError(
                "Controlled product write-off requires patient_id, doctor_id, medical_record_no, second_approver_id"
            )
        if second_approver_id and doctor_id and second_approver_id.strip() == doctor_id.strip():
            raise ValidationError("Controlled product write-off requires a second approver different from doctor_id")

    def _apply_transfer(self, connection: Connection, data: TransferCreate) -> dict[str, Any]:
        if data.source_warehouse_id == data.target_warehouse_id:
            raise ValidationError("Source and target warehouses must be different")
        self._ensure_warehouse_open(connection, data.source_warehouse_id)
        self._ensure_warehouse_open(connection, data.target_warehouse_id)
        self._ensure_batch_available(connection, data.batch_id)
        source_balance = self._balance_for_update(
            connection, data.batch_id, data.source_warehouse_id
        )
        source_free = Decimal(source_balance["quantity"]) - Decimal(
            source_balance["reserved_quantity"]
        )
        if source_free < data.quantity:
            raise InsufficientStockError("Not enough free stock for transfer")
        source_quantity = Decimal(source_balance["quantity"]) - data.quantity
        connection.execute(
            """
            UPDATE stock_balances
            SET quantity = ?
            WHERE batch_id = ? AND warehouse_id = ?
            """,
            (decimal_to_db(source_quantity), data.batch_id, data.source_warehouse_id),
        )
        lock_clause = " FOR UPDATE" if getattr(connection, "dialect", None) == "postgresql" else ""
        target_balance = connection.execute(
            """
            SELECT * FROM stock_balances
            WHERE batch_id = ? AND warehouse_id = ?
            """ + lock_clause,
            (data.batch_id, data.target_warehouse_id),
        ).fetchone()
        if target_balance is None:
            connection.execute(
                """
                INSERT INTO stock_balances(batch_id, warehouse_id, quantity, reserved_quantity)
                VALUES (?, ?, ?, '0')
                """,
                (data.batch_id, data.target_warehouse_id, decimal_to_db(data.quantity)),
            )
        else:
            target_quantity = Decimal(target_balance["quantity"]) + data.quantity
            connection.execute(
                """
                UPDATE stock_balances
                SET quantity = ?
                WHERE batch_id = ? AND warehouse_id = ?
                """,
                (decimal_to_db(target_quantity), data.batch_id, data.target_warehouse_id),
            )
        out_movement_id = self._movement(
            connection,
            MovementType.TRANSFER_OUT,
            data.batch_id,
            data.source_warehouse_id,
            data.quantity,
            reason=data.reason,
        )
        in_movement_id = self._movement(
            connection,
            MovementType.TRANSFER_IN,
            data.batch_id,
            data.target_warehouse_id,
            data.quantity,
            reason=data.reason,
        )
        return {
            "batch_id": data.batch_id,
            "source_warehouse_id": data.source_warehouse_id,
            "target_warehouse_id": data.target_warehouse_id,
            "quantity": decimal_to_db(data.quantity),
            "out_movement_id": out_movement_id,
            "in_movement_id": in_movement_id,
        }

    def _apply_supplier_return_line(
        self,
        connection: Connection,
        batch_id: int,
        warehouse_id: int,
        supplier_id: int,
        quantity: Decimal,
        reason: str,
    ) -> dict[str, Any]:
        self._ensure_warehouse_open(connection, warehouse_id)
        batch = self._require(connection, "batches", batch_id)
        self._require(connection, "suppliers", supplier_id)
        if batch["supplier_id"] != supplier_id:
            raise ValidationError("Return supplier must match the original batch supplier")
        self._ensure_batch_available(connection, batch_id)
        balance = self._balance_for_update(connection, batch_id, warehouse_id)
        free = Decimal(balance["quantity"]) - Decimal(balance["reserved_quantity"])
        if free < quantity:
            raise InsufficientStockError("Not enough free stock for supplier return")
        new_quantity = Decimal(balance["quantity"]) - quantity
        connection.execute(
            """
            UPDATE stock_balances
            SET quantity = ?
            WHERE batch_id = ? AND warehouse_id = ?
            """,
            (decimal_to_db(new_quantity), batch_id, warehouse_id),
        )
        movement_id = self._movement(
            connection,
            MovementType.RETURN_TO_SUPPLIER,
            batch_id,
            warehouse_id,
            quantity,
            reason=reason,
        )
        return {
            "batch_id": batch_id,
            "warehouse_id": warehouse_id,
            "supplier_id": supplier_id,
            "quantity": decimal_to_db(quantity),
            "movement_id": movement_id,
        }

    def _validate_repack_numbers(
        self,
        *,
        source_quantity: Decimal,
        target_quantity: Decimal,
        conversion_factor: Decimal,
        loss_quantity: Decimal,
    ) -> None:
        if source_quantity <= 0 or target_quantity <= 0:
            raise ValidationError("Repack quantities must be positive")
        if conversion_factor <= 0:
            raise ValidationError("Repack conversion factor must be positive")
        if loss_quantity < 0:
            raise ValidationError("Repack loss quantity cannot be negative")
        if loss_quantity >= source_quantity:
            raise ValidationError("Repack loss quantity must be less than source quantity")
        expected_target = (source_quantity - loss_quantity) * conversion_factor
        if expected_target.quantize(Decimal("0.001")) != target_quantity.quantize(Decimal("0.001")):
            raise ValidationError(
                "Repack target quantity must equal (source quantity - loss) * conversion factor"
            )

    def _apply_repack_line(
        self,
        connection: Connection,
        *,
        document_id: int,
        warehouse_id: int,
        source_batch_id: int,
        target_product_id: int,
        source_quantity: Decimal,
        target_quantity: Decimal,
        conversion_factor: Decimal,
        loss_quantity: Decimal,
        target_unit_price: Decimal | None,
        target_lot: str,
        target_expires_on: date | None,
        quarantine: bool,
        reason: str | None,
        actor_id: str,
    ) -> dict[str, Any]:
        self._validate_repack_numbers(
            source_quantity=source_quantity,
            target_quantity=target_quantity,
            conversion_factor=conversion_factor,
            loss_quantity=loss_quantity,
        )
        self._ensure_warehouse_open(connection, warehouse_id)
        source_batch = self._require(connection, "batches", source_batch_id)
        self._ensure_batch_available(connection, source_batch_id)
        self._require(connection, "products", target_product_id)
        balance = self._balance_for_update(connection, source_batch_id, warehouse_id)
        free = Decimal(balance["quantity"]) - Decimal(balance["reserved_quantity"])
        if free < source_quantity:
            raise InsufficientStockError("Not enough free stock for repack")
        new_source_quantity = Decimal(balance["quantity"]) - source_quantity
        connection.execute(
            """
            UPDATE stock_balances
            SET quantity = ?
            WHERE batch_id = ? AND warehouse_id = ?
            """,
            (decimal_to_db(new_source_quantity), source_batch_id, warehouse_id),
        )
        if target_unit_price is None:
            target_unit_price = (Decimal(source_batch["unit_price"]) * source_quantity / target_quantity).quantize(
                Decimal("0.0001")
            )
        status = BatchStatus.QUARANTINE if quarantine else BatchStatus.AVAILABLE
        target_batch_id = insert_and_get_id(
            connection,
            """
            INSERT INTO batches(
              product_id, supplier_id, received_at, lot, expires_on, unit_price, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                target_product_id,
                source_batch["supplier_id"],
                now_iso(),
                target_lot,
                target_expires_on.isoformat() if target_expires_on else source_batch["expires_on"],
                decimal_to_db(target_unit_price),
                status,
            ),
        )
        connection.execute(
            """
            INSERT INTO stock_balances(batch_id, warehouse_id, quantity, reserved_quantity)
            VALUES (?, ?, ?, '0')
            """,
            (target_batch_id, warehouse_id, decimal_to_db(target_quantity)),
        )
        out_movement_id = self._movement(
            connection,
            MovementType.REPACK_OUT,
            source_batch_id,
            warehouse_id,
            source_quantity,
            reason=reason,
        )
        in_movement_id = self._movement(
            connection,
            MovementType.REPACK_IN,
            target_batch_id,
            warehouse_id,
            target_quantity,
            reason=reason,
        )
        transformation_id = insert_and_get_id(
            connection,
            """
            INSERT INTO batch_transformations(
              document_id, source_batch_id, target_batch_id, warehouse_id,
              source_product_id, target_product_id, source_quantity,
              target_quantity, conversion_factor, loss_quantity,
              reason, created_by, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                document_id,
                source_batch_id,
                target_batch_id,
                warehouse_id,
                source_batch["product_id"],
                target_product_id,
                decimal_to_db(source_quantity),
                decimal_to_db(target_quantity),
                decimal_to_db(conversion_factor),
                decimal_to_db(loss_quantity),
                reason,
                actor_id,
                now_iso(),
            ),
        )
        if quarantine:
            self._ensure_quarantine_review(
                connection,
                batch_id=target_batch_id,
                warehouse_id=warehouse_id,
                actor_id=actor_id,
            )
        return {
            "transformation_id": transformation_id,
            "source_batch_id": source_batch_id,
            "target_batch_id": target_batch_id,
            "warehouse_id": warehouse_id,
            "source_quantity": decimal_to_db(source_quantity),
            "target_quantity": decimal_to_db(target_quantity),
            "loss_quantity": decimal_to_db(loss_quantity),
            "out_movement_id": out_movement_id,
            "in_movement_id": in_movement_id,
        }

    def _release_reservation(
        self, connection: Connection, reservation_id: int, actor_id: str
    ) -> dict[str, Any]:
        reservation = self._require(connection, "reservations", reservation_id)
        if reservation["status"] != ReservationStatus.RESERVED:
            return dict(reservation)
        balance = self._balance_for_update(
            connection, reservation["batch_id"], reservation["warehouse_id"]
        )
        reserved = Decimal(balance["reserved_quantity"]) - Decimal(reservation["quantity"])
        if reserved < 0:
            reserved = Decimal("0")
        connection.execute(
            """
            UPDATE stock_balances
            SET reserved_quantity = ?
            WHERE batch_id = ? AND warehouse_id = ?
            """,
            (decimal_to_db(reserved), reservation["batch_id"], reservation["warehouse_id"]),
        )
        connection.execute(
            "UPDATE reservations SET status = ? WHERE id = ?",
            (ReservationStatus.RELEASED, reservation_id),
        )
        self._movement(
            connection,
            MovementType.RELEASE_RESERVE,
            reservation["batch_id"],
            reservation["warehouse_id"],
            Decimal(reservation["quantity"]),
        )
        self._audit(
            connection,
            actor_id,
            AuditAction.RELEASE_RESERVE,
            "reservation",
            reservation_id,
            {"status": ReservationStatus.RELEASED},
            warehouse_id=reservation["warehouse_id"],
        )
        return self._get_by_id(connection, "reservations", reservation_id)

    def _ensure_warehouse_open(self, connection: Connection, warehouse_id: int) -> None:
        warehouse = self._require(connection, "warehouses", warehouse_id)
        if int(warehouse["inventory_lock"]):
            raise InventoryLockedError("Warehouse operations are locked during inventory")

    def _ensure_batch_available(self, connection: Connection, batch_id: int) -> None:
        batch = self._require(connection, "batches", batch_id)
        if batch["status"] != BatchStatus.AVAILABLE:
            raise BatchUnavailableError(f"Batch is not available: {batch['status']}")

    def _balance_for_update(self, connection: Connection, batch_id: int, warehouse_id: int) -> Row:
        lock_clause = " FOR UPDATE" if getattr(connection, "dialect", None) == "postgresql" else ""
        row = connection.execute(
            """
            SELECT * FROM stock_balances
            WHERE batch_id = ? AND warehouse_id = ?
            """ + lock_clause,
            (batch_id, warehouse_id),
        ).fetchone()
        if row is None:
            raise NotFoundError("Stock balance not found")
        return row

    def _batch_warehouse_ids(self, connection: Connection, batch_id: int) -> list[int]:
        rows = connection.execute(
            """
            SELECT warehouse_id FROM stock_balances
            WHERE batch_id = ?
            ORDER BY warehouse_id
            """,
            (batch_id,),
        ).fetchall()
        return [int(row["warehouse_id"]) for row in rows]

    def _batch_balances(self, connection: Connection, batch_id: int) -> list[dict[str, Any]]:
        rows = connection.execute(
            """
            SELECT
              b.product_id,
              sb.batch_id,
              sb.warehouse_id,
              sb.quantity AS total_quantity,
              sb.reserved_quantity,
              b.status AS batch_status,
              b.expires_on
            FROM stock_balances sb
            JOIN batches b ON b.id = sb.batch_id
            WHERE sb.batch_id = ?
            ORDER BY sb.warehouse_id
            """,
            (batch_id,),
        ).fetchall()
        return [self._balance_payload(row) for row in rows]

    def _batch_movements(
        self,
        connection: Connection,
        batch_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        rows = connection.execute(
            """
            SELECT *
            FROM stock_movements
            WHERE batch_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ? OFFSET ?
            """,
            (batch_id, safe_limit, safe_offset),
        ).fetchall()
        movements = [dict(row) for row in rows]
        for movement in movements:
            self._redact_movement_payload(movement)
        return movements

    def _batch_transformations(
        self,
        connection: Connection,
        *,
        warehouse_id: int | None = None,
        batch_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT
              bt.*,
              sp.name AS source_product_name,
              tp.name AS target_product_name,
              sb.lot AS source_lot,
              tb.lot AS target_lot
            FROM batch_transformations bt
            JOIN products sp ON sp.id = bt.source_product_id
            JOIN products tp ON tp.id = bt.target_product_id
            JOIN batches sb ON sb.id = bt.source_batch_id
            JOIN batches tb ON tb.id = bt.target_batch_id
        """
        filters: list[str] = []
        params: tuple[Any, ...] = ()
        if warehouse_id is not None:
            filters.append("bt.warehouse_id = ?")
            params = (*params, warehouse_id)
        if batch_id is not None:
            filters.append("(bt.source_batch_id = ? OR bt.target_batch_id = ?)")
            params = (*params, batch_id, batch_id)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY bt.created_at DESC, bt.id DESC LIMIT ? OFFSET ?"
        rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
        return [dict(row) for row in rows]

    def _batch_recalls(
        self,
        connection: Connection,
        *,
        batch_id: int | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = """
            SELECT
              br.*,
              p.name AS product_name,
              b.lot
            FROM batch_recalls br
            JOIN products p ON p.id = br.product_id
            JOIN batches b ON b.id = br.batch_id
        """
        params: tuple[Any, ...] = ()
        if batch_id is not None:
            query += " WHERE br.batch_id = ?"
            params = (batch_id,)
        query += " ORDER BY br.created_at DESC, br.id DESC LIMIT ? OFFSET ?"
        rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
        return [dict(row) for row in rows]

    def _get_batch_recall(self, connection: Connection, recall_id: int) -> dict[str, Any]:
        rows = self._batch_recalls(connection, limit=1_000)
        for row in rows:
            if int(row["id"]) == int(recall_id):
                return row
        raise NotFoundError(f"batch_recalls#{recall_id} not found")

    def _ensure_recall_notification(
        self,
        connection: Connection,
        *,
        batch_id: int,
        product_id: int,
        warehouse_id: int,
        lot: str,
        reason: str,
        free_quantity: Decimal,
    ) -> dict[str, Any]:
        existing = connection.execute(
            """
            SELECT id FROM notifications
            WHERE notification_type = 'recall'
              AND batch_id = ?
              AND warehouse_id = ?
              AND is_read = 0
            """,
            (batch_id, warehouse_id),
        ).fetchone()
        if existing:
            return self._get_by_id(connection, "notifications", existing["id"])
        title = f"Отозвана партия #{batch_id}"
        message = (
            f"Партия серия {lot} заблокирована из-за отзыва. "
            f"Свободный остаток на складе: {free_quantity}. Причина: {reason}"
        )
        notification_id = insert_and_get_id(
            connection,
            """
            INSERT INTO notifications(
              notification_type, product_id, batch_id, warehouse_id, title, message, created_at
            ) VALUES ('recall', ?, ?, ?, ?, ?, ?)
            """,
            (product_id, batch_id, warehouse_id, title, message, now_iso()),
        )
        return self._get_by_id(connection, "notifications", notification_id)

    def _movement(
        self,
        connection: Connection,
        movement_type: MovementType,
        batch_id: int,
        warehouse_id: int,
        quantity: Decimal,
        reason: str | None = None,
        patient_id: str | None = None,
        doctor_id: str | None = None,
        medical_record_no: str | None = None,
        second_approver_id: str | None = None,
        second_approval_note: str | None = None,
    ) -> int:
        return insert_and_get_id(
            connection,
            """
            INSERT INTO stock_movements(
              movement_type, batch_id, warehouse_id, quantity, reason,
              patient_id, doctor_id, medical_record_no,
              second_approver_id, second_approval_note, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                movement_type,
                batch_id,
                warehouse_id,
                decimal_to_db(quantity),
                reason,
                patient_id,
                doctor_id,
                medical_record_no,
                second_approver_id,
                second_approval_note,
                now_iso(),
            ),
        )

    def _audit(
        self,
        connection: Connection,
        actor_id: str,
        action: AuditAction,
        entity_type: str,
        entity_id: int,
        payload: Any,
        warehouse_id: int | None = None,
    ) -> None:
        from app.core.request_context import get_request_id, get_ip_address, get_user_agent
        if hasattr(payload, "model_dump"):
            payload = payload.model_dump(mode="json")
        payload = self._json_payload(payload)
        if warehouse_id is None:
            warehouse_id = self._audit_warehouse_id(payload)
        request_id = get_request_id() or None
        ip_address = get_ip_address() or None
        user_agent = get_user_agent() or None
        connection.execute(
            """
            INSERT INTO audit_log(
              actor_id, action, entity_type, entity_id, warehouse_id, payload, created_at,
              request_id, ip_address, user_agent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                actor_id,
                action,
                entity_type,
                str(entity_id),
                warehouse_id,
                json.dumps(payload),
                now_iso(),
                request_id,
                ip_address,
                user_agent,
            ),
        )

    def _audit_warehouse_id(self, payload: Any) -> int | None:
        if not isinstance(payload, dict):
            return None
        for key in ("warehouse_id", "source_warehouse_id", "target_warehouse_id"):
            value = payload.get(key)
            if isinstance(value, int):
                return value
        return None

    def _redact_audit_payload(self, payload: Any) -> Any:
        sensitive_keys = {"patient_id", "doctor_id", "medical_record_no", "second_approval_note"}
        if isinstance(payload, dict):
            return {
                key: "***" if key in sensitive_keys and value is not None else self._redact_audit_payload(value)
                for key, value in payload.items()
            }
        if isinstance(payload, list):
            return [self._redact_audit_payload(value) for value in payload]
        return payload

    def _redact_movement_payload(self, movement: dict[str, Any]) -> None:
        for key in ("patient_id", "doctor_id", "medical_record_no", "second_approval_note"):
            if movement.get(key) is not None:
                movement[key] = "***"

    def _product_label_zpl(self, name: str, sku: str, barcode: str, symbology: str = "CODE128") -> str:
        safe_name = self._zpl_text(name)[:42]
        safe_sku = self._zpl_text(sku)[:36]
        safe_barcode = self._zpl_barcode(barcode)
        barcode_command = "^BEN,92,Y,N" if symbology == "EAN13" else "^BCN,92,Y,N,N"
        return (
            "^XA\n"
            "^CI28\n"
            "^PW560\n"
            "^LL320\n"
            "^FO28,28^A0N,32,32^FD" + safe_name + "^FS\n"
            "^FO28,70^A0N,24,24^FDSKU: " + safe_sku + "^FS\n"
            "^FO28,112^BY2,2,92" + barcode_command + "^FD" + safe_barcode + "^FS\n"
            "^XZ"
        )

    def _product_label_epl(self, name: str, sku: str, barcode: str, symbology: str = "CODE128") -> str:
        safe_name = self._epl_text(name)[:38]
        safe_sku = self._epl_text(sku)[:34]
        safe_barcode = self._zpl_barcode(barcode)
        barcode_type = "E30" if symbology == "EAN13" else "1"
        return (
            "N\n"
            "q560\n"
            "Q320,24\n"
            f'A28,28,0,3,1,1,N,"{safe_name}"\n'
            f'A28,70,0,2,1,1,N,"SKU: {safe_sku}"\n'
            f'B28,112,0,{barcode_type},2,4,92,B,"{safe_barcode}"\n'
            "P1\n"
        )

    def _price_label_zpl(
        self,
        name: str,
        sku: str,
        lot: str,
        serial_number: str | None,
        expires_on: Any,
        unit_price: Decimal,
        barcode: str,
        symbology: str,
    ) -> str:
        safe_name = self._zpl_text(name)[:42]
        safe_sku = self._zpl_text(sku)[:36]
        safe_lot = self._zpl_text(lot)[:32]
        safe_serial = self._zpl_text(serial_number or "—")[:32]
        safe_expiry = self._zpl_text(expires_on or "без срока")[:24]
        safe_price = self._zpl_text(self._report_decimal(unit_price))[:24]
        safe_barcode = self._zpl_barcode(barcode)
        barcode_command = "^BEN,76,Y,N" if symbology == "EAN13" else "^BCN,76,Y,N,N"
        return (
            "^XA\n"
            "^CI28\n"
            "^PW560\n"
            "^LL390\n"
            "^FO28,24^A0N,32,32^FD" + safe_name + "^FS\n"
            "^FO28,64^A0N,22,22^FDSKU: " + safe_sku + "^FS\n"
            "^FO28,94^A0N,22,22^FDСерия: " + safe_lot + "^FS\n"
            "^FO28,124^A0N,22,22^FDСерийный: " + safe_serial + "^FS\n"
            "^FO28,154^A0N,22,22^FDГоден до: " + safe_expiry + "^FS\n"
            "^FO28,188^A0N,34,34^FDЦена: " + safe_price + "^FS\n"
            "^FO28,248^BY2,2,76" + barcode_command + "^FD" + safe_barcode + "^FS\n"
            "^XZ"
        )

    def _price_label_epl(
        self,
        name: str,
        sku: str,
        lot: str,
        serial_number: str | None,
        expires_on: Any,
        unit_price: Decimal,
        barcode: str,
        symbology: str,
    ) -> str:
        safe_name = self._epl_text(name)[:38]
        safe_sku = self._epl_text(sku)[:34]
        safe_lot = self._epl_text(lot)[:30]
        safe_serial = self._epl_text(serial_number or "—")[:30]
        safe_expiry = self._epl_text(expires_on or "без срока")[:24]
        safe_price = self._epl_text(self._report_decimal(unit_price))[:24]
        safe_barcode = self._zpl_barcode(barcode)
        barcode_type = "E30" if symbology == "EAN13" else "1"
        return (
            "N\n"
            "q560\n"
            "Q360,24\n"
            f'A28,24,0,3,1,1,N,"{safe_name}"\n'
            f'A28,64,0,2,1,1,N,"SKU: {safe_sku}"\n'
            f'A28,94,0,2,1,1,N,"Серия: {safe_lot}"\n'
            f'A28,124,0,2,1,1,N,"Серийный: {safe_serial}"\n'
            f'A28,154,0,2,1,1,N,"Годен до: {safe_expiry}"\n'
            f'A28,188,0,3,1,1,N,"Цена: {safe_price}"\n'
            f'B28,248,0,{barcode_type},2,4,76,B,"{safe_barcode}"\n'
            "P1\n"
        )

    def _build_product_barcode_label(
        self, connection: Connection, product_id: int, symbology: str = "code128"
    ) -> dict[str, Any]:
        product = dict(self._require(connection, "products", product_id))
        normalized_symbology = self._normalize_label_symbology(symbology)
        barcode = self._label_barcode(product.get("barcode"), product_id, normalized_symbology)
        label_text = f"{product['name']} | {product['sku']}"
        return {
            "product_id": product_id,
            "name": product["name"],
            "sku": product["sku"],
            "barcode": barcode,
            "symbology": normalized_symbology,
            "label_text": label_text,
            "zpl": self._product_label_zpl(product["name"], product["sku"], barcode, normalized_symbology),
            "epl": self._product_label_epl(product["name"], product["sku"], barcode, normalized_symbology),
            "svg": self._generate_svg_barcode(barcode, normalized_symbology),
            "label_needs_reprint": bool(product.get("label_needs_reprint", False)),
        }

    def _build_batch_price_label(
        self, connection: Connection, batch_id: int, symbology: str = "code128"
    ) -> dict[str, Any]:
        row = connection.execute(
            """
            SELECT
              b.id AS batch_id,
              b.product_id,
              b.lot,
              b.serial_number,
              b.expires_on,
              b.unit_price,
              p.name,
              p.sku,
              p.barcode
            FROM batches b
            JOIN products p ON p.id = b.product_id
            WHERE b.id = ?
            """,
            (batch_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"batches#{batch_id} not found")
        item = dict(row)
        normalized_symbology = self._normalize_label_symbology(symbology)
        barcode = self._label_barcode(item.get("barcode"), item["product_id"], normalized_symbology)
        unit_price = Decimal(str(item["unit_price"]))
        label_text = f"{item['name']} | {item['sku']} | {self._report_decimal(unit_price)}"
        if item.get("serial_number"):
            label_text += f" | serial {item['serial_number']}"
        return {
            "batch_id": batch_id,
            "product_id": item["product_id"],
            "name": item["name"],
            "sku": item["sku"],
            "lot": item["lot"],
            "serial_number": item.get("serial_number"),
            "expires_on": item["expires_on"],
            "unit_price": unit_price,
            "barcode": barcode,
            "symbology": normalized_symbology,
            "label_text": label_text,
            "zpl": self._price_label_zpl(
                item["name"], item["sku"], item["lot"], item.get("serial_number"), item["expires_on"], unit_price, barcode, normalized_symbology
            ),
            "epl": self._price_label_epl(
                item["name"], item["sku"], item["lot"], item.get("serial_number"), item["expires_on"], unit_price, barcode, normalized_symbology
            ),
            "svg": self._generate_svg_barcode(barcode, normalized_symbology),
        }

    def _record_supplier_price_history(
        self,
        connection: Connection,
        supplier_id: int,
        product_id: int,
        batch_id: int | None,
        lot: str | None,
        unit_price: Decimal,
        source: str,
    ) -> None:
        connection.execute(
            """
            INSERT INTO supplier_price_history(
              supplier_id, product_id, batch_id, lot, unit_price, source, recorded_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                supplier_id,
                product_id,
                batch_id,
                lot,
                decimal_to_db(unit_price),
                source,
                now_iso(),
            ),
        )


    def mark_product_reprinted(self, product_id: int) -> dict:
        with self.database.transaction() as connection:
            row = self._require(connection, "products", product_id)
            connection.execute(
                "UPDATE products SET label_needs_reprint = ? WHERE id = ?",
                (False, product_id),
            )
            return dict(row)

    def create_supplier_review(self, supplier_id: int, rating: int, comment: str | None, reviewer_id: str) -> dict:
        if not 1 <= rating <= 5:
            raise ValidationError("Rating must be between 1 and 5")
        with self.database.transaction() as connection:
            self._require(connection, "suppliers", supplier_id)
            row = connection.execute(
                """INSERT INTO supplier_reviews(supplier_id, rating, comment, reviewer_id, status, created_at)
                   VALUES (?, ?, ?, ?, 'pending', ?)
                   RETURNING *""",
                (supplier_id, rating, comment, reviewer_id, now_iso()),
            ).fetchone()
            return dict(row)

    def list_supplier_reviews(self, supplier_id: int, status: str | None = None) -> list[dict]:
        connection = self.database.connect()
        try:
            q = "SELECT * FROM supplier_reviews WHERE supplier_id = ?"
            params: list = [supplier_id]
            if status:
                q += " AND status = ?"
                params.append(status)
            q += " ORDER BY created_at DESC"
            rows = connection.execute(q, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def moderate_supplier_review(self, review_id: int, action: str) -> dict:
        if action not in ("approve", "reject"):
            raise ValidationError("action must be approve or reject")
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT * FROM supplier_reviews WHERE id = ?", (review_id,)
            ).fetchone()
            if not row:
                raise NotFoundError(f"supplier_reviews#{review_id} not found")
            new_status = "approved" if action == "approve" else "rejected"
            connection.execute(
                "UPDATE supplier_reviews SET status = ? WHERE id = ?",
                (new_status, review_id),
            )
            # Recompute average rating from approved reviews
            if action == "approve":
                avg_row = connection.execute(
                    "SELECT ROUND(AVG(rating)) AS avg_rating FROM supplier_reviews WHERE supplier_id = ? AND status = 'approved'",
                    (row["supplier_id"],),
                ).fetchone()
                if avg_row and avg_row["avg_rating"] is not None:
                    new_rating = int(avg_row["avg_rating"])
                    connection.execute(
                        "UPDATE suppliers SET rating = ? WHERE id = ?",
                        (new_rating, row["supplier_id"]),
                    )
            updated = connection.execute(
                "SELECT * FROM supplier_reviews WHERE id = ?", (review_id,)
            ).fetchone()
            return dict(updated)

    def reply_to_review(self, review_id: int, supplier_id: int, reply_text: str) -> dict:
        if not reply_text or not reply_text.strip():
            raise ValidationError("reply_text cannot be empty")
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT * FROM supplier_reviews WHERE id = ? AND supplier_id = ?",
                (review_id, supplier_id),
            ).fetchone()
            if not row:
                raise NotFoundError(f"supplier_reviews#{review_id} not found for this supplier")
            if row["status"] != "approved":
                raise ValidationError("Can only reply to approved reviews")
            connection.execute(
                "UPDATE supplier_reviews SET supplier_reply = ?, replied_at = ? WHERE id = ?",
                (reply_text.strip(), now_iso(), review_id),
            )
            updated = connection.execute(
                "SELECT * FROM supplier_reviews WHERE id = ?", (review_id,)
            ).fetchone()
            return dict(updated)

    def list_supplier_orders(
        self,
        supplier_id: int,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Completed/ordered inquiries for supplier — their order history."""
        connection = self.database.connect()
        try:
            where = ["mi.supplier_id = ?"]
            params: list = [supplier_id]
            if status:
                where.append("mi.status = ?")
                params.append(status)
            else:
                where.append("mi.status IN ('ordered', 'closed')")
            where_clause = "WHERE " + " AND ".join(where)
            total_row = connection.execute(
                f"SELECT COUNT(*) AS n FROM marketplace_inquiries mi {where_clause}", params
            ).fetchone()
            rows = connection.execute(
                f"""SELECT mi.*, ci.product_name, ci.sku, ci.unit,
                           s.name AS supplier_name,
                           w.name AS warehouse_name,
                           COALESCE(mi.quantity * mi.unit_price, 0) AS total_amount
                    FROM marketplace_inquiries mi
                    JOIN supplier_catalog_items ci ON ci.id = mi.catalog_item_id
                    JOIN suppliers s ON s.id = mi.supplier_id
                    LEFT JOIN warehouses w ON w.id = mi.warehouse_id
                    {where_clause}
                    ORDER BY mi.created_at DESC
                    LIMIT ? OFFSET ?""",
                params + [limit, offset],
            ).fetchall()
            items = [dict(r) for r in rows]
            return {"items": items, "total": total_row["n"] if total_row else 0}
        finally:
            self._close_connection(connection)

    def bulk_update_catalog_prices(
        self,
        supplier_id: int,
        item_ids: list[int] | None,
        percent_change: float,
    ) -> dict[str, Any]:
        """Apply a percentage price change to selected (or all) catalog items."""
        if not -99 < percent_change < 1000:
            raise ValidationError("percent_change must be between -99 and 1000")
        multiplier = 1 + percent_change / 100
        with self.database.transaction() as connection:
            if item_ids:
                placeholders = ",".join("?" * len(item_ids))
                connection.execute(
                    f"""UPDATE supplier_catalog_items
                        SET unit_price = ROUND(unit_price * ?, 2), updated_at = ?
                        WHERE supplier_id = ? AND id IN ({placeholders})""",
                    [multiplier, now_iso(), supplier_id] + list(item_ids),
                )
                updated_count = len(item_ids)
            else:
                result = connection.execute(
                    """UPDATE supplier_catalog_items
                       SET unit_price = ROUND(unit_price * ?, 2), updated_at = ?
                       WHERE supplier_id = ?""",
                    (multiplier, now_iso(), supplier_id),
                )
                updated_count = result.rowcount if hasattr(result, "rowcount") else 0
            updated_rows = connection.execute(
                "SELECT id, product_name, unit_price FROM supplier_catalog_items WHERE supplier_id = ? ORDER BY updated_at DESC",
                (supplier_id,),
            ).fetchall()
            return {"updated": updated_count, "items": [dict(r) for r in updated_rows]}

    def compare_catalog_items(self, item_ids: list[int]) -> list[dict[str, Any]]:
        """Fetch multiple catalog items with supplier info for side-by-side comparison."""
        if not item_ids or len(item_ids) > 6:
            raise ValidationError("Provide 1–6 item IDs to compare")
        connection = self.database.connect()
        try:
            placeholders = ",".join("?" * len(item_ids))
            rows = connection.execute(
                f"""SELECT ci.*, s.name AS supplier_name, s.city AS supplier_city,
                           s.rating AS supplier_rating, s.delivery_days AS supplier_delivery_days,
                           s.is_preferred AS supplier_is_preferred
                    FROM supplier_catalog_items ci
                    JOIN suppliers s ON s.id = ci.supplier_id
                    WHERE ci.id IN ({placeholders}) AND ci.is_active = TRUE
                    ORDER BY ci.unit_price ASC""",
                item_ids,
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def _generate_svg_barcode(self, barcode_value: str, symbology: str) -> str:
        try:
            import barcode as bc
            import io
            from barcode.writer import SVGWriter
            bc_class = bc.get_barcode_class("code128" if symbology == "CODE128" else "ean13")
            writer = SVGWriter()
            code = bc_class(barcode_value, writer=writer)
            buf = io.BytesIO()
            code.write(buf)
            return buf.getvalue().decode("utf-8")
        except Exception:
            return ""

    def _normalize_label_symbology(self, symbology: str) -> str:
        value = str(symbology or "code128").strip().lower().replace("-", "")
        if value in {"code128", "code"}:
            return "CODE128"
        if value in {"ean13", "ean"}:
            return "EAN13"
        raise ValidationError("Unsupported label symbology")

    def _label_barcode(self, raw_barcode: Any, entity_id: int, symbology: str) -> str:
        if symbology == "EAN13":
            return self._ean13_barcode(raw_barcode, entity_id)
        barcode = (str(raw_barcode or "").strip() or f"SKLAD-{int(entity_id):08d}").strip()
        return self._zpl_barcode(barcode)

    def _ean13_barcode(self, raw_barcode: Any, entity_id: int) -> str:
        digits = "".join(char for char in str(raw_barcode or "") if char.isdigit())
        if len(digits) == 13 and self._ean13_check_digit(digits[:12]) == int(digits[-1]):
            return digits
        if len(digits) == 12:
            return digits + str(self._ean13_check_digit(digits))
        base = f"20{int(entity_id):010d}"[-12:]
        return base + str(self._ean13_check_digit(base))

    def _ean13_check_digit(self, first_12_digits: str) -> int:
        if len(first_12_digits) != 12 or not first_12_digits.isdigit():
            raise ValidationError("EAN-13 requires 12 numeric digits before checksum")
        total = 0
        for index, char in enumerate(first_12_digits):
            digit = int(char)
            total += digit if index % 2 == 0 else digit * 3
        return (10 - (total % 10)) % 10

    def _csv_cell(self, value: Any) -> str:
        text = str(value)
        if any(char in text for char in ('"', ";", "\n", "\r")):
            return '"' + text.replace('"', '""') + '"'
        return text

    def _epl_text(self, value: Any) -> str:
        return (
            str(value)
            .replace('"', "'")
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()
        )

    def _zpl_text(self, value: str) -> str:
        return str(value).replace("^", " ").replace("~", " ").replace("\n", " ").strip()

    def _zpl_barcode(self, value: str) -> str:
        cleaned = self._zpl_text(value).replace(" ", "")
        if not cleaned:
            raise ValidationError("Barcode value cannot be empty")
        return cleaned[:64]

    def _json_payload(self, payload: Any) -> Any:
        if hasattr(payload, "model_dump"):
            return payload.model_dump(mode="json")
        if isinstance(payload, Decimal):
            return str(payload)
        if isinstance(payload, (date, datetime)):
            return payload.isoformat()
        if isinstance(payload, Enum):
            return payload.value
        if isinstance(payload, dict):
            return {key: self._json_payload(value) for key, value in payload.items()}
        if isinstance(payload, list):
            return [self._json_payload(value) for value in payload]
        return payload

    def _order_list_row(self, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": row["id"],
            "number": row["order_number"],
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row.get("updated_at"),
            "total_amount": float(row["total_amount"]) if row.get("total_amount") is not None else None,
            "currency": row.get("currency") or "KZT",
            "items_count": int(row.get("items_count") or 0),
            "supplier_id": row.get("supplier_id"),
            "supplier_name": row.get("supplier_name"),
            "product_name": row.get("product_name"),
            "payment_status": row.get("payment_status") or ("paid" if row.get("status") == "paid" else "unpaid"),
            "delivery_status": self._delivery_status_for_order(row.get("status")),
        }

    def _delivery_status_for_order(self, status_value: Any) -> str:
        status_text = str(status_value or "")
        if status_text in {"delivered", "completed"}:
            return "delivered"
        if status_text == "shipped":
            return "in_transit"
        if status_text in {"accepted", "preparing"}:
            return "preparing"
        return "not_started"

    def _get_marketplace_order_for_actor_conn(
        self, connection: Connection, actor_id: str, order_id: int
    ) -> dict[str, Any]:
        row = connection.execute(
            """SELECT mo.*, s.name AS supplier_name
               FROM marketplace_orders mo
               JOIN suppliers s ON s.id = mo.supplier_id
               WHERE mo.id = ? AND mo.actor_id = ?""",
            (order_id, actor_id),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"marketplace order {order_id} not found")
        return dict(row)

    def _get_marketplace_order_for_actor(self, actor_id: str, order_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            return self._get_marketplace_order_for_actor_conn(connection, actor_id, order_id)
        finally:
            self._close_connection(connection)

    def _get_marketplace_order_for_supplier(self, supplier_id: int, order_id: int) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            row = connection.execute(
                """SELECT mo.*, s.name AS supplier_name
                   FROM marketplace_orders mo
                   JOIN suppliers s ON s.id = mo.supplier_id
                   WHERE mo.id = ? AND mo.supplier_id = ?""",
                (order_id, supplier_id),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"marketplace order {order_id} not found")
            return dict(row)
        finally:
            self._close_connection(connection)

    def _marketplace_order_detail(self, order: dict[str, Any]) -> dict[str, Any]:
        connection = self.database.connect()
        try:
            items = connection.execute(
                """SELECT id, catalog_item_id, product_id, product_name, sku, unit,
                          quantity, unit_price, line_total
                   FROM marketplace_order_items
                   WHERE order_id = ?
                   ORDER BY id""",
                (order["id"],),
            ).fetchall()
            payment = connection.execute(
                """SELECT id, provider, status, amount, currency, payment_url, created_at, updated_at
                   FROM marketplace_payments
                   WHERE order_id = ?
                   ORDER BY created_at DESC, id DESC
                   LIMIT 1""",
                (order["id"],),
            ).fetchone()
            detail = self._order_list_row({
                **order,
                "items_count": len(items),
                "product_name": items[0]["product_name"] if items else None,
                "payment_status": payment["status"] if payment else None,
            })
            detail.update(
                {
                    "buyer_name": order.get("buyer_name"),
                    "buyer_phone": order.get("buyer_phone"),
                    "buyer_email": order.get("buyer_email"),
                    "delivery_address": order.get("delivery_address"),
                    "notes": order.get("notes"),
                    "items": [
                        {
                            "id": row["id"],
                            "catalog_item_id": row["catalog_item_id"],
                            "product_id": row["product_id"],
                            "product_name": row["product_name"],
                            "sku": row["sku"],
                            "quantity": float(row["quantity"]),
                            "unit": row["unit"],
                            "unit_price": float(row["unit_price"]) if row["unit_price"] is not None else None,
                            "line_total": float(row["line_total"]) if row["line_total"] is not None else None,
                            "image_url": None,
                        }
                        for row in items
                    ],
                    "latest_payment": dict(payment) if payment else None,
                    "timeline": self._marketplace_order_timeline(order, payment),
                }
            )
            return detail
        finally:
            self._close_connection(connection)

    def _marketplace_order_timeline(self, order: dict[str, Any], payment: Row | None) -> list[dict[str, Any]]:
        timeline = [
            {
                "id": "created",
                "title": "Заказ создан",
                "description": "Заказ сформирован из корзины.",
                "created_at": order["created_at"],
                "status": "draft",
            }
        ]
        if payment:
            timeline.append(
                {
                    "id": f"payment-{payment['id']}",
                    "title": "Оплата подтверждена" if payment["status"] == "paid" else "Ожидается оплата",
                    "description": "Статус поступает от платежного провайдера.",
                    "created_at": payment["updated_at"] or payment["created_at"],
                    "status": order["status"],
                }
            )
        return timeline

    def _payment_method_public(self, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": str(row["id"]),
            "provider": row.get("provider"),
            "brand": row.get("brand") or "unknown",
            "last4": row.get("last4"),
            "expiry_month": row.get("expiry_month"),
            "expiry_year": row.get("expiry_year"),
            "holder_name": row.get("holder_name"),
            "is_default": bool(row.get("is_default")),
            "status": row.get("status") or "active",
        }

    def _mark_marketplace_order_paid(
        self, connection: Connection, order_id: int, payment_id: int
    ) -> None:
        payment = connection.execute(
            "SELECT * FROM marketplace_payments WHERE id = ?",
            (payment_id,),
        ).fetchone()
        if payment is None:
            raise NotFoundError(f"payment {payment_id} not found")
        order = connection.execute(
            "SELECT * FROM marketplace_orders WHERE id = ?",
            (order_id,),
        ).fetchone()
        if order is None:
            raise NotFoundError(f"marketplace order {order_id} not found")
        now = now_iso()
        connection.execute(
            "UPDATE marketplace_orders SET status = 'paid', paid_at = ?, updated_at = ? WHERE id = ? AND status <> 'paid'",
            (now, now, order_id),
        )
        supplier_id = int(order["supplier_id"])
        amount = Decimal(str(payment["amount"]))
        account = connection.execute(
            "SELECT id FROM marketplace_seller_accounts WHERE supplier_id = ?",
            (supplier_id,),
        ).fetchone()
        if account is None:
            insert_and_get_id(
                connection,
                """INSERT INTO marketplace_seller_accounts(
                     supplier_id, currency, available_amount, pending_amount, created_at, updated_at
                   ) VALUES (?, 'KZT', 0, 0, ?, ?)""",
                (supplier_id, now, now),
            )
        source_id = str(payment_id)
        existing = connection.execute(
            """SELECT id FROM marketplace_seller_ledger
               WHERE source_type = 'payment' AND source_id = ? AND entry_type = 'credit'""",
            (source_id,),
        ).fetchone()
        if existing is None:
            insert_and_get_id(
                connection,
                """INSERT INTO marketplace_seller_ledger(
                     supplier_id, order_id, payment_id, entry_type, status, amount,
                     currency, description, source_type, source_id, created_at
                   ) VALUES (?, ?, ?, 'credit', 'posted', ?, 'KZT', ?, 'payment', ?, ?)""",
                (
                    supplier_id,
                    order_id,
                    payment_id,
                    decimal_to_db(amount),
                    f"Оплата заказа {order['order_number']}",
                    source_id,
                    now,
                ),
            )
            connection.execute(
                """UPDATE marketplace_seller_accounts
                   SET available_amount = CAST(available_amount AS NUMERIC) + CAST(? AS NUMERIC),
                       updated_at = ?
                   WHERE supplier_id = ?""",
                (decimal_to_db(amount), now, supplier_id),
            )

    def _optional_decimal_to_db(self, value: Decimal | int | str | None) -> str | None:
        if value is None:
            return None
        return decimal_to_db(value)

    def _validate_sensor_thresholds(
        self, data: SensorDeviceCreate | SensorDeviceUpdate
    ) -> None:
        if (
            data.min_temperature_c is not None
            and data.max_temperature_c is not None
            and data.min_temperature_c > data.max_temperature_c
        ):
            raise ValidationError("Minimum temperature cannot be greater than maximum temperature")
        if (
            data.min_humidity_percent is not None
            and data.max_humidity_percent is not None
            and data.min_humidity_percent > data.max_humidity_percent
        ):
            raise ValidationError("Minimum humidity cannot be greater than maximum humidity")
        for value in (data.min_humidity_percent, data.max_humidity_percent):
            if value is not None and (value < Decimal("0") or value > Decimal("100")):
                raise ValidationError("Humidity threshold must be between 0 and 100")

    def _validate_sensor_reading(self, data: SensorReadingCreate) -> None:
        if data.temperature_c is None and data.humidity_percent is None:
            raise ValidationError("Sensor reading requires temperature or humidity")
        if data.humidity_percent is not None and (
            data.humidity_percent < Decimal("0") or data.humidity_percent > Decimal("100")
        ):
            raise ValidationError("Humidity reading must be between 0 and 100")

    def _sensor_reading_status(
        self, device: dict[str, Any], data: SensorReadingCreate
    ) -> str:
        if data.temperature_c is not None:
            min_temperature = device.get("min_temperature_c")
            max_temperature = device.get("max_temperature_c")
            if min_temperature is not None and data.temperature_c < Decimal(str(min_temperature)):
                return "warning"
            if max_temperature is not None and data.temperature_c > Decimal(str(max_temperature)):
                return "warning"
        if data.humidity_percent is not None:
            min_humidity = device.get("min_humidity_percent")
            max_humidity = device.get("max_humidity_percent")
            if min_humidity is not None and data.humidity_percent < Decimal(str(min_humidity)):
                return "warning"
            if max_humidity is not None and data.humidity_percent > Decimal(str(max_humidity)):
                return "warning"
        return "ok"

    def _sensor_warning_details(
        self, device: dict[str, Any], reading: dict[str, Any]
    ) -> list[str]:
        details: list[str] = []
        temperature = reading.get("temperature_c")
        if temperature is not None:
            value = Decimal(str(temperature))
            min_temperature = device.get("min_temperature_c")
            max_temperature = device.get("max_temperature_c")
            norm = self._format_sensor_range(min_temperature, max_temperature, "°C")
            if min_temperature is not None and value < Decimal(str(min_temperature)):
                details.append(f"температура {value} °C ниже нормы {norm}")
            elif max_temperature is not None and value > Decimal(str(max_temperature)):
                details.append(f"температура {value} °C выше нормы {norm}")
        humidity = reading.get("humidity_percent")
        if humidity is not None:
            value = Decimal(str(humidity))
            min_humidity = device.get("min_humidity_percent")
            max_humidity = device.get("max_humidity_percent")
            norm = self._format_sensor_range(min_humidity, max_humidity, "%")
            if min_humidity is not None and value < Decimal(str(min_humidity)):
                details.append(f"влажность {value} % ниже нормы {norm}")
            elif max_humidity is not None and value > Decimal(str(max_humidity)):
                details.append(f"влажность {value} % выше нормы {norm}")
        if not details:
            details.append("значение вне настроенных порогов датчика")
        return details

    def _format_sensor_range(self, low: Any, high: Any, unit: str) -> str:
        if low is not None and high is not None:
            return f"{low}…{high} {unit}"
        if low is not None:
            return f"от {low} {unit}"
        if high is not None:
            return f"до {high} {unit}"
        return f"не задана {unit}"

    def _require(self, connection: Connection, table: str, entity_id: int) -> Row:
        row = connection.execute(f"SELECT * FROM {table} WHERE id = ?", (entity_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"{table}#{entity_id} not found")
        return row

    def _require_active(self, connection: Connection, table: str, entity_id: int) -> Row:
        row = self._require(connection, table, entity_id)
        if "is_active" in row.keys() and not bool(row["is_active"]):
            raise ValidationError(f"{table}#{entity_id} is inactive")
        return row

    def _get_purchase_request(
        self, connection: Connection, request_id: int
    ) -> dict[str, Any]:
        row = connection.execute(
            """
            SELECT
              pr.*,
              p.name AS product_name,
              p.sku
            FROM purchase_requests pr
            JOIN products p ON p.id = pr.product_id
            WHERE pr.id = ?
            """,
            (request_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"purchase_requests#{request_id} not found")
        return dict(row)

    def _get_supplier_application(
        self, connection: Connection, application_id: int
    ) -> dict[str, Any]:
        row = connection.execute(
            """
            SELECT
              sa.*,
              s.name AS supplier_name
            FROM supplier_applications sa
            LEFT JOIN suppliers s ON s.id = sa.supplier_id
            WHERE sa.id = ?
            """,
            (application_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"supplier_applications#{application_id} not found")
        return dict(row)

    def _get_abc_xyz_run(self, connection: Connection, run_id: int) -> dict[str, Any]:
        run = dict(self._require(connection, "abc_xyz_runs", run_id))
        rows = connection.execute(
            """
            SELECT
              product_id,
              product_name,
              sku,
              abc_class,
              xyz_class,
              consumption_quantity,
              consumption_value,
              current_free_quantity,
              reorder_point,
              safety_stock,
              recommended_order_quantity,
              recommendation,
              movement_count
            FROM abc_xyz_run_items
            WHERE run_id = ?
            ORDER BY product_name, product_id
            """,
            (run_id,),
        ).fetchall()
        run["items"] = [dict(row) for row in rows]
        return run

    def _get_quarantine_review(self, connection: Connection, review_id: int) -> dict[str, Any]:
        row = connection.execute(
            """
            SELECT
              qr.*,
              b.product_id,
              b.lot,
              p.name AS product_name
            FROM quarantine_reviews qr
            JOIN batches b ON b.id = qr.batch_id
            JOIN products p ON p.id = b.product_id
            WHERE qr.id = ?
            """,
            (review_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"quarantine_reviews#{review_id} not found")
        return dict(row)

    def _get_sensor_reading(self, connection: Connection, reading_id: int) -> dict[str, Any]:
        row = connection.execute(
            """
            SELECT
              sr.*,
              sd.name AS device_name,
              w.name AS warehouse_name
            FROM sensor_readings sr
            JOIN sensor_devices sd ON sd.id = sr.device_id
            JOIN warehouses w ON w.id = sr.warehouse_id
            WHERE sr.id = ?
            """,
            (reading_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"sensor_readings#{reading_id} not found")
        return dict(row)

    def _ensure_quarantine_review(
        self,
        connection: Connection,
        *,
        batch_id: int,
        warehouse_id: int,
        actor_id: str,
    ) -> int:
        existing = connection.execute(
            """
            SELECT id FROM quarantine_reviews
            WHERE batch_id = ? AND warehouse_id = ?
            """,
            (batch_id, warehouse_id),
        ).fetchone()
        if existing:
            return int(existing["id"])
        now = now_iso()
        return insert_and_get_id(
            connection,
            """
            INSERT INTO quarantine_reviews(
              batch_id, warehouse_id, status, responsible_id, due_at, decision_reason,
              created_by, decided_by, created_at, updated_at, decided_at
            ) VALUES (?, ?, ?, NULL, NULL, NULL, ?, NULL, ?, ?, NULL)
            """,
            (
                batch_id,
                warehouse_id,
                QuarantineReviewStatus.PENDING,
                actor_id,
                now,
                now,
            ),
        )

    def _ensure_quarantine_reviews_for_open_batches(
        self, connection: Connection, warehouse_id: int | None = None
    ) -> None:
        params: tuple[Any, ...] = ()
        warehouse_filter = ""
        if warehouse_id is not None:
            warehouse_filter = " AND sb.warehouse_id = ?"
            params = (warehouse_id,)
        rows = connection.execute(
            f"""
            SELECT b.id AS batch_id, sb.warehouse_id
            FROM stock_balances sb
            JOIN batches b ON b.id = sb.batch_id
            LEFT JOIN quarantine_reviews qr
              ON qr.batch_id = b.id AND qr.warehouse_id = sb.warehouse_id
            WHERE b.status = ?
              AND qr.id IS NULL
              AND CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL) > 0
              {warehouse_filter}
            ORDER BY b.id, sb.warehouse_id
            """,
            (BatchStatus.QUARANTINE, *params),
        ).fetchall()
        for row in rows:
            self._ensure_quarantine_review(
                connection,
                batch_id=row["batch_id"],
                warehouse_id=row["warehouse_id"],
                actor_id="system",
            )

    def _close_open_quarantine_reviews(
        self,
        connection: Connection,
        *,
        batch_id: int,
        status: QuarantineReviewStatus,
        actor_id: str,
        reason: str | None,
    ) -> None:
        now = now_iso()
        connection.execute(
            """
            UPDATE quarantine_reviews
            SET status = ?,
                decision_reason = COALESCE(?, decision_reason),
                decided_by = ?,
                updated_at = ?,
                decided_at = ?
            WHERE batch_id = ?
              AND status IN (?, ?)
            """,
            (
                status,
                reason,
                actor_id,
                now,
                now,
                batch_id,
                QuarantineReviewStatus.PENDING,
                QuarantineReviewStatus.IN_REVIEW,
            ),
        )

    def _get_by_id(self, connection: Connection, table: str, entity_id: int) -> dict[str, Any]:
        return dict(self._require(connection, table, entity_id))

    def _list_table(
        self,
        table: str,
        order_by: str,
        limit: int = 100,
        offset: int = 0,
        *,
        where: str | None = None,
        params: tuple[Any, ...] = (),
    ) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        query = f"SELECT * FROM {table}"
        if where:
            query += f" WHERE {where}"
        query += f" ORDER BY {order_by} LIMIT ? OFFSET ?"
        connection = self.database.connect()
        try:
            rows = connection.execute(query, (*params, safe_limit, safe_offset)).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def _get_batch(self, connection: Connection, batch_id: int) -> dict[str, Any]:
        row = self._require(connection, "batches", batch_id)
        return dict(row)

    def _get_document(self, connection: Connection, document_id: int) -> dict[str, Any]:
        document = dict(self._require(connection, "stock_documents", document_id))
        document["lines"] = [
            dict(row)
            for row in connection.execute(
                "SELECT * FROM stock_document_lines WHERE document_id = ? ORDER BY id",
                (document_id,),
            ).fetchall()
        ]
        return document

    def _get_inventory_session(self, connection: Connection, session_id: int) -> dict[str, Any]:
        session = dict(self._require(connection, "inventory_sessions", session_id))
        session["responsible_ids"] = [
            row["responsible_id"]
            for row in connection.execute(
                """
                SELECT responsible_id
                FROM inventory_responsibles
                WHERE session_id = ?
                ORDER BY responsible_id
                """,
                (session_id,),
            ).fetchall()
        ]
        session["category_ids"] = [
            row["category_id"]
            for row in connection.execute(
                """
                SELECT category_id
                FROM inventory_session_categories
                WHERE session_id = ?
                ORDER BY category_id
                """,
                (session_id,),
            ).fetchall()
        ]
        session["lines"] = [
            dict(row)
            for row in connection.execute(
                "SELECT * FROM inventory_lines WHERE session_id = ? ORDER BY id",
                (session_id,),
            ).fetchall()
        ]
        session["summary"] = self._inventory_summary(session["lines"])
        return session

    def _inventory_print_csv(self, lines: list[dict[str, Any]], include_actual: bool) -> str:
        headers = [
            "N",
            "Товар",
            "SKU",
            "Ед.",
            "Партия",
            "Срок годности",
            "Ожидается",
            "Факт",
        ]
        if include_actual:
            headers.append("Расхождение")
        rows = [headers]
        for line in lines:
            row = [
                line["line_no"],
                line["product_name"],
                line["sku"],
                line["unit"],
                line["lot"],
                line["expires_on"] or "",
                self._report_decimal(Decimal(str(line["expected_quantity"]))),
                "" if line["actual_quantity"] is None else self._report_decimal(Decimal(str(line["actual_quantity"]))),
            ]
            if include_actual:
                difference = line["difference_quantity"]
                row.append("" if difference is None else self._report_decimal(Decimal(str(difference))))
            rows.append(row)
        return "\n".join(";".join(self._csv_cell(cell) for cell in row) for row in rows)

    def _repack_print_csv(self, lines: list[dict[str, Any]]) -> str:
        rows: list[list[Any]] = [
            [
                "N",
                "Исходный товар",
                "Исходная партия",
                "Полученный товар",
                "Полученная партия",
                "ID полученной партии",
                "Взяли",
                "Получили",
                "Коэффициент",
                "Потери",
                "Цена результата",
                "Причина",
            ]
        ]
        for line in lines:
            target_unit_price = line["target_unit_price"]
            rows.append(
                [
                    line["line_no"],
                    line["source_product_name"],
                    line["source_lot"],
                    line["target_product_name"],
                    line["target_lot"],
                    line["target_batch_id"] or "",
                    self._report_decimal(Decimal(str(line["source_quantity"]))),
                    self._report_decimal(Decimal(str(line["target_quantity"]))),
                    self._report_decimal(Decimal(str(line["conversion_factor"]))),
                    self._report_decimal(Decimal(str(line["loss_quantity"]))),
                    "" if target_unit_price is None else self._report_decimal(Decimal(str(target_unit_price))),
                    line["reason"] or "",
                ]
            )
        return "\n".join(";".join(self._csv_cell(cell) for cell in row) for row in rows)

    def _transfer_print_csv(self, lines: list[dict[str, Any]]) -> str:
        rows: list[list[Any]] = [
            [
                "N",
                "Товар",
                "Партия",
                "Откуда",
                "Куда",
                "Количество",
                "Основание",
            ]
        ]
        for line in lines:
            rows.append(
                [
                    line["line_no"],
                    line["product_name"],
                    line["lot"],
                    line["source_warehouse_name"],
                    line["target_warehouse_name"],
                    self._report_decimal(Decimal(str(line["quantity"]))),
                    line["reason"] or "",
                ]
            )
        return "\n".join(";".join(self._csv_cell(cell) for cell in row) for row in rows)

    def _quarantine_protocol_csv(self, protocol: dict[str, Any]) -> str:
        rows: list[list[Any]] = [
            ["Поле", "Значение"],
            ["Номер проверки", protocol["review_id"]],
            ["Партия", protocol["batch_id"]],
            ["Товар", protocol["product_name"]],
            ["Серия", protocol["lot"]],
            ["Склад", protocol["warehouse_name"]],
            ["Статус", protocol["status"]],
            ["Ответственный", protocol["responsible_id"] or ""],
            ["Срок проверки", protocol["due_at"] or ""],
            ["Решение / причина", protocol["decision_reason"] or ""],
            ["Создал", protocol["created_by"]],
            ["Принял решение", protocol["decided_by"] or ""],
            ["Создано", protocol["created_at"]],
            ["Обновлено", protocol["updated_at"]],
            ["Дата решения", protocol["decided_at"] or ""],
        ]
        return "\n".join(";".join(self._csv_cell(cell) for cell in row) for row in rows)

    def _get_inventory_line(self, connection: Connection, line_id: int) -> dict[str, Any]:
        return dict(self._require(connection, "inventory_lines", line_id))

    def _inventory_summary(self, lines: list[dict[str, Any]]) -> dict[str, Any]:
        total_expected = Decimal("0")
        total_actual = Decimal("0")
        total_surplus = Decimal("0")
        total_shortage = Decimal("0")
        filled = 0
        surplus_lines = 0
        shortage_lines = 0
        matched_lines = 0
        for line in lines:
            expected = Decimal(line["expected_quantity"])
            total_expected += expected
            actual_value = line.get("actual_quantity")
            difference_value = line.get("difference_quantity")
            if actual_value is None:
                continue
            filled += 1
            actual = Decimal(actual_value)
            total_actual += actual
            difference = Decimal(difference_value) if difference_value is not None else actual - expected
            if difference > 0:
                surplus_lines += 1
                total_surplus += difference
            elif difference < 0:
                shortage_lines += 1
                total_shortage += abs(difference)
            else:
                matched_lines += 1
        return {
            "total_lines": len(lines),
            "filled_lines": filled,
            "missing_lines": max(0, len(lines) - filled),
            "surplus_lines": surplus_lines,
            "shortage_lines": shortage_lines,
            "matched_lines": matched_lines,
            "total_expected_quantity": total_expected,
            "total_actual_quantity": total_actual,
            "total_surplus_quantity": total_surplus,
            "total_shortage_quantity": total_shortage,
        }

    def _current_free_quantity(
        self, connection: Connection, product_id: int, warehouse_id: int
    ) -> Decimal:
        row = connection.execute(
            """
            SELECT COALESCE(SUM(
              CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL)
            ), 0) AS free_quantity
            FROM batches b
            LEFT JOIN stock_balances sb
              ON sb.batch_id = b.id AND sb.warehouse_id = ?
            WHERE b.product_id = ?
            """,
            (warehouse_id, product_id),
        ).fetchone()
        return Decimal(str(row["free_quantity"] or 0))

    def _balance_payload(self, row: Row) -> dict[str, Any]:
        total = Decimal(row["total_quantity"])
        reserved = Decimal(row["reserved_quantity"])
        return {
            "product_id": row["product_id"],
            "batch_id": row["batch_id"],
            "warehouse_id": row["warehouse_id"],
            "total_quantity": total,
            "reserved_quantity": reserved,
            "free_quantity": total - reserved,
            "batch_status": row["batch_status"],
            "expires_on": self._date_from_db(row["expires_on"]) if row["expires_on"] else None,
        }

    # === USERS ===

    def get_user_by_username(self, username: str):
        import json as _json
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT * FROM sklad_users WHERE username = ? AND is_active = TRUE",
                (username,)
            ).fetchone()
        finally:
            self._close_connection(connection)
        if row is None:
            return None
        return dict(row)

    def get_supplier_by_email(self, email: str):
        """Look up a supplier by login email. Only returns suppliers with
        portal access already granted (password_hash set + enabled)."""
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT * FROM suppliers WHERE email = ? AND portal_access_enabled = TRUE "
                "AND password_hash IS NOT NULL",
                (email,)
            ).fetchone()
        finally:
            self._close_connection(connection)
        if row is None:
            return None
        return dict(row)

    def set_supplier_portal_access(
        self, supplier_id: int, password_hash: str, actor_id: str = "system"
    ) -> dict[str, Any]:
        """Grant (or rotate) a supplier's portal login. Called by staff only —
        the plaintext password is generated by the route handler and never
        persisted anywhere except this hash."""
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "suppliers", supplier_id)
            if not before.get("email"):
                raise ValidationError("У поставщика не указан email — это логин для портала")
            connection.execute(
                "UPDATE suppliers SET password_hash = ?, portal_access_enabled = TRUE WHERE id = ?",
                (password_hash, supplier_id),
            )
            updated = self._get_by_id(connection, "suppliers", supplier_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "supplier",
                supplier_id,
                {"before": {"portal_access_enabled": before.get("portal_access_enabled")},
                 "after": {"portal_access_enabled": True}},
            )
        return dict(updated)

    def revoke_supplier_portal_access(self, supplier_id: int, actor_id: str = "system") -> dict[str, Any]:
        with self.database.transaction() as connection:
            before = self._get_by_id(connection, "suppliers", supplier_id)
            connection.execute(
                "UPDATE suppliers SET password_hash = NULL, portal_access_enabled = FALSE WHERE id = ?",
                (supplier_id,),
            )
            updated = self._get_by_id(connection, "suppliers", supplier_id)
            self._audit(
                connection,
                actor_id,
                AuditAction.UPDATE,
                "supplier",
                supplier_id,
                {"before": {"portal_access_enabled": before.get("portal_access_enabled")},
                 "after": {"portal_access_enabled": False}},
            )
        return dict(updated)

    def list_users(self):
        import json as _json
        connection = self.database.connect()
        try:
            rows = connection.execute(
                "SELECT id, username, full_name, roles, warehouse_ids, department, supplier_id, is_active, created_at FROM sklad_users ORDER BY id"
            ).fetchall()
        finally:
            self._close_connection(connection)
        return [dict(r) for r in rows]

    def create_user(self, username: str, full_name: str, password_hash: str, roles, warehouse_ids, department, supplier_id=None):
        import json as _json
        roles_str = ",".join(roles)
        wh_json = _json.dumps(warehouse_ids)
        with self.database.transaction() as connection:
            user_id = insert_and_get_id(
                connection,
                "INSERT INTO sklad_users (username, full_name, password_hash, roles, warehouse_ids, department, supplier_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (username, full_name, password_hash, roles_str, wh_json, department, supplier_id)
            )
            row = connection.execute(
                "SELECT id, username, full_name, roles, warehouse_ids, department, supplier_id, is_active, created_at FROM sklad_users WHERE id = ?",
                (user_id,)
            ).fetchone()
        return dict(row)

    def update_user(self, user_id: int, updates: dict):
        import json as _json
        fields = []
        params = []
        if "full_name" in updates:
            fields.append("full_name = ?")
            params.append(updates["full_name"])
        if "password_hash" in updates:
            fields.append("password_hash = ?")
            params.append(updates["password_hash"])
        if "roles" in updates:
            fields.append("roles = ?")
            params.append(",".join(updates["roles"]))
        if "warehouse_ids" in updates:
            fields.append("warehouse_ids = ?")
            params.append(_json.dumps(updates["warehouse_ids"]))
        if "department" in updates:
            fields.append("department = ?")
            params.append(updates["department"])
        if "supplier_id" in updates:
            fields.append("supplier_id = ?")
            params.append(updates["supplier_id"])
        if "is_active" in updates:
            fields.append("is_active = ?")
            params.append(updates["is_active"])
        if not fields:
            return self.get_user_by_id(user_id)
        params.append(user_id)
        with self.database.transaction() as connection:
            connection.execute(
                f"UPDATE sklad_users SET {', '.join(fields)} WHERE id = ?",
                tuple(params)
            )
            row = connection.execute(
                "SELECT id, username, full_name, roles, warehouse_ids, department, supplier_id, is_active, created_at FROM sklad_users WHERE id = ?",
                (user_id,)
            ).fetchone()
        return dict(row) if row else None

    def get_user_by_id(self, user_id: int):
        connection = self.database.connect()
        try:
            row = connection.execute(
                "SELECT id, username, full_name, roles, warehouse_ids, department, supplier_id, is_active, created_at FROM sklad_users WHERE id = ?",
                (user_id,)
            ).fetchone()
        finally:
            self._close_connection(connection)
        return dict(row) if row else None

    # === SUPPLIER MAP / SHIPMENTS ===

    def list_suppliers_with_geo(self) -> list:
        connection = self.database.connect()
        try:
            rows = connection.execute(
                "SELECT id, name, city, lat, lng, rating, delivery_days, is_preferred, phone, address FROM suppliers WHERE lat IS NOT NULL AND lng IS NOT NULL ORDER BY name"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    def create_shipment(self, data: dict) -> dict:
        fields = ["supplier_id", "reference", "status", "origin_city", "origin_lat", "origin_lng",
                  "destination_warehouse_id", "current_city", "current_lat", "current_lng", "estimated_arrival", "notes"]
        values = [data.get(f) for f in fields]
        placeholders = ", ".join("?" * len(fields))
        col_names = ", ".join(fields)
        with self.database.transaction() as conn:
            sid = insert_and_get_id(
                conn,
                f"INSERT INTO shipments ({col_names}) VALUES ({placeholders})",
                tuple(values)
            )
            row = conn.execute("SELECT * FROM shipments WHERE id = ?", (sid,)).fetchone()
        return dict(row)

    def list_shipments(self, supplier_id=None, status=None, limit=50, offset=0) -> dict:
        where = []
        params = []
        if supplier_id is not None:
            where.append("supplier_id = ?")
            params.append(supplier_id)
        if status:
            where.append("status = ?")
            params.append(status)
        where_clause = f"WHERE {' AND '.join(where)}" if where else ""
        connection = self.database.connect()
        try:
            total_row = connection.execute(f"SELECT COUNT(*) AS n FROM shipments {where_clause}", tuple(params)).fetchone()
            total = total_row["n"] if total_row else 0
            rows = connection.execute(
                f"SELECT * FROM shipments {where_clause} ORDER BY created_at DESC LIMIT ? OFFSET ?",
                tuple(params) + (limit, offset)
            ).fetchall()
            return {"items": [dict(r) for r in rows], "total": total}
        finally:
            self._close_connection(connection)

    def get_shipment(self, shipment_id: int) -> dict | None:
        connection = self.database.connect()
        try:
            row = connection.execute("SELECT * FROM shipments WHERE id = ?", (shipment_id,)).fetchone()
            return dict(row) if row else None
        finally:
            self._close_connection(connection)

    def update_shipment(self, shipment_id: int, updates: dict):
        fields = []
        params = []
        for key in ["status", "current_city", "current_lat", "current_lng", "estimated_arrival", "notes"]:
            if key in updates:
                fields.append(f"{key} = ?")
                params.append(updates[key])
        if not fields:
            return None
        fields.append("updated_at = ?")
        params.append(now_iso())
        params.append(shipment_id)
        with self.database.transaction() as conn:
            conn.execute(f"UPDATE shipments SET {", ".join(fields)} WHERE id = ?", tuple(params))
            row = conn.execute("SELECT * FROM shipments WHERE id = ?", (shipment_id,)).fetchone()
        return dict(row) if row else None

    # === REPACK TEMPLATES ===

    def create_repack_template(self, data: dict, actor_id: str) -> dict:
        with self.database.transaction() as conn:
            if data.get("target_product_id"):
                self._require(conn, "products", data["target_product_id"])
            if data.get("source_product_id"):
                self._require(conn, "products", data["source_product_id"])
            tpl_id = insert_and_get_id(
                conn,
                "INSERT INTO repack_templates"
                " (name, source_product_id, target_product_id, quantity_factor,"
                "  loss_factor, target_unit_price, reason, created_by, created_at)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    data["name"],
                    data.get("source_product_id"),
                    data["target_product_id"],
                    str(data.get("quantity_factor", "1")),
                    str(data.get("loss_factor", "0")),
                    str(data["target_unit_price"]) if data.get("target_unit_price") else None,
                    data.get("reason"),
                    actor_id,
                    now_iso(),
                ),
            )
            row = conn.execute("SELECT * FROM repack_templates WHERE id=?", (tpl_id,)).fetchone()
        return dict(row)

    def list_repack_templates(self, source_product_id: int | None = None) -> list[dict]:
        where = "WHERE rt.source_product_id = ?" if source_product_id else ""
        params: tuple = (source_product_id,) if source_product_id else ()
        with self.database.transaction() as conn:
            rows = conn.execute(
                f"SELECT rt.*,"
                f" sp.name AS source_product_name, tp.name AS target_product_name"
                f" FROM repack_templates rt"
                f" LEFT JOIN products sp ON sp.id = rt.source_product_id"
                f" LEFT JOIN products tp ON tp.id = rt.target_product_id"
                f" {where} ORDER BY rt.name, rt.id",
                params,
            ).fetchall()
        return [dict(r) for r in rows]

    def delete_repack_template(self, template_id: int, actor_id: str) -> None:
        with self.database.transaction() as conn:
            row = conn.execute("SELECT id FROM repack_templates WHERE id=?", (template_id,)).fetchone()
            if not row:
                raise ValueError(f"Repack template {template_id} not found")
            conn.execute("DELETE FROM repack_templates WHERE id=?", (template_id,))
            self._audit(conn, "repack_template.deleted", actor_id=actor_id,
                        payload={"template_id": template_id})

    def count_mis_mapped_warehouses(self) -> int:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS c FROM warehouses"
                " WHERE mis_clinic_id IS NOT NULL AND mis_room_id IS NOT NULL"
            ).fetchone()
            return int(row["c"])

    def list_warehouse_ids_by_mis_clinic(self, mis_clinic_id: str) -> list[int]:
        """All sklad warehouses mapped to a given MIS clinic (any room), for SSO scoping."""
        connection = self.database.connect()
        try:
            rows = connection.execute(
                "SELECT id FROM warehouses WHERE mis_clinic_id = ?", (mis_clinic_id,)
            ).fetchall()
            return [row["id"] for row in rows]
        finally:
            self._close_connection(connection)

    # === MIS PROCEDURE CONSUMPTION TEMPLATES ===

    def create_procedure_consumption_template(self, data: dict, actor_id: str) -> dict:
        items = data.get("items") or []
        if not items:
            raise ValidationError("Template must contain at least one item")
        with self.database.transaction() as conn:
            for item in items:
                self._require(conn, "products", item["product_id"])
            tpl_id = insert_and_get_id(
                conn,
                "INSERT INTO procedure_consumption_templates"
                " (mis_clinic_id, service_code, name, created_by, created_at)"
                " VALUES (?,?,?,?,?)",
                (
                    data["mis_clinic_id"],
                    data["service_code"],
                    data["name"],
                    actor_id,
                    now_iso(),
                ),
            )
            for item in items:
                conn.execute(
                    "INSERT INTO procedure_consumption_items (template_id, product_id, quantity)"
                    " VALUES (?,?,?)",
                    (tpl_id, item["product_id"], str(item["quantity"])),
                )
            self._audit(
                conn, actor_id, AuditAction.CREATE, "procedure_consumption_template", tpl_id, data
            )
            return self._get_procedure_consumption_template(conn, tpl_id)

    def _get_procedure_consumption_template(self, conn: Connection, template_id: int) -> dict:
        row = conn.execute(
            "SELECT * FROM procedure_consumption_templates WHERE id=?", (template_id,)
        ).fetchone()
        if not row:
            raise NotFoundError(f"Procedure consumption template {template_id} not found")
        tpl = dict(row)
        tpl["created_at"] = str(tpl["created_at"])
        item_rows = conn.execute(
            "SELECT pci.id, pci.product_id, pci.quantity, p.name AS product_name"
            " FROM procedure_consumption_items pci"
            " JOIN products p ON p.id = pci.product_id"
            " WHERE pci.template_id=? ORDER BY pci.id",
            (template_id,),
        ).fetchall()
        items = [dict(r) for r in item_rows]
        for item in items:
            item["quantity"] = str(item["quantity"])
        tpl["items"] = items
        return tpl

    def list_procedure_consumption_templates(self, mis_clinic_id: str | None = None) -> list[dict]:
        where = "WHERE mis_clinic_id = ?" if mis_clinic_id else ""
        params: tuple = (mis_clinic_id,) if mis_clinic_id else ()
        with self.database.transaction() as conn:
            rows = conn.execute(
                f"SELECT id FROM procedure_consumption_templates {where}"
                f" ORDER BY mis_clinic_id, service_code",
                params,
            ).fetchall()
            return [self._get_procedure_consumption_template(conn, row["id"]) for row in rows]

    def delete_procedure_consumption_template(self, template_id: int, actor_id: str) -> None:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT id FROM procedure_consumption_templates WHERE id=?", (template_id,)
            ).fetchone()
            if not row:
                raise ValueError(f"Procedure consumption template {template_id} not found")
            conn.execute("DELETE FROM procedure_consumption_items WHERE template_id=?", (template_id,))
            conn.execute("DELETE FROM procedure_consumption_templates WHERE id=?", (template_id,))
            self._audit(
                conn,
                actor_id,
                AuditAction.DELETE,
                "procedure_consumption_template",
                template_id,
                {"template_id": template_id},
            )

    # === MIS PROCEDURE EVENTS ===

    def process_mis_procedure_event(
        self,
        *,
        mis_clinic_id: str,
        mis_room_id: str,
        service_code: str,
        mis_event_id: str,
        patient_id: str | None = None,
        doctor_id: str | None = None,
        medical_record_no: str | None = None,
        actor_id: str = "mis-integration",
    ) -> dict:
        with self.database.transaction() as conn:
            already = conn.execute(
                "SELECT id FROM mis_processed_events WHERE mis_event_id = ?", (mis_event_id,)
            ).fetchone()
            if already:
                return {"status": "already_processed", "mis_event_id": mis_event_id, "write_offs": []}

            warehouse = conn.execute(
                "SELECT id FROM warehouses WHERE mis_clinic_id = ? AND mis_room_id = ?",
                (mis_clinic_id, mis_room_id),
            ).fetchone()
            if not warehouse:
                raise NotFoundError(
                    f"Кабинет (clinic={mis_clinic_id}, room={mis_room_id}) "
                    f"не сопоставлен со складом в sklad"
                )
            warehouse_id = warehouse["id"]

            template = conn.execute(
                "SELECT id FROM procedure_consumption_templates"
                " WHERE mis_clinic_id = ? AND service_code = ?",
                (mis_clinic_id, service_code),
            ).fetchone()
            if not template:
                raise NotFoundError(f"Расход для процедуры «{service_code}» не настроен")
            items = conn.execute(
                "SELECT product_id, quantity FROM procedure_consumption_items WHERE template_id = ?",
                (template["id"],),
            ).fetchall()
            if not items:
                raise ValidationError(f"Шаблон расхода для процедуры «{service_code}» пуст")

            write_offs = [
                self._write_off_fefo_within(
                    conn,
                    actor_id=actor_id,
                    product_id=item["product_id"],
                    warehouse_id=warehouse_id,
                    quantity=Decimal(str(item["quantity"])),
                    reason=f"МИС: процедура {service_code}",
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    medical_record_no=medical_record_no,
                )
                for item in items
            ]

            conn.execute(
                "INSERT INTO mis_processed_events (mis_event_id, created_at) VALUES (?, ?)",
                (mis_event_id, now_iso()),
            )

            return {
                "status": "processed",
                "mis_event_id": mis_event_id,
                "warehouse_id": warehouse_id,
                "write_offs": write_offs,
            }

    # === AUCTIONS ===

    def create_auction(self, data: dict, actor_id: str) -> dict:
        with self.database.transaction() as conn:
            sql = (
                "INSERT INTO auctions (title, description, product_id, warehouse_id, quantity, unit,"
                " start_price, current_price, min_price, step_amount, step_interval_seconds,"
                " status, created_by, created_at, starts_at)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,'draft',?,?,?)"
            )
            auction_id = insert_and_get_id(conn, sql, (
                data["title"], data.get("description"), data["product_id"], data["warehouse_id"],
                str(data["quantity"]), data.get("unit", "шт"), str(data["start_price"]),
                str(data["start_price"]), str(data["min_price"]), str(data.get("step_amount", "100")),
                data.get("step_interval_seconds", 300), actor_id, now_iso(), data.get("starts_at"),
            ))
            row = conn.execute("SELECT * FROM auctions WHERE id = ?", (auction_id,)).fetchone()
        return dict(row)

    def list_auctions(self, status: str | None = None, limit: int = 20, offset: int = 0) -> dict:
        where = "WHERE a.status = ?" if status else ""
        params: tuple = (status,) if status else ()
        with self.database.transaction() as conn:
            total = conn.execute(f"SELECT COUNT(*) as n FROM auctions a {where}", params).fetchone()["n"]
            rows = conn.execute(
                f"SELECT a.*, p.name as product_name,"
                f" (SELECT COUNT(*) FROM auction_bids b WHERE b.auction_id = a.id) as bid_count"
                f" FROM auctions a LEFT JOIN products p ON p.id = a.product_id"
                f" {where} ORDER BY a.created_at DESC LIMIT ? OFFSET ?",
                params + (limit, offset)
            ).fetchall()
        return {"items": [dict(r) for r in rows], "total": total}

    def get_auction(self, auction_id: int) -> dict | None:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT a.*, p.name as product_name,"
                " (SELECT COUNT(*) FROM auction_bids b WHERE b.auction_id = a.id) as bid_count"
                " FROM auctions a LEFT JOIN products p ON p.id = a.product_id WHERE a.id = ?",
                (auction_id,)
            ).fetchone()
        return dict(row) if row else None

    def start_auction(self, auction_id: int) -> dict | None:
        with self.database.transaction() as conn:
            _now = now_iso()
            conn.execute(
                "UPDATE auctions SET status='active', starts_at=?"
                " WHERE id = ? AND status='draft'",
                (_now, auction_id)
            )
            row = conn.execute("SELECT * FROM auctions WHERE id = ?", (auction_id,)).fetchone()
        return dict(row) if row else None

    def place_bid(self, auction_id: int, supplier_id: int, bid_amount: float) -> dict:
        with self.database.transaction() as conn:
            auction = conn.execute(
                "SELECT * FROM auctions WHERE id = ? AND status = 'active'", (auction_id,)
            ).fetchone()
            if not auction:
                raise ValueError("Auction not active")
            if bid_amount >= float(auction["current_price"]):
                raise ValueError(f"Ставка должна быть ниже текущей цены {auction['current_price']}")
            if bid_amount < float(auction["min_price"]):
                raise ValueError(f"Ставка не может быть ниже минимальной {auction['min_price']}")
            bid_id = insert_and_get_id(
                conn,
                "INSERT INTO auction_bids (auction_id, supplier_id, bid_amount) VALUES (?,?,?)",
                (auction_id, supplier_id, str(bid_amount))
            )
            conn.execute(
                "UPDATE auctions SET current_price=?, winner_supplier_id=?, winner_bid=? WHERE id=?",
                (str(bid_amount), supplier_id, str(bid_amount), auction_id)
            )
            row = conn.execute("SELECT * FROM auction_bids WHERE id=?", (bid_id,)).fetchone()
        return dict(row)

    def close_auction(self, auction_id: int) -> dict | None:
        with self.database.transaction() as conn:
            cur = conn.execute(
                "UPDATE auctions SET status='closed', ends_at=? WHERE id=? AND status='active'",
                (now_iso(), auction_id)
            )
            if cur.rowcount == 0:
                return None
            row = conn.execute("SELECT * FROM auctions WHERE id=?", (auction_id,)).fetchone()
        return dict(row) if row else None

    def list_auction_bids(self, auction_id: int) -> list[dict]:
        with self.database.transaction() as conn:
            rows = conn.execute(
                "SELECT b.*, s.name as supplier_name FROM auction_bids b"
                " LEFT JOIN suppliers s ON s.id = b.supplier_id"
                " WHERE b.auction_id=? ORDER BY b.bid_amount ASC",
                (auction_id,)
            ).fetchall()
        return [dict(r) for r in rows]



    def _fire_accounting_webhook(self, purchase_request):
        """Fire outbound webhook to accounting service when purchase request is ordered."""
        try:
            from app.core.config import get_settings
            settings = get_settings()
            url = settings.accounting_webhook_url
            if not url:
                return
            import urllib.request as _urllib
            payload = json.dumps({
                "event": "purchase_request.ordered",
                "id": purchase_request.get("id"),
                "warehouse_id": purchase_request.get("warehouse_id"),
                "product_id": purchase_request.get("product_id"),
                "recommended_quantity": str(purchase_request.get("recommended_quantity") or 0),
                "reason": purchase_request.get("reason"),
                "created_at": str(purchase_request.get("created_at")),
            }).encode()
            headers = {"Content-Type": "application/json"}
            secret = settings.accounting_webhook_secret
            if secret:
                import hmac as _hmac, hashlib as _hashlib
                sig = _hmac.new(secret.encode(), payload, _hashlib.sha256).hexdigest()
                headers["X-Sklad-Signature"] = sig
            def _send():
                try:
                    req = _urllib.Request(url, data=payload, headers=headers, method="POST")
                    _urllib.urlopen(req, timeout=10)
                except Exception as exc:
                    import logging
                    logging.getLogger(__name__).warning("Accounting webhook failed: %s", exc)
            threading.Thread(target=_send, daemon=True).start()
        except Exception:
            pass
    def _check_and_create_reorder_requests(self, connection, warehouse_id, product_ids):
        if not product_ids:
            return
        placeholders = ",".join("?" * len(product_ids))
        qsql = (
            "SELECT p.id AS product_id, p.name AS product_name, p.reorder_point, p.safety_stock,"
            " COALESCE(SUM(CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL)), 0) AS free_quantity"
            " FROM products p"
            " LEFT JOIN batches b ON b.product_id = p.id"
            " LEFT JOIN stock_balances sb ON sb.batch_id = b.id AND sb.warehouse_id = ?"
            f" WHERE p.id IN ({placeholders})"
            " GROUP BY p.id, p.name, p.reorder_point, p.safety_stock"
            " HAVING CAST(p.reorder_point AS REAL) > 0"
            " AND COALESCE(SUM(CAST(sb.quantity AS REAL) - CAST(sb.reserved_quantity AS REAL)), 0) < CAST(p.reorder_point AS REAL)"
        )
        rows = connection.execute(qsql, (warehouse_id, *product_ids)).fetchall()
        for row in rows:
            existing = connection.execute("SELECT id FROM purchase_requests WHERE warehouse_id = ? AND product_id = ? AND status = 'draft'", (warehouse_id, row["product_id"])).fetchone()
            if existing:
                continue
            current_free = Decimal(str(row["free_quantity"] or 0))
            reorder_point = Decimal(str(row["reorder_point"] or 0))
            safety_stock = Decimal(str(row["safety_stock"] or 0))
            rec_qty = max(Decimal("0"), reorder_point + safety_stock - current_free)
            if self._is_postgresql(connection):
                req_id = self._insert_purchase_request_if_absent_postgresql(connection, warehouse_id=warehouse_id, product_id=row["product_id"], current_free=current_free, reorder_point=reorder_point, safety_stock=safety_stock, recommended_quantity=rec_qty, reason="Ниже точки заказа (авто)", actor_id="system")
            else:
                req_id = insert_and_get_id(connection, "INSERT INTO purchase_requests(warehouse_id, product_id, status, current_free_quantity, reorder_point, safety_stock, recommended_quantity, reason, source, created_by, created_at) VALUES (?, ?, 'draft', ?, ?, ?, ?, ?, 'auto', 'system', ?)", (warehouse_id, row["product_id"], self._report_decimal(current_free), self._report_decimal(reorder_point), self._report_decimal(safety_stock), self._report_decimal(rec_qty), "Ниже точки заказа (авто)", now_iso()))
            if not req_id:
                continue
            product_name = row["product_name"]
            msg = f"Автозаявка: {product_name} (остаток {float(current_free):.3f}, точка {float(reorder_point):.3f})"
            existing_notif = connection.execute("SELECT id FROM notifications WHERE notification_type = 'low_stock' AND product_id = ? AND warehouse_id = ? AND is_read = 0", (row["product_id"], warehouse_id)).fetchone()
            if not existing_notif:
                insert_and_get_id(connection, "INSERT INTO notifications(notification_type, warehouse_id, product_id, title, message, is_read, created_at) VALUES (?, ?, ?, ?, ?, 0, ?)", ('low_stock', warehouse_id, row["product_id"], "Сформирована автозаявка", msg, now_iso()))

    def list_all_supplier_reviews(self, status: str | None = None) -> list[dict]:
        connection = self.database.connect()
        try:
            q = "SELECT * FROM supplier_reviews"
            params: list = []
            if status:
                q += " WHERE status = ?"
                params.append(status)
            q += " ORDER BY created_at DESC LIMIT 200"
            rows = connection.execute(q, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            self._close_connection(connection)

    # ── Service marketplace (repair/cleaning/logistics/consulting) ─────────────

    def _service_catalog_select(self) -> str:
        return """
            SELECT sc.*, s.name AS supplier_name
            FROM supplier_catalog sc
            JOIN suppliers s ON s.id = sc.supplier_id
        """

    def list_service_catalog(
        self,
        supplier_id: int,
        item_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        connection = self.database.connect()
        try:
            filters = ["sc.supplier_id = ?"]
            params: tuple[Any, ...] = (supplier_id,)
            if item_type is not None:
                filters.append("sc.type = ?")
                params = (*params, item_type)
            rows = connection.execute(
                f"""
                {self._service_catalog_select()}
                WHERE {" AND ".join(filters)}
                ORDER BY sc.created_at DESC, sc.id DESC
                LIMIT ? OFFSET ?
                """,
                (*params, limit, offset),
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_service_catalog(self, supplier_id: int, item_type: str | None = None) -> int:
        connection = self.database.connect()
        try:
            filters = ["supplier_id = ?"]
            params: tuple[Any, ...] = (supplier_id,)
            if item_type is not None:
                filters.append("type = ?")
                params = (*params, item_type)
            row = connection.execute(
                f"SELECT COUNT(*) AS n FROM supplier_catalog WHERE {' AND '.join(filters)}",
                params,
            ).fetchone()
            return int(row["n"]) if row else 0
        finally:
            self._close_connection(connection)

    def create_service_catalog_item(
        self, supplier_id: int, actor_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        with self.database.transaction() as connection:
            now = now_iso()
            item_id = insert_and_get_id(
                connection,
                """
                INSERT INTO supplier_catalog
                  (supplier_id, actor_id, type, title, description, price,
                   price_type, unit, service_category, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    supplier_id,
                    actor_id,
                    data.get("type", "service"),
                    data["title"],
                    data.get("description"),
                    data.get("price"),
                    data.get("price_type", "negotiable"),
                    data.get("unit"),
                    data.get("service_category") or None,
                    now,
                    now,
                ),
            )
            row = connection.execute(
                f"{self._service_catalog_select()} WHERE sc.id = ?",
                (item_id,),
            ).fetchone()
            return dict(row) if row else {}

    def update_service_catalog_item(
        self, item_id: int, supplier_id: int, data: dict[str, Any]
    ) -> dict[str, Any] | None:
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT id FROM supplier_catalog WHERE id = ? AND supplier_id = ?",
                (item_id, supplier_id),
            ).fetchone()
            if row is None:
                return None
            now = now_iso()
            connection.execute(
                """
                UPDATE supplier_catalog
                SET type = ?, title = ?, description = ?, price = ?,
                    price_type = ?, unit = ?, service_category = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    data.get("type", "service"),
                    data["title"],
                    data.get("description"),
                    data.get("price"),
                    data.get("price_type", "negotiable"),
                    data.get("unit"),
                    data.get("service_category") or None,
                    now,
                    item_id,
                ),
            )
            updated = connection.execute(
                f"{self._service_catalog_select()} WHERE sc.id = ?",
                (item_id,),
            ).fetchone()
            return dict(updated) if updated else None

    def delete_service_catalog_item(self, item_id: int, supplier_id: int) -> bool:
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT id FROM supplier_catalog WHERE id = ? AND supplier_id = ?",
                (item_id, supplier_id),
            ).fetchone()
            if row is None:
                return False
            connection.execute(
                "UPDATE supplier_catalog SET is_active = 0, updated_at = ? WHERE id = ?",
                (now_iso(), item_id),
            )
            return True

    def set_service_catalog_item_image(
        self, item_id: int, supplier_id: int, file_id: str
    ) -> dict[str, Any] | None:
        with self.database.transaction() as connection:
            row = connection.execute(
                "SELECT id FROM supplier_catalog WHERE id = ? AND supplier_id = ? AND is_active = 1",
                (item_id, supplier_id),
            ).fetchone()
            if row is None:
                return None
            connection.execute(
                "UPDATE supplier_catalog SET image_file_id = ?, updated_at = ? WHERE id = ?",
                (file_id, now_iso(), item_id),
            )
            updated = connection.execute(
                f"{self._service_catalog_select()} WHERE sc.id = ?",
                (item_id,),
            ).fetchone()
            return dict(updated) if updated else None

    def list_service_marketplace(
        self,
        item_type: str | None = None,
        service_category: str | None = None,
        supplier_id: int | None = None,
        q: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        connection = self.database.connect()
        try:
            filters = ["sc.is_active = 1"]
            params: tuple[Any, ...] = ()
            if item_type is not None:
                filters.append("sc.type = ?")
                params = (*params, item_type)
            if service_category is not None:
                filters.append("sc.service_category = ?")
                params = (*params, service_category)
            if supplier_id is not None:
                filters.append("sc.supplier_id = ?")
                params = (*params, supplier_id)
            if q:
                filters.append("(sc.title ILIKE ? OR sc.description ILIKE ?)")
                like = f"%{q}%"
                params = (*params, like, like)
            rows = connection.execute(
                f"""
                {self._service_catalog_select()}
                WHERE {" AND ".join(filters)}
                ORDER BY sc.created_at DESC, sc.id DESC
                LIMIT ? OFFSET ?
                """,
                (*params, limit, offset),
            ).fetchall()
            return [dict(row) for row in rows]
        finally:
            self._close_connection(connection)

    def count_service_marketplace(
        self,
        item_type: str | None = None,
        service_category: str | None = None,
        supplier_id: int | None = None,
        q: str | None = None,
    ) -> int:
        connection = self.database.connect()
        try:
            filters = ["sc.is_active = 1"]
            params: tuple[Any, ...] = ()
            if item_type is not None:
                filters.append("sc.type = ?")
                params = (*params, item_type)
            if service_category is not None:
                filters.append("sc.service_category = ?")
                params = (*params, service_category)
            if supplier_id is not None:
                filters.append("sc.supplier_id = ?")
                params = (*params, supplier_id)
            if q:
                filters.append("(sc.title ILIKE ? OR sc.description ILIKE ?)")
                like = f"%{q}%"
                params = (*params, like, like)
            row = connection.execute(
                f"SELECT COUNT(*) AS n FROM supplier_catalog sc WHERE {' AND '.join(filters)}",
                params,
            ).fetchone()
            return int(row["n"]) if row else 0
        finally:
            self._close_connection(connection)
