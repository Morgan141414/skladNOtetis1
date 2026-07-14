from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterator


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS suppliers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  bin TEXT,
  phone TEXT,
  address TEXT,
  rating INTEGER,
  is_preferred INTEGER NOT NULL DEFAULT 0,
  contact_person TEXT,
  email TEXT,
  contract_number TEXT,
  contract_expires_on TEXT,
  payment_terms TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS supplier_applications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actor_id TEXT NOT NULL,
  supplier_id INTEGER REFERENCES suppliers(id),
  status TEXT NOT NULL,
  name TEXT NOT NULL,
  bin TEXT,
  phone TEXT,
  email TEXT NOT NULL,
  contact_person TEXT,
  address TEXT,
  city TEXT,
  delivery_days INTEGER,
  notes TEXT,
  review_reason TEXT,
  submitted_at TEXT NOT NULL,
  reviewed_by TEXT,
  reviewed_at TEXT
);

CREATE TABLE IF NOT EXISTS warehouses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  department TEXT,
  inventory_lock INTEGER NOT NULL DEFAULT 0,
  tetis_org_id TEXT,
  external_tetis_id TEXT,
  mis_clinic_id TEXT,
  mis_room_id TEXT,
  storage_zone TEXT,
  capacity_limit TEXT,
  storage_conditions TEXT,
  responsible_person TEXT
);

CREATE TABLE IF NOT EXISTS sensor_devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  name TEXT NOT NULL,
  serial_number TEXT,
  sensor_type TEXT NOT NULL DEFAULT 'temperature_humidity',
  min_temperature_c TEXT,
  max_temperature_c TEXT,
  min_humidity_percent TEXT,
  max_humidity_percent TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sensor_readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER NOT NULL REFERENCES sensor_devices(id),
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  temperature_c TEXT,
  humidity_percent TEXT,
  recorded_at TEXT NOT NULL,
  received_at TEXT NOT NULL,
  status TEXT NOT NULL,
  raw_payload TEXT
);

CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  sku TEXT NOT NULL UNIQUE,
  unit TEXT NOT NULL,
  category_id INTEGER NOT NULL REFERENCES categories(id),
  reorder_point TEXT NOT NULL DEFAULT '0',
  safety_stock TEXT NOT NULL DEFAULT '0',
  is_controlled INTEGER NOT NULL DEFAULT 0,
  barcode TEXT,
  description TEXT,
  certificate_ref TEXT,
  is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS batches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL REFERENCES products(id),
  supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  received_at TEXT NOT NULL,
  lot TEXT NOT NULL,
  serial_number TEXT,
  expires_on TEXT,
  unit_price TEXT NOT NULL,
  status TEXT NOT NULL,
  UNIQUE(product_id, supplier_id, received_at, lot)
);

CREATE TABLE IF NOT EXISTS quarantine_reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  batch_id INTEGER NOT NULL REFERENCES batches(id),
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  status TEXT NOT NULL,
  responsible_id TEXT,
  due_at TEXT,
  decision_reason TEXT,
  created_by TEXT NOT NULL,
  decided_by TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  decided_at TEXT,
  UNIQUE(batch_id, warehouse_id)
);

CREATE TABLE IF NOT EXISTS stock_balances (
  batch_id INTEGER NOT NULL REFERENCES batches(id),
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  quantity TEXT NOT NULL,
  reserved_quantity TEXT NOT NULL DEFAULT '0',
  PRIMARY KEY(batch_id, warehouse_id)
);

CREATE TABLE IF NOT EXISTS stock_movements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  movement_type TEXT NOT NULL,
  batch_id INTEGER NOT NULL REFERENCES batches(id),
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  quantity TEXT NOT NULL,
  reason TEXT,
  patient_id TEXT,
  doctor_id TEXT,
  medical_record_no TEXT,
  second_approver_id TEXT,
  second_approval_note TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  document_type TEXT NOT NULL,
  status TEXT NOT NULL,
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  supplier_id INTEGER REFERENCES suppliers(id),
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL,
  approved_by TEXT,
  approved_at TEXT,
  posted_at TEXT
);

CREATE TABLE IF NOT EXISTS stock_document_lines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  document_id INTEGER NOT NULL REFERENCES stock_documents(id) ON DELETE CASCADE,
  product_id INTEGER REFERENCES products(id),
  batch_id INTEGER REFERENCES batches(id),
  target_warehouse_id INTEGER REFERENCES warehouses(id),
  target_product_id INTEGER REFERENCES products(id),
  quantity TEXT NOT NULL,
  target_quantity TEXT,
  conversion_factor TEXT,
  loss_quantity TEXT,
  unit_price TEXT,
  target_unit_price TEXT,
  lot TEXT,
  serial_number TEXT,
  target_lot TEXT,
  expires_on TEXT,
  target_expires_on TEXT,
  quarantine INTEGER NOT NULL DEFAULT 0,
  reason TEXT,
  patient_id TEXT,
  doctor_id TEXT,
  medical_record_no TEXT,
  second_approver_id TEXT,
  second_approval_note TEXT
);

CREATE TABLE IF NOT EXISTS reservations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  batch_id INTEGER NOT NULL REFERENCES batches(id),
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  quantity TEXT NOT NULL,
  reserved_for TEXT NOT NULL,
  status TEXT NOT NULL,
  expires_at TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  status TEXT NOT NULL,
  started_by TEXT NOT NULL,
  posted_by TEXT,
  started_at TEXT NOT NULL,
  posted_at TEXT,
  cancelled_at TEXT
);

CREATE TABLE IF NOT EXISTS inventory_lines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES inventory_sessions(id) ON DELETE CASCADE,
  product_id INTEGER NOT NULL REFERENCES products(id),
  batch_id INTEGER NOT NULL REFERENCES batches(id),
  expected_quantity TEXT NOT NULL,
  actual_quantity TEXT,
  difference_quantity TEXT,
  UNIQUE(session_id, batch_id)
);

CREATE TABLE IF NOT EXISTS inventory_responsibles (
  session_id INTEGER NOT NULL REFERENCES inventory_sessions(id) ON DELETE CASCADE,
  responsible_id TEXT NOT NULL,
  PRIMARY KEY(session_id, responsible_id)
);

CREATE TABLE IF NOT EXISTS inventory_session_categories (
  session_id INTEGER NOT NULL REFERENCES inventory_sessions(id) ON DELETE CASCADE,
  category_id INTEGER NOT NULL REFERENCES categories(id),
  PRIMARY KEY(session_id, category_id)
);

CREATE TABLE IF NOT EXISTS supplier_price_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  product_id INTEGER NOT NULL REFERENCES products(id),
  batch_id INTEGER REFERENCES batches(id),
  lot TEXT,
  unit_price TEXT NOT NULL,
  source TEXT NOT NULL,
  recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actor_id TEXT NOT NULL,
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  warehouse_id INTEGER REFERENCES warehouses(id),
  payload TEXT NOT NULL,
  created_at TEXT NOT NULL,
  request_id TEXT,
  ip_address TEXT,
  user_agent TEXT
);

CREATE TABLE IF NOT EXISTS notifications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  notification_type TEXT NOT NULL,
  product_id INTEGER REFERENCES products(id),
  batch_id INTEGER REFERENCES batches(id),
  device_id INTEGER REFERENCES sensor_devices(id),
  sensor_reading_id INTEGER REFERENCES sensor_readings(id),
  warehouse_id INTEGER REFERENCES warehouses(id),
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  is_read INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  read_at TEXT
);

CREATE TABLE IF NOT EXISTS batch_recalls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  batch_id INTEGER NOT NULL REFERENCES batches(id),
  product_id INTEGER NOT NULL REFERENCES products(id),
  reason TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT 'manual',
  reference TEXT,
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS purchase_requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  product_id INTEGER NOT NULL REFERENCES products(id),
  status TEXT NOT NULL,
  current_free_quantity TEXT NOT NULL,
  reorder_point TEXT NOT NULL,
  safety_stock TEXT NOT NULL DEFAULT '0',
  recommended_quantity TEXT NOT NULL,
  reason TEXT,
  source TEXT NOT NULL DEFAULT 'auto',
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS abc_xyz_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  warehouse_id INTEGER REFERENCES warehouses(id),
  analysis_days INTEGER NOT NULL,
  period_start TEXT NOT NULL,
  period_end TEXT NOT NULL,
  source TEXT NOT NULL,
  status TEXT NOT NULL,
  items_count INTEGER NOT NULL DEFAULT 0,
  error TEXT,
  generated_by TEXT NOT NULL,
  generated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS abc_xyz_run_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id INTEGER NOT NULL REFERENCES abc_xyz_runs(id) ON DELETE CASCADE,
  product_id INTEGER NOT NULL REFERENCES products(id),
  product_name TEXT NOT NULL,
  sku TEXT NOT NULL,
  abc_class TEXT NOT NULL,
  xyz_class TEXT NOT NULL,
  consumption_quantity TEXT NOT NULL,
  consumption_value TEXT NOT NULL,
  current_free_quantity TEXT NOT NULL,
  reorder_point TEXT NOT NULL,
  safety_stock TEXT NOT NULL,
  recommended_order_quantity TEXT NOT NULL,
  recommendation TEXT NOT NULL,
  movement_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT NOT NULL,
  actor_id TEXT NOT NULL,
  method TEXT NOT NULL,
  path TEXT NOT NULL,
  request_hash TEXT NOT NULL,
  status TEXT NOT NULL,
  response_status INTEGER,
  response_body TEXT,
  resource_type TEXT,
  resource_id TEXT,
  created_at TEXT NOT NULL,
  locked_at TEXT,
  expires_at TEXT,
  UNIQUE(actor_id, key)
);

CREATE TABLE IF NOT EXISTS marketplace_favorites (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actor_id TEXT NOT NULL,
  catalog_item_id INTEGER NOT NULL REFERENCES supplier_catalog_items(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(actor_id, catalog_item_id)
);

CREATE INDEX IF NOT EXISTS idx_mf_actor ON marketplace_favorites(actor_id);
CREATE INDEX IF NOT EXISTS idx_mf_item ON marketplace_favorites(catalog_item_id);

CREATE TABLE IF NOT EXISTS marketplace_refund_requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL REFERENCES marketplace_orders(id) ON DELETE CASCADE,
  payment_id INTEGER REFERENCES marketplace_payments(id) ON DELETE SET NULL,
  actor_id TEXT NOT NULL,
  supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  amount TEXT NOT NULL,
  currency TEXT NOT NULL DEFAULT 'KZT',
  reason TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'requested',
  reviewer_id TEXT,
  review_reason TEXT,
  reviewed_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_mrr_order ON marketplace_refund_requests(order_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mrr_actor ON marketplace_refund_requests(actor_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mrr_supplier_status ON marketplace_refund_requests(supplier_id, status, created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS uq_mrr_active_order
  ON marketplace_refund_requests(order_id)
  WHERE status IN ('requested','approved','processing');

CREATE INDEX IF NOT EXISTS idx_notifications_warehouse_read
  ON notifications(warehouse_id, is_read, created_at DESC, id DESC);

DROP INDEX IF EXISTS uq_notifications_unread_low_stock_product;

CREATE UNIQUE INDEX IF NOT EXISTS uq_notifications_unread_low_stock_warehouse_product
  ON notifications(warehouse_id, product_id)
  WHERE notification_type = 'low_stock' AND is_read = 0;

CREATE INDEX IF NOT EXISTS idx_audit_log_warehouse_created
  ON audit_log(warehouse_id, created_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_purchase_requests_warehouse_status_created
  ON purchase_requests(warehouse_id, status, created_at DESC, id DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uq_purchase_requests_open_draft_product_warehouse
  ON purchase_requests(warehouse_id, product_id)
  WHERE status = 'draft';

CREATE INDEX IF NOT EXISTS idx_sensor_devices_warehouse
  ON sensor_devices(warehouse_id, id);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_warehouse_recorded
  ON sensor_readings(warehouse_id, recorded_at DESC, id DESC);

CREATE INDEX IF NOT EXISTS idx_sensor_readings_device_recorded
  ON sensor_readings(device_id, recorded_at DESC, id DESC);

CREATE TABLE IF NOT EXISTS repack_templates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  source_product_id INTEGER REFERENCES products(id),
  target_product_id INTEGER NOT NULL REFERENCES products(id),
  quantity_factor TEXT NOT NULL DEFAULT '1',
  loss_factor TEXT NOT NULL DEFAULT '0',
  target_unit_price TEXT,
  reason TEXT,
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS procedure_consumption_templates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mis_clinic_id TEXT NOT NULL,
  service_code TEXT NOT NULL,
  name TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE (mis_clinic_id, service_code)
);

CREATE TABLE IF NOT EXISTS procedure_consumption_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  template_id INTEGER NOT NULL REFERENCES procedure_consumption_templates(id),
  product_id INTEGER NOT NULL REFERENCES products(id),
  quantity TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_procedure_consumption_items_template
  ON procedure_consumption_items(template_id);

CREATE TABLE IF NOT EXISTS mis_processed_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mis_event_id TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS auctions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  product_id INTEGER NOT NULL REFERENCES products(id),
  warehouse_id INTEGER NOT NULL,
  quantity TEXT NOT NULL,
  unit TEXT NOT NULL DEFAULT 'шт',
  start_price TEXT NOT NULL,
  current_price TEXT NOT NULL,
  min_price TEXT NOT NULL,
  step_amount TEXT NOT NULL DEFAULT '100',
  step_interval_seconds INTEGER NOT NULL DEFAULT 300,
  status TEXT NOT NULL DEFAULT 'draft',
  winner_supplier_id INTEGER REFERENCES suppliers(id),
  winner_bid TEXT,
  starts_at TEXT,
  ends_at TEXT,
  next_step_at TEXT,
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS auction_bids (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  auction_id INTEGER NOT NULL REFERENCES auctions(id),
  supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  bid_amount TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_auction_bids_auction ON auction_bids(auction_id);
"""


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def decimal_to_db(value: Decimal | int | str) -> str:
    return str(Decimal(value))


class SQLiteDatabase:
    def __init__(self, path: str | Path = "sklad.db") -> None:
        self.path = ":memory:" if str(path) == ":memory:" else str(Path(path))
        self._memory_connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if self.path == ":memory:":
            if self._memory_connection is None:
                self._memory_connection = self._new_connection()
            return self._memory_connection
        return self._new_connection()

    def _new_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def init_schema(self) -> None:
        with self.transaction() as connection:
            connection.executescript(SCHEMA)
            self._ensure_column(connection, "warehouses", "tetis_org_id", "TEXT")
            self._ensure_column(connection, "warehouses", "external_tetis_id", "TEXT")
            self._ensure_column(connection, "warehouses", "storage_zone", "TEXT")
            self._ensure_column(connection, "warehouses", "capacity_limit", "TEXT")
            self._ensure_column(connection, "warehouses", "storage_conditions", "TEXT")
            self._ensure_column(connection, "warehouses", "responsible_person", "TEXT")
            self._ensure_column(connection, "suppliers", "address", "TEXT")
            self._ensure_column(connection, "suppliers", "rating", "INTEGER")
            self._ensure_column(connection, "suppliers", "is_preferred", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_column(connection, "suppliers", "contact_person", "TEXT")
            self._ensure_column(connection, "suppliers", "email", "TEXT")
            self._ensure_column(connection, "suppliers", "contract_number", "TEXT")
            self._ensure_column(connection, "suppliers", "contract_expires_on", "TEXT")
            self._ensure_column(connection, "suppliers", "payment_terms", "TEXT")
            self._ensure_column(connection, "suppliers", "notes", "TEXT")
            self._ensure_column(connection, "categories", "is_active", "INTEGER NOT NULL DEFAULT 1")
            self._ensure_column(connection, "products", "barcode", "TEXT")
            self._ensure_column(connection, "products", "description", "TEXT")
            self._ensure_column(connection, "products", "certificate_ref", "TEXT")
            self._ensure_column(connection, "products", "is_active", "INTEGER NOT NULL DEFAULT 1")
            self._ensure_column(connection, "suppliers", "lat", "REAL")
            self._ensure_column(connection, "suppliers", "lng", "REAL")
            self._ensure_column(connection, "suppliers", "city", "TEXT")
            self._ensure_column(connection, "warehouses", "controlled_substance_limit", "TEXT")
            self._ensure_column(connection, "suppliers", "delivery_days", "INTEGER")
            self._ensure_column(connection, "suppliers", "password_hash", "TEXT")
            self._ensure_column(connection, "suppliers", "portal_access_enabled", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_supplier_application_schema(connection)
            self._ensure_column(connection, "batches", "serial_number", "TEXT")
            self._ensure_column(connection, "products", "label_needs_reprint", "INTEGER NOT NULL DEFAULT 0")
            self._ensure_column(connection, "products", "last_label_price", "TEXT")
            self._ensure_column(connection, "audit_log", "warehouse_id", "INTEGER REFERENCES warehouses(id)")
            self._ensure_column(connection, "audit_log", "request_id", "TEXT")
            self._ensure_column(connection, "audit_log", "ip_address", "TEXT")
            self._ensure_column(connection, "audit_log", "user_agent", "TEXT")
            self._ensure_column(connection, "notifications", "batch_id", "INTEGER REFERENCES batches(id)")
            self._ensure_column(connection, "notifications", "device_id", "INTEGER REFERENCES sensor_devices(id)")
            self._ensure_column(
                connection,
                "notifications",
                "sensor_reading_id",
                "INTEGER REFERENCES sensor_readings(id)",
            )
            self._ensure_column(
                connection,
                "stock_document_lines",
                "target_warehouse_id",
                "INTEGER REFERENCES warehouses(id)",
            )
            self._ensure_column(connection, "stock_document_lines", "serial_number", "TEXT")
            self._ensure_column(connection, "stock_documents", "approved_by", "TEXT")
            self._ensure_column(connection, "stock_documents", "external_ref", "TEXT")
            self._ensure_column(connection, "stock_documents", "notes", "TEXT")
            self._ensure_column(connection, "stock_documents", "approved_at", "TEXT")
            self._ensure_column(connection, "stock_movements", "second_approver_id", "TEXT")
            self._ensure_column(connection, "stock_movements", "second_approval_note", "TEXT")
            self._ensure_column(connection, "stock_document_lines", "second_approver_id", "TEXT")
            self._ensure_column(connection, "stock_document_lines", "second_approval_note", "TEXT")
            self._ensure_repack_schema(connection)
            self._ensure_recall_schema(connection)
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS purchase_requests (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
                  product_id INTEGER NOT NULL REFERENCES products(id),
                  status TEXT NOT NULL,
                  current_free_quantity TEXT NOT NULL,
                  reorder_point TEXT NOT NULL,
                  safety_stock TEXT NOT NULL DEFAULT '0',
                  recommended_quantity TEXT NOT NULL,
                  reason TEXT,
                  source TEXT NOT NULL DEFAULT 'auto',
                  created_by TEXT NOT NULL,
                  created_at TEXT NOT NULL
                )
                """
            )
            self._ensure_column(
                connection,
                "purchase_requests",
                "safety_stock",
                "TEXT NOT NULL DEFAULT '0'",
            )
            self._ensure_column(
                connection,
                "purchase_requests",
                "reason",
                "TEXT",
            )
            self._ensure_column(
                connection,
                "purchase_requests",
                "source",
                "TEXT NOT NULL DEFAULT 'auto'",
            )
            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_notifications_unread_expiry_warehouse_batch
                  ON notifications(warehouse_id, batch_id)
                  WHERE notification_type = 'expiry' AND is_read = 0
                """
            )
            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_notifications_unread_sensor_warning_device
                  ON notifications(device_id)
                  WHERE notification_type = 'sensor_warning' AND is_read = 0
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_purchase_requests_warehouse_status_created
                  ON purchase_requests(warehouse_id, status, created_at DESC, id DESC)
                """
            )
            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS uq_purchase_requests_open_draft_product_warehouse
                  ON purchase_requests(warehouse_id, product_id)
                  WHERE status = 'draft'
                """
            )
            self._ensure_abc_xyz_history_schema(connection)
            self._ensure_quarantine_review_schema(connection)
            self._ensure_sensor_schema(connection)
            self._ensure_inventory_metadata_schema(connection)
            self._ensure_supplier_price_history_schema(connection)

    def _ensure_supplier_application_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS supplier_applications (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              actor_id TEXT NOT NULL,
              supplier_id INTEGER REFERENCES suppliers(id),
              status TEXT NOT NULL,
              name TEXT NOT NULL,
              bin TEXT,
              phone TEXT,
              email TEXT NOT NULL,
              contact_person TEXT,
              address TEXT,
              city TEXT,
              delivery_days INTEGER,
              notes TEXT,
              review_reason TEXT,
              submitted_at TEXT NOT NULL,
              reviewed_by TEXT,
              reviewed_at TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_supplier_applications_status_submitted
            ON supplier_applications(status, submitted_at DESC, id DESC)
            """
        )

    def _ensure_inventory_metadata_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory_responsibles (
              session_id INTEGER NOT NULL REFERENCES inventory_sessions(id) ON DELETE CASCADE,
              responsible_id TEXT NOT NULL,
              PRIMARY KEY(session_id, responsible_id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory_session_categories (
              session_id INTEGER NOT NULL REFERENCES inventory_sessions(id) ON DELETE CASCADE,
              category_id INTEGER NOT NULL REFERENCES categories(id),
              PRIMARY KEY(session_id, category_id)
            )
            """
        )

    def _ensure_supplier_price_history_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS supplier_price_history (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
              product_id INTEGER NOT NULL REFERENCES products(id),
              batch_id INTEGER REFERENCES batches(id),
              lot TEXT,
              unit_price TEXT NOT NULL,
              source TEXT NOT NULL,
              recorded_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_supplier_price_history_supplier_product_recorded
              ON supplier_price_history(supplier_id, product_id, recorded_at DESC, id DESC)
            """
        )

    def _ensure_recall_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS batch_recalls (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              batch_id INTEGER NOT NULL REFERENCES batches(id),
              product_id INTEGER NOT NULL REFERENCES products(id),
              reason TEXT NOT NULL,
              source TEXT NOT NULL DEFAULT 'manual',
              reference TEXT,
              created_by TEXT NOT NULL,
              created_at TEXT NOT NULL
            )
            """
        )
        self._ensure_column(connection, "batch_recalls", "source", "TEXT NOT NULL DEFAULT 'manual'")
        self._ensure_column(connection, "batch_recalls", "reference", "TEXT")
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_batch_recalls_batch_created
              ON batch_recalls(batch_id, created_at DESC, id DESC)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_batch_recalls_created
              ON batch_recalls(created_at DESC, id DESC)
            """
        )

    def _ensure_repack_schema(self, connection: sqlite3.Connection) -> None:
        self._ensure_column(
            connection,
            "stock_document_lines",
            "target_product_id",
            "INTEGER REFERENCES products(id)",
        )
        self._ensure_column(connection, "stock_document_lines", "target_quantity", "TEXT")
        self._ensure_column(connection, "stock_document_lines", "conversion_factor", "TEXT")
        self._ensure_column(connection, "stock_document_lines", "loss_quantity", "TEXT")
        self._ensure_column(connection, "stock_document_lines", "target_unit_price", "TEXT")
        self._ensure_column(connection, "stock_document_lines", "target_lot", "TEXT")
        self._ensure_column(connection, "stock_document_lines", "target_expires_on", "TEXT")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS batch_transformations (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              document_id INTEGER REFERENCES stock_documents(id),
              source_batch_id INTEGER NOT NULL REFERENCES batches(id),
              target_batch_id INTEGER NOT NULL REFERENCES batches(id),
              warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
              source_product_id INTEGER NOT NULL REFERENCES products(id),
              target_product_id INTEGER NOT NULL REFERENCES products(id),
              source_quantity TEXT NOT NULL,
              target_quantity TEXT NOT NULL,
              conversion_factor TEXT NOT NULL,
              loss_quantity TEXT NOT NULL DEFAULT '0',
              reason TEXT,
              created_by TEXT NOT NULL,
              created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_batch_transformations_source_batch
              ON batch_transformations(source_batch_id, created_at DESC, id DESC)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_batch_transformations_target_batch
              ON batch_transformations(target_batch_id, created_at DESC, id DESC)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_batch_transformations_document
              ON batch_transformations(document_id)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_batch_transformations_warehouse_created
              ON batch_transformations(warehouse_id, created_at DESC, id DESC)
            """
        )

    def _ensure_sensor_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_devices (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
              name TEXT NOT NULL,
              serial_number TEXT,
              sensor_type TEXT NOT NULL DEFAULT 'temperature_humidity',
              min_temperature_c TEXT,
              max_temperature_c TEXT,
              min_humidity_percent TEXT,
              max_humidity_percent TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              device_id INTEGER NOT NULL REFERENCES sensor_devices(id),
              warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
              temperature_c TEXT,
              humidity_percent TEXT,
              recorded_at TEXT NOT NULL,
              received_at TEXT NOT NULL,
              status TEXT NOT NULL,
              raw_payload TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_sensor_devices_warehouse
              ON sensor_devices(warehouse_id, id)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_sensor_readings_warehouse_recorded
              ON sensor_readings(warehouse_id, recorded_at DESC, id DESC)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_sensor_readings_device_recorded
              ON sensor_readings(device_id, recorded_at DESC, id DESC)
            """
        )

    def _ensure_quarantine_review_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS quarantine_reviews (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              batch_id INTEGER NOT NULL REFERENCES batches(id),
              warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
              status TEXT NOT NULL,
              responsible_id TEXT,
              due_at TEXT,
              decision_reason TEXT,
              created_by TEXT NOT NULL,
              decided_by TEXT,
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              decided_at TEXT,
              UNIQUE(batch_id, warehouse_id)
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_quarantine_reviews_warehouse_status_due
              ON quarantine_reviews(warehouse_id, status, due_at, id)
            """
        )
        self._ensure_column(connection, "quarantine_reviews", "commission_members", "TEXT")
        self._ensure_column(connection, "quarantine_reviews", "resolution_type", "TEXT")
        self._ensure_column(connection, "quarantine_reviews", "disposal_quantity", "TEXT")

    def _ensure_abc_xyz_history_schema(self, connection: sqlite3.Connection) -> None:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS abc_xyz_runs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              warehouse_id INTEGER REFERENCES warehouses(id),
              analysis_days INTEGER NOT NULL,
              period_start TEXT NOT NULL,
              period_end TEXT NOT NULL,
              source TEXT NOT NULL,
              status TEXT NOT NULL,
              items_count INTEGER NOT NULL DEFAULT 0,
              error TEXT,
              generated_by TEXT NOT NULL,
              generated_at TEXT NOT NULL
            )
            """
        )
        self._ensure_column(connection, "abc_xyz_runs", "period_start", "TEXT NOT NULL DEFAULT ''")
        self._ensure_column(connection, "abc_xyz_runs", "period_end", "TEXT NOT NULL DEFAULT ''")
        self._ensure_column(connection, "abc_xyz_runs", "source", "TEXT NOT NULL DEFAULT 'manual'")
        self._ensure_column(connection, "abc_xyz_runs", "status", "TEXT NOT NULL DEFAULT 'succeeded'")
        self._ensure_column(connection, "abc_xyz_runs", "items_count", "INTEGER NOT NULL DEFAULT 0")
        self._ensure_column(connection, "abc_xyz_runs", "error", "TEXT")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS abc_xyz_run_items (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              run_id INTEGER NOT NULL REFERENCES abc_xyz_runs(id) ON DELETE CASCADE,
              product_id INTEGER NOT NULL REFERENCES products(id),
              product_name TEXT NOT NULL,
              sku TEXT NOT NULL,
              abc_class TEXT NOT NULL,
              xyz_class TEXT NOT NULL,
              consumption_quantity TEXT NOT NULL,
              consumption_value TEXT NOT NULL,
              current_free_quantity TEXT NOT NULL,
              reorder_point TEXT NOT NULL,
              safety_stock TEXT NOT NULL,
              recommended_order_quantity TEXT NOT NULL,
              recommendation TEXT NOT NULL,
              movement_count INTEGER NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_abc_xyz_runs_warehouse_generated
              ON abc_xyz_runs(warehouse_id, generated_at DESC, id DESC)
            """
        )
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS uq_abc_xyz_runs_period
              ON abc_xyz_runs(
                COALESCE(warehouse_id, 0), analysis_days, period_start, period_end, source
              )
              WHERE status = 'succeeded'
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_abc_xyz_run_items_run
              ON abc_xyz_run_items(run_id, product_id)
            """
        )

    def _ensure_column(
        self, connection: sqlite3.Connection, table: str, column: str, definition: str
    ) -> None:
        columns = {row["name"] for row in connection.execute(f"PRAGMA table_info({table})")}
        if column not in columns:
            connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            if self.path != ":memory:":
                connection.close()


def insert_and_get_id(connection: sqlite3.Connection, query: str, params: tuple[Any, ...]) -> int:
    if hasattr(connection, "insert_and_get_id"):
        return int(connection.insert_and_get_id(query, params))
    cursor = connection.execute(query, params)
    return int(cursor.lastrowid)
