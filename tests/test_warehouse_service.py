from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from app.domain.enums import AuditAction, BatchStatus, InventoryStatus, QuarantineReviewStatus
from app.domain.errors import (
    BatchUnavailableError,
    InsufficientStockError,
    InventoryLockedError,
    NotFoundError,
    ValidationError,
)
from app.domain.schemas import (
    CategoryCreate,
    CategoryUpdate,
    DepartmentReturnDocumentCreate,
    DepartmentReturnDocumentLineCreate,
    DepartmentReturnCreate,
    InventoryCreate,
    InventoryLineCountUpdate,
    BatchRecallCreate,
    ProductCreate,
    ProductUpdate,
    PurchaseRequestCreate,
    PurchaseRequestStatusUpdate,
    QuarantineReviewUpdate,
    ReceiptCreate,
    ReceiptDocumentCreate,
    ReceiptDocumentLineCreate,
    RepackDocumentCreate,
    RepackDocumentLineCreate,
    ReservationCreate,
    ReservationUseCreate,
    SensorDeviceCreate,
    SensorReadingCreate,
    SupplierApplicationCreate,
    SupplierApplicationReview,
    SupplierCreate,
    SupplierUpdate,
    SupplierReturnDocumentCreate,
    SupplierReturnDocumentLineCreate,
    SupplierReturnCreate,
    TransferCreate,
    TransferDocumentCreate,
    TransferDocumentLineCreate,
    WarehouseCreate,
    WarehouseUpdate,
    WriteOffCreate,
    WriteOffFefoCreate,
    WriteOffDocumentCreate,
    WriteOffDocumentLineCreate,
)
from app.services.warehouse import WarehouseService
from app.storage.sqlite import SQLiteDatabase


class WarehouseServiceTest(TestCase):
    def setUp(self) -> None:
        self.database = SQLiteDatabase(":memory:")
        self.database.init_schema()
        self.service = WarehouseService(self.database)
        self.category = self.service.create_category(CategoryCreate(name="Медикаменты"))
        self.supplier = self.service.create_supplier(SupplierCreate(name="ТОО Поставщик"))
        self.warehouse = self.service.create_warehouse(WarehouseCreate(name="Основной склад"))
        self.product = self.service.create_product(
            ProductCreate(
                name="Физраствор",
                sku="NACL-001",
                unit="флакон",
                category_id=self.category["id"],
                reorder_point=Decimal("10"),
            )
        )

    def receive_available_batch(self, quantity: str = "20") -> dict:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal(quantity),
                unit_price=Decimal("350"),
                lot="LOT-1",
                expires_on=date(2027, 1, 1),
                quarantine=False,
            )
        )
        return batch

    def create_controlled_product(self) -> dict:
        return self.service.create_product(
            ProductCreate(
                name="Морфин",
                sku="CTRL-001",
                unit="ампула",
                category_id=self.category["id"],
                is_controlled=True,
            )
        )

    def receive_controlled_batch(self, quantity: str = "20") -> dict:
        product = self.create_controlled_product()
        return self.service.receive(
            ReceiptCreate(
                product_id=product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal(quantity),
                unit_price=Decimal("1000"),
                lot="CTRL-LOT-1",
                expires_on=date(2027, 1, 1),
                quarantine=False,
            )
        )

    def test_receipt_creates_balance(self) -> None:
        batch = self.receive_available_batch("12.5")

        balances = self.service.list_balances(self.product["id"])

        self.assertEqual(batch["status"], BatchStatus.AVAILABLE)
        self.assertEqual(balances[0]["total_quantity"], Decimal("12.5"))
        self.assertEqual(balances[0]["free_quantity"], Decimal("12.5"))

    def test_product_unit_must_exist_in_catalog(self) -> None:
        self.assertIn("шт", self.service.list_product_units())
        self.assertIn("ампула", self.service.list_product_units())

        with self.assertRaises(ValidationError):
            self.service.create_product(
                ProductCreate(
                    name="Товар с неверной единицей",
                    sku="BAD-UNIT",
                    unit="штуки",
                    category_id=self.category["id"],
                )
            )

    def test_marketplace_payment_method_stores_token_fingerprint(self) -> None:
        connection = self.database.connect()
        connection.execute(
            """CREATE TABLE marketplace_payment_methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                provider_token TEXT NOT NULL,
                brand TEXT NOT NULL DEFAULT 'unknown',
                last4 TEXT NOT NULL,
                expiry_month INTEGER,
                expiry_year INTEGER,
                holder_name TEXT,
                is_default BOOLEAN NOT NULL DEFAULT FALSE,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )"""
        )
        connection.commit()

        with patch(
            "app.services.warehouse.get_settings",
            return_value=SimpleNamespace(
                marketplace_payment_token_secret="unit-test-token-secret",
                jwt_hmac_secret=None,
                marketplace_payment_webhook_secret=None,
                deployment_mode="production",
            ),
        ):
            method = self.service.bind_marketplace_payment_method(
                "buyer-1",
                provider="test_psp",
                provider_token="tok_live_sensitive_12345",
                brand="visa",
                last4="4242",
                is_default=True,
            )

        row = connection.execute(
            "SELECT provider_token FROM marketplace_payment_methods WHERE id = ?",
            (int(method["id"]),),
        ).fetchone()

        self.assertIsNotNone(row)
        self.assertNotEqual(row["provider_token"], "tok_live_sensitive_12345")
        self.assertTrue(str(row["provider_token"]).startswith("hmac-sha256:"))
        self.assertEqual(len(str(row["provider_token"])), len("hmac-sha256:") + 64)

    def test_marketplace_payment_method_requires_token_secret_in_production(self) -> None:
        with patch(
            "app.services.warehouse.get_settings",
            return_value=SimpleNamespace(
                marketplace_payment_token_secret=None,
                jwt_hmac_secret=None,
                marketplace_payment_webhook_secret=None,
                deployment_mode="production",
            ),
        ):
            with self.assertRaises(ValidationError):
                self.service.bind_marketplace_payment_method(
                    "buyer-1",
                    provider="test_psp",
                    provider_token="tok_live_sensitive_12345",
                    brand="visa",
                    last4="4242",
                )

    def test_catalog_entries_can_be_updated_with_audit_trail(self) -> None:
        category = self.service.update_category(
            self.category["id"], CategoryUpdate(name="Расходные материалы"), "manager"
        )
        supplier = self.service.update_supplier(
            self.supplier["id"],
            SupplierUpdate(
                name="ТОО Надежный поставщик",
                bin="123456789012",
                phone="+7 777 000 00 00",
                address="Астана, склад 7",
                rating=5,
                is_preferred=True,
                contact_person="Айжан",
                email="supplier@example.kz",
                contract_number="MED-2026",
                contract_expires_on=date(2027, 12, 31),
                payment_terms="15 дней после поставки",
                notes="Основной поставщик расходников",
            ),
            "manager",
        )
        warehouse = self.service.update_warehouse(
            self.warehouse["id"],
            WarehouseUpdate(
                name="Склад отделения",
                department="Хирургия",
                tetis_org_id="71114554532",
                external_tetis_id="tetis-warehouse-1",
                storage_zone="Холодильник A",
                capacity_limit=Decimal("120.5"),
                storage_conditions="2-8 C",
                responsible_person="Зав. отделением",
            ),
            "manager",
        )
        product = self.service.update_product(
            self.product["id"],
            ProductUpdate(
                name="Физраствор 0.9%",
                sku="NACL-UPDATED",
                unit="бутылка",
                category_id=category["id"],
                reorder_point=Decimal("12.5"),
                safety_stock=Decimal("4.5"),
                is_controlled=True,
                barcode="4870200000012",
                description="Флакон 500 мл, стерильный раствор.",
                certificate_ref="CERT-2026-001",
            ),
            "manager",
        )

        self.assertEqual(category["name"], "Расходные материалы")
        self.assertEqual(supplier["phone"], "+7 777 000 00 00")
        self.assertEqual(supplier["contact_person"], "Айжан")
        self.assertEqual(supplier["email"], "supplier@example.kz")
        self.assertEqual(supplier["contract_number"], "MED-2026")
        self.assertEqual(supplier["contract_expires_on"], "2027-12-31")
        self.assertEqual(supplier["payment_terms"], "15 дней после поставки")
        self.assertEqual(supplier["notes"], "Основной поставщик расходников")
        self.assertEqual(warehouse["department"], "Хирургия")
        self.assertEqual(warehouse["tetis_org_id"], "71114554532")
        self.assertEqual(warehouse["external_tetis_id"], "tetis-warehouse-1")
        self.assertEqual(warehouse["storage_zone"], "Холодильник A")
        self.assertEqual(warehouse["capacity_limit"], "120.5")
        self.assertEqual(warehouse["storage_conditions"], "2-8 C")
        self.assertEqual(warehouse["responsible_person"], "Зав. отделением")
        self.assertEqual(product["sku"], "NACL-UPDATED")
        self.assertEqual(product["reorder_point"], "12.5")
        self.assertEqual(product["safety_stock"], "4.5")
        self.assertEqual(product["is_controlled"], 1)
        self.assertEqual(product["barcode"], "4870200000012")
        self.assertEqual(product["description"], "Флакон 500 мл, стерильный раствор.")
        self.assertEqual(product["certificate_ref"], "CERT-2026-001")
        audit_rows = self.service.list_audit_log(limit=20)
        update_rows = [row for row in audit_rows if row["action"] == "update"]
        self.assertGreaterEqual(len(update_rows), 4)

    def test_catalog_entries_are_soft_deleted_without_losing_history(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.delete_category(self.category["id"], "manager")

        product = self.service.delete_product(self.product["id"], "manager")
        self.assertFalse(product["is_active"])
        self.assertEqual(self.service.list_products(), [])

        category = self.service.delete_category(self.category["id"], "manager")
        self.assertFalse(category["is_active"])
        self.assertEqual(self.service.list_categories(), [])

        audit_log = self.service.list_audit_log()
        self.assertIn(AuditAction.DELETE, [row["action"] for row in audit_log])

        hidden_product = self.service._get_by_id(self.database.connect(), "products", self.product["id"])
        self.assertEqual(hidden_product["name"], "Физраствор")

    def test_tetis_org_mapping_lists_local_warehouse_ids(self) -> None:
        first = self.service.update_warehouse(
            self.warehouse["id"],
            WarehouseUpdate(
                name="Основной склад",
                department="Стационар",
                tetis_org_id="org-1",
                external_tetis_id="tetis-main",
            ),
        )
        second = self.service.create_warehouse(
            WarehouseCreate(
                name="Аптека",
                department="Фармация",
                tetis_org_id="org-1",
                external_tetis_id="tetis-pharmacy",
            )
        )
        self.service.create_warehouse(
            WarehouseCreate(name="Чужой склад", tetis_org_id="org-2", external_tetis_id="other")
        )

        self.assertEqual(
            self.service.list_warehouse_ids_for_tetis_org("org-1"),
            [first["id"], second["id"]],
        )
        self.assertEqual(self.service.list_warehouse_ids_for_tetis_org(" org-1 "), [first["id"], second["id"]])
        self.assertEqual(self.service.list_warehouse_ids_for_tetis_org(""), [])

    def test_mis_clinic_mapping_lists_local_warehouse_ids(self) -> None:
        first = self.service.update_warehouse(
            self.warehouse["id"],
            WarehouseUpdate(name="Основной склад", department="Стационар", mis_clinic_id="clinic-1"),
        )
        second = self.service.create_warehouse(
            WarehouseCreate(name="Кабинет 2", department="Стоматология", mis_clinic_id="clinic-1")
        )
        third = self.service.create_warehouse(
            WarehouseCreate(name="Чужая клиника", mis_clinic_id="clinic-2")
        )

        self.assertEqual(
            self.service.list_warehouse_ids_by_mis_clinic("clinic-1"),
            [first["id"], second["id"]],
        )
        self.assertEqual(self.service.list_warehouse_ids_by_mis_clinic("clinic-2"), [third["id"]])
        self.assertEqual(self.service.list_warehouse_ids_by_mis_clinic("unknown-clinic"), [])

    def test_sensor_readings_are_stored_with_threshold_status(self) -> None:
        device = self.service.create_sensor_device(
            SensorDeviceCreate(
                warehouse_id=self.warehouse["id"],
                name="Датчик холодильника",
                serial_number="USB-CH340",
                min_temperature_c=Decimal("2"),
                max_temperature_c=Decimal("8"),
                min_humidity_percent=Decimal("30"),
                max_humidity_percent=Decimal("70"),
            ),
            "manager",
        )

        ok_reading = self.service.record_sensor_reading(
            SensorReadingCreate(
                device_id=device["id"],
                temperature_c=Decimal("5.2"),
                humidity_percent=Decimal("45.0"),
                raw_payload="T=5.2 H=45.0",
            ),
            "sensor",
        )
        warning_reading = self.service.record_sensor_reading(
            SensorReadingCreate(
                device_id=device["id"],
                temperature_c=Decimal("11.3"),
                humidity_percent=Decimal("45.0"),
                raw_payload="T=11.3 H=45.0",
            ),
            "sensor",
        )

        self.assertEqual(ok_reading["warehouse_id"], self.warehouse["id"])
        self.assertEqual(ok_reading["status"], "ok")
        self.assertEqual(warning_reading["status"], "warning")
        self.assertEqual(self.service.count_sensor_readings(warehouse_id=self.warehouse["id"]), 2)
        listed = self.service.list_sensor_readings(warehouse_id=self.warehouse["id"])
        self.assertEqual(listed[0]["device_name"], "Датчик холодильника")
        self.assertEqual(listed[0]["warehouse_name"], "Основной склад")
        notifications = self.service.list_notifications(unread_only=True, warehouse_id=self.warehouse["id"])
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]["notification_type"], "sensor_warning")
        self.assertEqual(notifications[0]["device_id"], device["id"])
        self.assertEqual(notifications[0]["sensor_reading_id"], warning_reading["id"])
        self.assertIn("Нарушены условия хранения", notifications[0]["title"])
        self.assertIn("температура", notifications[0]["message"])

        repeated_warning = self.service.record_sensor_reading(
            SensorReadingCreate(
                device_id=device["id"],
                temperature_c=Decimal("12.0"),
                humidity_percent=Decimal("45.0"),
            ),
            "sensor",
        )
        deduped = self.service.list_notifications(unread_only=True, warehouse_id=self.warehouse["id"])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["id"], notifications[0]["id"])
        self.assertEqual(deduped[0]["sensor_reading_id"], repeated_warning["id"])

        self.service.mark_notification_read(deduped[0]["id"])
        new_warning = self.service.record_sensor_reading(
            SensorReadingCreate(device_id=device["id"], temperature_c=Decimal("13.0")),
            "sensor",
        )
        refreshed = self.service.list_notifications(unread_only=True, warehouse_id=self.warehouse["id"])
        self.assertEqual(len(refreshed), 1)
        self.assertNotEqual(refreshed[0]["id"], deduped[0]["id"])
        self.assertEqual(refreshed[0]["sensor_reading_id"], new_warning["id"])

    def test_sensor_warnings_are_deduped_per_device(self) -> None:
        first = self.service.create_sensor_device(
            SensorDeviceCreate(
                warehouse_id=self.warehouse["id"],
                name="Холодильник 1",
                min_temperature_c=Decimal("2"),
                max_temperature_c=Decimal("8"),
            ),
            "manager",
        )
        second = self.service.create_sensor_device(
            SensorDeviceCreate(
                warehouse_id=self.warehouse["id"],
                name="Холодильник 2",
                min_temperature_c=Decimal("2"),
                max_temperature_c=Decimal("8"),
            ),
            "manager",
        )

        ok = self.service.record_sensor_reading(
            SensorReadingCreate(device_id=first["id"], temperature_c=Decimal("5")),
            "sensor",
        )
        self.assertEqual(ok["status"], "ok")
        self.assertEqual(self.service.list_notifications(unread_only=True), [])

        self.service.record_sensor_reading(
            SensorReadingCreate(device_id=first["id"], temperature_c=Decimal("11")),
            "sensor",
        )
        self.service.record_sensor_reading(
            SensorReadingCreate(device_id=second["id"], temperature_c=Decimal("12")),
            "sensor",
        )

        notifications = self.service.list_notifications(unread_only=True, warehouse_id=self.warehouse["id"])
        self.assertEqual(len(notifications), 2)
        self.assertEqual({row["device_id"] for row in notifications}, {first["id"], second["id"]})

    def test_sensor_reading_rejects_empty_and_invalid_humidity(self) -> None:
        device = self.service.create_sensor_device(
            SensorDeviceCreate(warehouse_id=self.warehouse["id"], name="Датчик кабинета")
        )

        with self.assertRaises(ValidationError):
            self.service.record_sensor_reading(SensorReadingCreate(device_id=device["id"]))

        with self.assertRaises(ValidationError):
            self.service.record_sensor_reading(
                SensorReadingCreate(device_id=device["id"], humidity_percent=Decimal("101"))
            )

    def test_product_barcode_label_uses_existing_barcode_and_printable_zpl(self) -> None:
        product = self.service.update_product(
            self.product["id"],
            ProductUpdate(
                name="Физраствор 0.9%",
                sku="NACL-500",
                unit="флакон",
                category_id=self.category["id"],
                barcode="4870200000012",
            ),
        )

        label = self.service.get_product_barcode_label(product["id"])

        self.assertEqual(label["barcode"], "4870200000012")
        self.assertEqual(label["symbology"], "CODE128")
        self.assertIn("^XA", label["zpl"])
        self.assertIn("^BCN", label["zpl"])
        self.assertIn("4870200000012", label["zpl"])
        self.assertIn("B28,112", label["epl"])

    def test_product_barcode_label_generates_internal_code_when_barcode_is_empty(self) -> None:
        label = self.service.get_product_barcode_label(self.product["id"])

        self.assertEqual(label["barcode"], f"SKLAD-{self.product['id']:08d}")
        self.assertIn(label["barcode"], label["zpl"])

    def test_product_barcode_label_supports_ean13_and_epl(self) -> None:
        product = self.service.update_product(
            self.product["id"],
            ProductUpdate(
                name="Физраствор 0.9%",
                sku="NACL-500",
                unit="флакон",
                category_id=self.category["id"],
                barcode="487020000001",
            ),
        )

        label = self.service.get_product_barcode_label(product["id"], symbology="ean13")

        self.assertEqual(label["barcode"], "4870200000010")
        self.assertEqual(label["symbology"], "EAN13")
        self.assertIn("^BEN", label["zpl"])
        self.assertIn("E30", label["epl"])

    def test_product_barcode_labels_batch_deduplicates_and_combines_zpl(self) -> None:
        second_product = self.service.create_product(
            ProductCreate(
                name="Шприц",
                sku="SYR-005",
                unit="шт",
                category_id=self.category["id"],
                barcode="4870200000099",
            )
        )

        labels = self.service.get_product_barcode_labels(
            [self.product["id"], second_product["id"], self.product["id"]]
        )

        self.assertEqual([label["product_id"] for label in labels["labels"]], [self.product["id"], second_product["id"]])
        self.assertEqual(labels["labels"][0]["barcode"], f"SKLAD-{self.product['id']:08d}")
        self.assertIn("4870200000099", labels["zpl"])
        self.assertEqual(labels["zpl"].count("^XA"), 2)

    def test_get_product_by_barcode_finds_and_returns_none(self) -> None:
        second = self.service.create_product(
            __import__("app.domain.schemas", fromlist=["ProductCreate"]).ProductCreate(
                name="Barcode Search",
                sku="BC-SRCH-001",
                unit="шт",
                category_id=self.category["id"],
                barcode="4600123456789",
            )
        )
        found = self.service.get_product_by_barcode("4600123456789")
        self.assertIsNotNone(found)
        self.assertEqual(found["id"], second["id"])
        self.assertEqual(found["barcode"], "4600123456789")
        # Trimmed whitespace is handled
        found_ws = self.service.get_product_by_barcode("  4600123456789  ")
        self.assertIsNotNone(found_ws)
        self.assertEqual(found_ws["id"], second["id"])
        # Unknown barcode returns None
        self.assertIsNone(self.service.get_product_by_barcode("0000000000000"))

    def test_batch_price_label_contains_price_lot_zpl_and_epl(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("10"),
                unit_price=Decimal("350"),
                lot="LOT-PRICE",
                serial_number="SN-PRICE-1",
                expires_on=date(2027, 1, 1),
                quarantine=False,
            )
        )

        label = self.service.get_batch_price_label(batch["id"], symbology="ean13")

        self.assertEqual(label["batch_id"], batch["id"])
        self.assertEqual(label["unit_price"], Decimal("350"))
        self.assertEqual(label["symbology"], "EAN13")
        self.assertEqual(label["serial_number"], "SN-PRICE-1")
        self.assertIn("LOT-PRICE", label["zpl"])
        self.assertIn("SN-PRICE-1", label["zpl"])
        self.assertIn("Цена: 350", label["zpl"])
        self.assertIn("E30", label["epl"])

    def test_batch_price_labels_batch_deduplicates_and_combines_printer_payloads(self) -> None:
        first = self.receive_available_batch("10")
        second = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("375"),
                lot="LOT-2",
                expires_on=date(2027, 2, 1),
                quarantine=False,
            )
        )

        labels = self.service.get_batch_price_labels([first["id"], second["id"], first["id"]])

        self.assertEqual([label["batch_id"] for label in labels["labels"]], [first["id"], second["id"]])
        self.assertEqual(labels["zpl"].count("^XA"), 2)
        self.assertEqual(labels["epl"].count("P1"), 2)

    def test_supplier_price_history_is_recorded_on_receipts(self) -> None:
        self.receive_available_batch("10")
        self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("375"),
                lot="LOT-2",
                expires_on=date(2027, 2, 1),
                quarantine=False,
            )
        )

        history = self.service.list_supplier_price_history(self.supplier["id"], product_id=self.product["id"])

        self.assertEqual(self.service.count_supplier_price_history(self.supplier["id"], self.product["id"]), 2)
        self.assertEqual(history[0]["unit_price"], Decimal("375"))
        self.assertEqual(history[0]["lot"], "LOT-2")
        self.assertEqual(history[0]["product_name"], "Физраствор")

    def test_list_balances_supports_limit_and_offset(self) -> None:
        first = self.receive_available_batch("1")
        second = self.receive_available_batch("2")
        self.receive_available_batch("3")

        page = self.service.list_balances(self.product["id"], limit=1, offset=1)

        self.assertEqual(len(page), 1)
        self.assertNotEqual(page[0]["batch_id"], first["id"])
        self.assertEqual(page[0]["batch_id"], second["id"])
        self.assertEqual(self.service.count_balances(self.product["id"]), 3)

    def test_list_batches_supports_operational_filters(self) -> None:
        first = self.receive_available_batch("5")
        second = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("6"),
                unit_price=Decimal("350"),
                lot="LOT-2",
                expires_on=date(2028, 1, 1),
                quarantine=True,
            )
        )

        available = self.service.list_batches(
            product_id=self.product["id"],
            supplier_id=self.supplier["id"],
            status="available",
            expires_before=date(2027, 12, 31),
        )
        quarantine = self.service.list_batches(
            warehouse_id=self.warehouse["id"],
            status="quarantine",
            expires_after=date(2027, 12, 31),
        )

        self.assertEqual([row["id"] for row in available], [first["id"]])
        self.assertEqual([row["id"] for row in quarantine], [second["id"]])

    def test_quarantine_batch_cannot_be_written_off(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="Q-1",
                quarantine=True,
            )
        )

        with self.assertRaises(BatchUnavailableError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="Тест",
                )
            )

    def test_quarantine_receipt_creates_review_workflow(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="Q-WORKFLOW",
                quarantine=True,
            ),
            actor_id="receiver-1",
        )

        reviews = self.service.list_quarantine_reviews(warehouse_id=self.warehouse["id"])

        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["batch_id"], batch["id"])
        self.assertEqual(reviews[0]["status"], QuarantineReviewStatus.PENDING)
        self.assertEqual(reviews[0]["created_by"], "receiver-1")
        self.assertEqual(reviews[0]["product_name"], "Физраствор")

    def test_quarantine_review_decision_updates_batch_status(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="Q-DECISION",
                quarantine=True,
            )
        )
        review = self.service.list_quarantine_reviews(warehouse_id=self.warehouse["id"])[0]

        with self.assertRaises(ValidationError):
            self.service.update_quarantine_review(
                review["id"],
                QuarantineReviewUpdate(status=QuarantineReviewStatus.APPROVED),
                actor_id="quality-1",
            )

        approved = self.service.update_quarantine_review(
            review["id"],
            QuarantineReviewUpdate(
                status=QuarantineReviewStatus.APPROVED,
                responsible_id="quality-1",
                decision_reason="Сертификаты проверены",
            ),
            actor_id="quality-1",
        )

        self.assertEqual(approved["status"], QuarantineReviewStatus.APPROVED)
        self.assertEqual(approved["decided_by"], "quality-1")
        self.assertEqual(self.service.get_batch_detail(batch["id"])["batch"]["status"], BatchStatus.AVAILABLE)

        protocol = self.service.get_quarantine_review_protocol(review["id"])

        self.assertEqual(protocol["review_id"], review["id"])
        self.assertEqual(protocol["warehouse_name"], "Основной склад")
        self.assertEqual(protocol["status"], QuarantineReviewStatus.APPROVED)
        self.assertIn("Физраствор", protocol["csv"])
        self.assertIn("Q-DECISION", protocol["csv"])
        self.assertIn("Сертификаты проверены", protocol["csv"])

    def test_blocking_batch_closes_open_quarantine_review_as_rejected(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="Q-REJECT",
                quarantine=True,
            )
        )

        self.service.update_batch_status(batch["id"], BatchStatus.BLOCKED, "Сертификат не прошел", "quality-2")
        review = self.service.list_quarantine_reviews(warehouse_id=self.warehouse["id"])[0]

        self.assertEqual(review["status"], QuarantineReviewStatus.REJECTED)
        self.assertEqual(review["decision_reason"], "Сертификат не прошел")
        self.assertEqual(review["decided_by"], "quality-2")

    def test_batch_warehouse_ids_follow_transfers(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))

        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("4"),
            )
        )

        self.assertEqual(
            self.service.get_batch_warehouse_ids(batch["id"]),
            [self.warehouse["id"], target["id"]],
        )

    def test_batch_status_noop_does_not_create_audit_record(self) -> None:
        batch = self.receive_available_batch("10")
        before = self.service.count_audit_log(entity_type="batch")

        updated = self.service.update_batch_status(
            batch["id"], BatchStatus.AVAILABLE, "Уже доступна"
        )

        self.assertEqual(updated["status"], BatchStatus.AVAILABLE)
        self.assertEqual(self.service.count_audit_log(entity_type="batch"), before)

    def test_batch_status_audit_is_visible_for_each_batch_warehouse(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("4"),
            )
        )

        self.service.update_batch_status(batch["id"], BatchStatus.BLOCKED, "Отзыв партии")

        source_audit = self.service.list_audit_log(
            entity_type="batch", warehouse_id=self.warehouse["id"]
        )
        target_audit = self.service.list_audit_log(entity_type="batch", warehouse_id=target["id"])

        self.assertTrue(any(row["payload"]["status"] == BatchStatus.BLOCKED for row in source_audit))
        self.assertTrue(any(row["payload"]["status"] == BatchStatus.BLOCKED for row in target_audit))

    def test_recall_batch_blocks_stock_and_notifies_affected_warehouses(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("4"),
            )
        )

        result = self.service.recall_batch(
            batch["id"],
            BatchRecallCreate(
                reason="Письмо производителя об отзыве серии",
                source="manufacturer",
                reference="LETTER-42",
            ),
            actor_id="quality-chief",
        )

        self.assertEqual(result["batch"]["status"], BatchStatus.BLOCKED)
        self.assertEqual(result["recall"]["reason"], "Письмо производителя об отзыве серии")
        self.assertEqual(result["recall"]["reference"], "LETTER-42")
        self.assertEqual(
            sorted(row["warehouse_id"] for row in result["affected_warehouses"]),
            [self.warehouse["id"], target["id"]],
        )
        self.assertEqual(len(result["notifications"]), 2)
        self.assertTrue(all(row["notification_type"] == "recall" for row in result["notifications"]))
        with self.assertRaises(BatchUnavailableError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="Нельзя списывать отозванную партию",
                )
            )

        traceability = self.service.get_batch_traceability(batch["id"])
        self.assertEqual(traceability["recalls"][0]["created_by"], "quality-chief")
        recall_audit = self.service.list_audit_log(action="recall", entity_type="batch")
        self.assertGreaterEqual(len(recall_audit), 2)

    def test_reservation_reduces_free_balance(self) -> None:
        batch = self.receive_available_batch("20")

        reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("7"),
                reserved_for="Операционный день",
            )
        )
        balance = self.service.list_balances(self.product["id"])[0]

        self.assertEqual(reservation["quantity"], "7")
        self.assertEqual(balance["reserved_quantity"], Decimal("7"))
        self.assertEqual(balance["free_quantity"], Decimal("13"))

    def test_write_off_cannot_use_reserved_quantity(self) -> None:
        batch = self.receive_available_batch("10")
        self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("8"),
                reserved_for="Пациент #42",
            )
        )

        with self.assertRaises(InsufficientStockError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("3"),
                    reason="Списание",
                )
            )

    def test_controlled_batch_writeoff_requires_patient_doctor_record_and_second_approver(self) -> None:
        batch = self.receive_controlled_batch("5")

        with self.assertRaises(ValidationError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="Выдача пациенту",
                    patient_id="patient-1",
                    doctor_id="doctor-1",
                )
            )

        balance = self.service.list_balances(batch["product_id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("5"))

        with self.assertRaises(ValidationError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="Выдача пациенту",
                    patient_id="patient-1",
                    doctor_id="doctor-1",
                    medical_record_no="MR-1",
                )
            )
        with self.assertRaises(ValidationError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="Выдача пациенту",
                    patient_id="patient-1",
                    doctor_id="doctor-1",
                    medical_record_no="MR-1",
                    second_approver_id="doctor-1",
                )
            )
        balance = self.service.list_balances(batch["product_id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("5"))

        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("1"),
                reason="Выдача пациенту",
                patient_id="patient-1",
                doctor_id="doctor-1",
                medical_record_no="MR-1",
                second_approver_id="head-nurse-1",
                second_approval_note="Сверено по журналу ПКУ",
            )
        )
        balance = self.service.list_balances(batch["product_id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("4"))

    def test_controlled_substance_ledger_lists_controlled_movements(self) -> None:
        batch = self.receive_controlled_batch("5")
        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("2"),
                reason="Выдача пациенту",
                patient_id="patient-1",
                doctor_id="doctor-1",
                medical_record_no="MR-1",
                second_approver_id="head-nurse-1",
                second_approval_note="Сверено",
            )
        )
        self.receive_available_batch("3")

        entries = self.service.list_controlled_substance_ledger(
            warehouse_id=self.warehouse["id"],
            batch_id=batch["id"],
        )

        self.assertEqual(
            self.service.count_controlled_substance_ledger(warehouse_id=self.warehouse["id"]),
            2,
        )
        self.assertEqual(len(entries), 2)
        writeoff = next(item for item in entries if item["movement_type"] == "write_off")
        self.assertEqual(writeoff["product_name"], "Морфин")
        self.assertEqual(writeoff["lot"], "CTRL-LOT-1")
        self.assertEqual(writeoff["quantity"], "2")
        self.assertEqual(writeoff["patient_id"], "patient-1")
        self.assertEqual(writeoff["doctor_id"], "doctor-1")
        self.assertEqual(writeoff["medical_record_no"], "MR-1")
        self.assertEqual(writeoff["second_approver_id"], "head-nurse-1")
        self.assertEqual(writeoff["second_approval_note"], "Сверено")

    def test_inventory_lock_blocks_movements(self) -> None:
        batch = self.receive_available_batch("10")
        self.service.set_inventory_lock(self.warehouse["id"], True)

        with self.assertRaises(InventoryLockedError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="Списание во время инвентаризации",
                )
            )

    def test_transfer_moves_free_stock_between_warehouses(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))

        result = self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("4"),
                reason="Выдача в кабинет",
            )
        )
        source_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        target_balance = self.service.list_balances(
            self.product["id"], warehouse_id=target["id"]
        )[0]

        self.assertEqual(result["quantity"], "4")
        self.assertEqual(source_balance["total_quantity"], Decimal("6"))
        self.assertEqual(target_balance["total_quantity"], Decimal("4"))
        self.assertEqual(target_balance["free_quantity"], Decimal("4"))

    def test_transfer_accumulates_existing_target_balance(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))

        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("3"),
            )
        )
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("2"),
            )
        )
        target_balance = self.service.list_balances(
            self.product["id"], warehouse_id=target["id"]
        )[0]

        self.assertEqual(target_balance["total_quantity"], Decimal("5"))

    def test_transfer_cannot_use_reserved_source_quantity(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("8"),
                reserved_for="Операционный день",
            )
        )

        with self.assertRaises(InsufficientStockError):
            self.service.transfer(
                TransferCreate(
                    batch_id=batch["id"],
                    source_warehouse_id=self.warehouse["id"],
                    target_warehouse_id=target["id"],
                    quantity=Decimal("3"),
                )
            )

        source_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        self.assertEqual(source_balance["total_quantity"], Decimal("10"))

    def test_generate_purchase_requests_uses_reorder_point_and_deduplicates_drafts(self) -> None:
        self.receive_available_batch("4")

        generated = self.service.generate_purchase_requests(self.warehouse["id"], actor_id="buyer-1")
        generated_again = self.service.generate_purchase_requests(
            self.warehouse["id"], actor_id="buyer-1"
        )
        listed = self.service.list_purchase_requests(warehouse_id=self.warehouse["id"])

        self.assertEqual(len(generated), 1)
        self.assertEqual(generated_again[0]["id"], generated[0]["id"])
        self.assertEqual(len(listed), 1)
        self.assertEqual(generated[0]["warehouse_id"], self.warehouse["id"])
        self.assertEqual(generated[0]["product_id"], self.product["id"])
        self.assertEqual(generated[0]["status"], "draft")
        self.assertEqual(generated[0]["current_free_quantity"], "4")
        self.assertEqual(generated[0]["reorder_point"], "10")
        self.assertEqual(generated[0]["recommended_quantity"], "6")
        self.assertEqual(generated[0]["reason"], "Ниже точки заказа")
        self.assertEqual(generated[0]["source"], "auto")

    def test_create_purchase_request_updates_existing_draft(self) -> None:
        created = self.service.create_purchase_request(
            PurchaseRequestCreate(
                warehouse_id=self.warehouse["id"],
                product_id=self.product["id"],
                quantity=Decimal("12"),
                reason="Нужно для отделения",
            ),
            actor_id="buyer-2",
        )
        updated = self.service.create_purchase_request(
            PurchaseRequestCreate(
                warehouse_id=self.warehouse["id"],
                product_id=self.product["id"],
                quantity=Decimal("18"),
                reason="Срочное пополнение",
            ),
            actor_id="buyer-2",
        )
        listed = self.service.list_purchase_requests(warehouse_id=self.warehouse["id"])

        self.assertEqual(updated["id"], created["id"])
        self.assertEqual(len(listed), 1)
        self.assertEqual(updated["recommended_quantity"], "18")
        self.assertEqual(updated["reason"], "Срочное пополнение")
        self.assertEqual(updated["source"], "manual")

    def test_purchase_request_status_can_be_ordered_or_cancelled_from_draft(self) -> None:
        created = self.service.create_purchase_request(
            PurchaseRequestCreate(
                warehouse_id=self.warehouse["id"],
                product_id=self.product["id"],
                quantity=Decimal("12"),
                reason="Нужно для отделения",
            ),
            actor_id="buyer-2",
        )

        ordered = self.service.update_purchase_request_status(
            created["id"],
            PurchaseRequestStatusUpdate(status="ordered"),
            actor_id="buyer-2",
        )
        ordered_again = self.service.update_purchase_request_status(
            created["id"],
            PurchaseRequestStatusUpdate(status="ordered"),
            actor_id="buyer-2",
        )

        self.assertEqual(ordered["status"], "ordered")
        self.assertEqual(ordered_again["status"], "ordered")
        with self.assertRaises(ValidationError):
            self.service.update_purchase_request_status(
                created["id"],
                PurchaseRequestStatusUpdate(status="cancelled"),
                actor_id="buyer-2",
            )

    def test_transfer_is_blocked_when_target_inventory_is_locked(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.create_inventory_session(InventoryCreate(warehouse_id=target["id"]))

        with self.assertRaises(InventoryLockedError):
            self.service.transfer(
                TransferCreate(
                    batch_id=batch["id"],
                    source_warehouse_id=self.warehouse["id"],
                    target_warehouse_id=target["id"],
                    quantity=Decimal("1"),
                )
            )

        source_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        self.assertEqual(source_balance["total_quantity"], Decimal("10"))

    def test_return_from_department_moves_stock_back_to_main_warehouse(self) -> None:
        batch = self.receive_available_batch("10")
        cabinet = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=cabinet["id"],
                quantity=Decimal("4"),
            )
        )

        self.service.return_from_department(
            DepartmentReturnCreate(
                batch_id=batch["id"],
                source_warehouse_id=cabinet["id"],
                target_warehouse_id=self.warehouse["id"],
                quantity=Decimal("1.5"),
                reason="Не использовали",
            ),
            actor_id="nurse-1",
        )
        main_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        cabinet_balance = self.service.list_balances(
            self.product["id"], warehouse_id=cabinet["id"]
        )[0]
        audit_log = self.service.list_audit_log(entity_type="batch", limit=20)

        self.assertEqual(main_balance["total_quantity"], Decimal("7.5"))
        self.assertEqual(cabinet_balance["total_quantity"], Decimal("2.5"))
        self.assertTrue(any(row["action"] == "return" for row in audit_log))

    def test_return_to_supplier_reduces_free_stock(self) -> None:
        batch = self.receive_available_batch("10")

        result = self.service.return_to_supplier(
            SupplierReturnCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                supplier_id=self.supplier["id"],
                quantity=Decimal("3"),
                reason="Брак",
            )
        )
        balance = self.service.list_balances(self.product["id"])[0]

        self.assertEqual(result["quantity"], "3")
        self.assertEqual(balance["total_quantity"], Decimal("7"))

    def test_return_to_supplier_requires_original_supplier(self) -> None:
        batch = self.receive_available_batch("10")
        other_supplier = self.service.create_supplier(SupplierCreate(name="Другой поставщик"))

        with self.assertRaises(ValidationError):
            self.service.return_to_supplier(
                SupplierReturnCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    supplier_id=other_supplier["id"],
                    quantity=Decimal("1"),
                    reason="Брак",
                )
            )

        balance = self.service.list_balances(self.product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("10"))

    def test_return_to_supplier_cannot_use_reserved_quantity(self) -> None:
        batch = self.receive_available_batch("10")
        self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("8"),
                reserved_for="Операционный день",
            )
        )

        with self.assertRaises(InsufficientStockError):
            self.service.return_to_supplier(
                SupplierReturnCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    supplier_id=self.supplier["id"],
                    quantity=Decimal("3"),
                    reason="Брак",
                )
            )

        balance = self.service.list_balances(self.product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("10"))

    def test_receipt_document_draft_does_not_change_balance_until_posted(self) -> None:
        document = self.service.create_receipt_document(
            ReceiptDocumentCreate(
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                lines=[
                    ReceiptDocumentLineCreate(
                        product_id=self.product["id"],
                        quantity=Decimal("9"),
                        unit_price=Decimal("200"),
                        lot="DOC-1",
                        expires_on=date(2028, 1, 1),
                        quarantine=False,
                    )
                ],
            )
        )

        self.assertEqual(self.service.list_balances(self.product["id"]), [])

        posted = self.service.post_stock_document(document["id"])
        balances = self.service.list_balances(self.product["id"])

        self.assertEqual(posted["status"], "posted")
        self.assertEqual(balances[0]["free_quantity"], Decimal("9"))

    def test_stock_documents_can_be_filtered_by_type_and_status(self) -> None:
        receipt = self.service.create_receipt_document(
            ReceiptDocumentCreate(
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                lines=[
                    ReceiptDocumentLineCreate(
                        product_id=self.product["id"],
                        quantity=Decimal("9"),
                        unit_price=Decimal("200"),
                        lot="DOC-FILTER",
                        quarantine=False,
                    )
                ],
            )
        )
        batch = self.receive_available_batch("5")
        writeoff = self.service.create_writeoff_document(
            WriteOffDocumentCreate(
                warehouse_id=self.warehouse["id"],
                lines=[
                    WriteOffDocumentLineCreate(
                        batch_id=batch["id"],
                        quantity=Decimal("2"),
                        reason="Фильтр",
                    )
                ],
            )
        )

        receipts = self.service.list_stock_documents(
            document_type="receipt",
            status="draft",
        )
        writeoffs_total = self.service.count_stock_documents(
            warehouse_id=self.warehouse["id"],
            document_type="write_off",
            status="draft",
        )

        self.assertEqual([row["id"] for row in receipts], [receipt["id"]])
        self.assertEqual(writeoffs_total, 1)
        self.assertEqual(
            self.service.list_stock_documents(document_type="write_off")[0]["id"],
            writeoff["id"],
        )

    def test_post_stock_document_is_idempotent(self) -> None:
        document = self.service.create_receipt_document(
            ReceiptDocumentCreate(
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                lines=[
                    ReceiptDocumentLineCreate(
                        product_id=self.product["id"],
                        quantity=Decimal("4"),
                        unit_price=Decimal("200"),
                        lot="DOC-2",
                        quarantine=False,
                    )
                ],
            )
        )

        self.service.post_stock_document(document["id"])
        self.service.post_stock_document(document["id"])

        balances = self.service.list_balances(self.product["id"])
        self.assertEqual(len(balances), 1)
        self.assertEqual(balances[0]["total_quantity"], Decimal("4"))

    def test_stock_document_can_be_approved_before_posting(self) -> None:
        document = self.service.create_receipt_document(
            ReceiptDocumentCreate(
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                lines=[
                    ReceiptDocumentLineCreate(
                        product_id=self.product["id"],
                        quantity=Decimal("4"),
                        unit_price=Decimal("200"),
                        lot="APPROVE-1",
                        quarantine=False,
                    )
                ],
            )
        )

        approved = self.service.approve_stock_document(document["id"], actor_id="chief")
        approved_again = self.service.approve_stock_document(document["id"], actor_id="chief")
        self.assertEqual(approved["status"], "approved")
        self.assertEqual(approved["approved_by"], "chief")
        self.assertIsNotNone(approved["approved_at"])
        self.assertEqual(approved_again["status"], "approved")
        self.assertEqual(self.service.list_balances(self.product["id"]), [])

        posted = self.service.post_stock_document(document["id"], actor_id="chief")
        self.assertEqual(posted["status"], "posted")
        self.assertEqual(self.service.list_balances(self.product["id"])[0]["free_quantity"], Decimal("4"))

        with self.assertRaises(ValidationError):
            self.service.approve_stock_document(document["id"], actor_id="chief")

    def test_cancel_stock_document_marks_draft_without_changing_balances(self) -> None:
        document = self.service.create_receipt_document(
            ReceiptDocumentCreate(
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                lines=[
                    ReceiptDocumentLineCreate(
                        product_id=self.product["id"],
                        quantity=Decimal("5"),
                        unit_price=Decimal("200"),
                        lot="CANCEL-1",
                        quarantine=False,
                    )
                ],
            )
        )

        cancelled = self.service.cancel_stock_document(document["id"])
        cancelled_again = self.service.cancel_stock_document(document["id"])

        self.assertEqual(cancelled["status"], "cancelled")
        self.assertEqual(cancelled_again["status"], "cancelled")
        self.assertEqual(self.service.list_balances(self.product["id"]), [])

    def test_cancel_stock_document_allows_approved_document(self) -> None:
        document = self.service.create_receipt_document(
            ReceiptDocumentCreate(
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                lines=[
                    ReceiptDocumentLineCreate(
                        product_id=self.product["id"],
                        quantity=Decimal("5"),
                        unit_price=Decimal("200"),
                        lot="CANCEL-APPROVED",
                        quarantine=False,
                    )
                ],
            )
        )
        self.service.approve_stock_document(document["id"], actor_id="chief")

        cancelled = self.service.cancel_stock_document(document["id"])

        self.assertEqual(cancelled["status"], "cancelled")
        self.assertEqual(self.service.list_balances(self.product["id"]), [])

    def test_cancel_stock_document_rejects_posted_document(self) -> None:
        document = self.service.create_receipt_document(
            ReceiptDocumentCreate(
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                lines=[
                    ReceiptDocumentLineCreate(
                        product_id=self.product["id"],
                        quantity=Decimal("5"),
                        unit_price=Decimal("200"),
                        lot="CANCEL-2",
                        quarantine=False,
                    )
                ],
            )
        )
        self.service.post_stock_document(document["id"])

        with self.assertRaises(ValidationError):
            self.service.cancel_stock_document(document["id"])

        balances = self.service.list_balances(self.product["id"])
        self.assertEqual(balances[0]["total_quantity"], Decimal("5"))

    def test_transfer_document_draft_does_not_change_balance_until_posted(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))

        document = self.service.create_transfer_document(
            TransferDocumentCreate(
                source_warehouse_id=self.warehouse["id"],
                lines=[
                    TransferDocumentLineCreate(
                        batch_id=batch["id"],
                        target_warehouse_id=target["id"],
                        quantity=Decimal("4"),
                        reason="Выдача в кабинет",
                    )
                ],
            )
        )

        source_before = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        self.assertEqual(document["lines"][0]["target_warehouse_id"], target["id"])
        self.assertEqual(source_before["total_quantity"], Decimal("10"))
        self.assertEqual(self.service.list_balances(self.product["id"], warehouse_id=target["id"]), [])

        posted = self.service.post_stock_document(document["id"])
        source_after = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        target_after = self.service.list_balances(
            self.product["id"], warehouse_id=target["id"]
        )[0]

        self.assertEqual(posted["status"], "posted")
        self.assertEqual(source_after["total_quantity"], Decimal("6"))
        self.assertEqual(target_after["total_quantity"], Decimal("4"))

        print_form = self.service.get_transfer_print_form(document["id"])

        self.assertEqual(print_form["document_id"], document["id"])
        self.assertEqual(print_form["status"], "posted")
        self.assertEqual(print_form["source_warehouse_name"], "Основной склад")
        self.assertEqual(print_form["lines"][0]["target_warehouse_name"], "Кабинет 101")
        self.assertIn("Товар", print_form["csv"])
        self.assertIn("Кабинет 101", print_form["csv"])
        self.assertIn("Выдача в кабинет", print_form["csv"])

    def test_transfer_document_rolls_back_when_any_line_fails(self) -> None:
        batch = self.receive_available_batch("5")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        document = self.service.create_transfer_document(
            TransferDocumentCreate(
                source_warehouse_id=self.warehouse["id"],
                lines=[
                    TransferDocumentLineCreate(
                        batch_id=batch["id"],
                        target_warehouse_id=target["id"],
                        quantity=Decimal("2"),
                    ),
                    TransferDocumentLineCreate(
                        batch_id=batch["id"],
                        target_warehouse_id=target["id"],
                        quantity=Decimal("10"),
                    ),
                ],
            )
        )

        with self.assertRaises(InsufficientStockError):
            self.service.post_stock_document(document["id"])

        source_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        self.assertEqual(source_balance["total_quantity"], Decimal("5"))
        self.assertEqual(self.service.list_balances(self.product["id"], warehouse_id=target["id"]), [])
        self.assertEqual(self.service.get_stock_document(document["id"])["status"], "draft")

    def test_transfer_document_post_is_idempotent(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        document = self.service.create_transfer_document(
            TransferDocumentCreate(
                source_warehouse_id=self.warehouse["id"],
                lines=[
                    TransferDocumentLineCreate(
                        batch_id=batch["id"],
                        target_warehouse_id=target["id"],
                        quantity=Decimal("3"),
                    )
                ],
            )
        )

        self.service.post_stock_document(document["id"])
        self.service.post_stock_document(document["id"])

        source_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        target_balance = self.service.list_balances(
            self.product["id"], warehouse_id=target["id"]
        )[0]
        self.assertEqual(source_balance["total_quantity"], Decimal("7"))
        self.assertEqual(target_balance["total_quantity"], Decimal("3"))

    def test_repack_document_creates_child_batch_and_traceability(self) -> None:
        source_batch = self.receive_available_batch("10")
        target_product = self.service.create_product(
            ProductCreate(
                name="Физраствор 100 мл",
                sku="NACL-100",
                unit="флакон",
                category_id=self.category["id"],
            )
        )
        document = self.service.create_repack_document(
            RepackDocumentCreate(
                warehouse_id=self.warehouse["id"],
                lines=[
                    RepackDocumentLineCreate(
                        batch_id=source_batch["id"],
                        target_product_id=target_product["id"],
                        quantity=Decimal("2"),
                        target_quantity=Decimal("38"),
                        conversion_factor=Decimal("20"),
                        loss_quantity=Decimal("0.1"),
                        target_lot="PACK-1",
                        reason="Фасовка во флаконы 100 мл",
                    )
                ],
            ),
            actor_id="manager",
        )

        self.assertEqual(document["status"], "draft")
        source_before = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        self.assertEqual(source_before["total_quantity"], Decimal("10"))

        posted = self.service.post_stock_document(document["id"], actor_id="manager")
        source_after = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        target_balance = self.service.list_balances(
            target_product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        transformations = self.service.list_batch_transformations(
            batch_id=source_batch["id"],
        )
        source_trace = self.service.get_batch_traceability(source_batch["id"])
        target_trace = self.service.get_batch_traceability(target_balance["batch_id"])

        self.assertEqual(posted["status"], "posted")
        self.assertEqual(source_after["total_quantity"], Decimal("8"))
        self.assertEqual(target_balance["total_quantity"], Decimal("38"))
        self.assertEqual(transformations[0]["source_batch_id"], source_batch["id"])
        self.assertEqual(transformations[0]["target_batch_id"], target_balance["batch_id"])
        self.assertEqual(transformations[0]["loss_quantity"], "0.1")
        self.assertEqual(source_trace["transformations"][0]["target_batch_id"], target_balance["batch_id"])
        self.assertEqual(target_trace["transformations"][0]["source_batch_id"], source_batch["id"])
        movement_types = [row["movement_type"] for row in self.service.list_stock_movements(limit=20)]
        self.assertIn("repack_out", movement_types)
        self.assertIn("repack_in", movement_types)

        print_form = self.service.get_repack_print_form(document["id"])

        self.assertEqual(print_form["document_id"], document["id"])
        self.assertEqual(print_form["status"], "posted")
        self.assertEqual(print_form["warehouse_name"], "Основной склад")
        self.assertEqual(print_form["lines"][0]["target_batch_id"], target_balance["batch_id"])
        self.assertIn("Физраствор", print_form["csv"])
        self.assertIn("PACK-1", print_form["csv"])
        self.assertIn("38", print_form["csv"])

    def test_repack_document_rolls_back_when_source_stock_is_not_enough(self) -> None:
        source_batch = self.receive_available_batch("1")
        target_product = self.service.create_product(
            ProductCreate(
                name="Физраствор фасованный",
                sku="NACL-PACK",
                unit="пакет",
                category_id=self.category["id"],
            )
        )
        document = self.service.create_repack_document(
            RepackDocumentCreate(
                warehouse_id=self.warehouse["id"],
                lines=[
                    RepackDocumentLineCreate(
                        batch_id=source_batch["id"],
                        target_product_id=target_product["id"],
                        quantity=Decimal("2"),
                        target_quantity=Decimal("20"),
                        conversion_factor=Decimal("10"),
                        loss_quantity=Decimal("0"),
                        target_lot="PACK-FAIL",
                    )
                ],
            )
        )

        with self.assertRaises(InsufficientStockError):
            self.service.post_stock_document(document["id"])

        source_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        self.assertEqual(source_balance["total_quantity"], Decimal("1"))
        self.assertEqual(self.service.list_balances(target_product["id"]), [])
        self.assertEqual(self.service.count_batch_transformations(), 0)
        self.assertEqual(self.service.get_stock_document(document["id"])["status"], "draft")

    def test_department_return_document_moves_stock_back_to_main_warehouse(self) -> None:
        batch = self.receive_available_batch("10")
        cabinet = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=cabinet["id"],
                quantity=Decimal("4"),
            )
        )
        document = self.service.create_department_return_document(
            DepartmentReturnDocumentCreate(
                source_warehouse_id=cabinet["id"],
                lines=[
                    DepartmentReturnDocumentLineCreate(
                        batch_id=batch["id"],
                        target_warehouse_id=self.warehouse["id"],
                        quantity=Decimal("1.5"),
                        reason="Не использовали",
                    )
                ],
            )
        )

        self.service.post_stock_document(document["id"])

        main_balance = self.service.list_balances(
            self.product["id"], warehouse_id=self.warehouse["id"]
        )[0]
        cabinet_balance = self.service.list_balances(
            self.product["id"], warehouse_id=cabinet["id"]
        )[0]
        self.assertEqual(main_balance["total_quantity"], Decimal("7.5"))
        self.assertEqual(cabinet_balance["total_quantity"], Decimal("2.5"))

    def test_supplier_return_document_reduces_free_stock(self) -> None:
        batch = self.receive_available_batch("10")
        document = self.service.create_supplier_return_document(
            SupplierReturnDocumentCreate(
                warehouse_id=self.warehouse["id"],
                supplier_id=self.supplier["id"],
                lines=[
                    SupplierReturnDocumentLineCreate(
                        batch_id=batch["id"],
                        quantity=Decimal("3"),
                        reason="Брак",
                    )
                ],
            )
        )

        self.service.post_stock_document(document["id"])

        balance = self.service.list_balances(self.product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("7"))

    def test_supplier_return_document_requires_original_supplier(self) -> None:
        batch = self.receive_available_batch("10")
        other_supplier = self.service.create_supplier(SupplierCreate(name="Другой поставщик"))
        document = self.service.create_supplier_return_document(
            SupplierReturnDocumentCreate(
                warehouse_id=self.warehouse["id"],
                supplier_id=other_supplier["id"],
                lines=[
                    SupplierReturnDocumentLineCreate(
                        batch_id=batch["id"],
                        quantity=Decimal("1"),
                        reason="Брак",
                    )
                ],
            )
        )

        with self.assertRaises(ValidationError):
            self.service.post_stock_document(document["id"])

        balance = self.service.list_balances(self.product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("10"))
        self.assertEqual(self.service.get_stock_document(document["id"])["status"], "draft")

    def test_writeoff_document_rolls_back_when_any_line_fails(self) -> None:
        batch = self.receive_available_batch("5")
        document = self.service.create_writeoff_document(
            WriteOffDocumentCreate(
                warehouse_id=self.warehouse["id"],
                lines=[
                    WriteOffDocumentLineCreate(
                        batch_id=batch["id"],
                        quantity=Decimal("2"),
                        reason="Строка успешна",
                    ),
                    WriteOffDocumentLineCreate(
                        batch_id=batch["id"],
                        quantity=Decimal("10"),
                        reason="Строка должна сорвать документ",
                    ),
                ],
            )
        )

        with self.assertRaises(InsufficientStockError):
            self.service.post_stock_document(document["id"])

        balance = self.service.list_balances(self.product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("5"))
        self.assertEqual(self.service.get_stock_document(document["id"])["status"], "draft")

    def test_controlled_writeoff_document_posting_requires_patient_doctor_record_and_second_approver(self) -> None:
        batch = self.receive_controlled_batch("5")
        document = self.service.create_writeoff_document(
            WriteOffDocumentCreate(
                warehouse_id=self.warehouse["id"],
                lines=[
                    WriteOffDocumentLineCreate(
                        batch_id=batch["id"],
                        quantity=Decimal("1"),
                        reason="Выдача пациенту",
                        patient_id="patient-1",
                        doctor_id="doctor-1",
                    )
                ],
            )
        )

        with self.assertRaises(ValidationError):
            self.service.post_stock_document(document["id"])

        balance = self.service.list_balances(batch["product_id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("5"))
        self.assertEqual(self.service.get_stock_document(document["id"])["status"], "draft")

        valid_document = self.service.create_writeoff_document(
            WriteOffDocumentCreate(
                warehouse_id=self.warehouse["id"],
                lines=[
                    WriteOffDocumentLineCreate(
                        batch_id=batch["id"],
                        quantity=Decimal("1"),
                        reason="Выдача пациенту",
                        patient_id="patient-1",
                        doctor_id="doctor-1",
                        medical_record_no="MR-1",
                        second_approver_id="head-nurse-1",
                        second_approval_note="Подтверждено комиссией",
                    )
                ],
            )
        )

        self.service.post_stock_document(valid_document["id"])
        ledger = self.service.list_controlled_substance_ledger(batch_id=batch["id"])
        writeoff = next(row for row in ledger if row["movement_type"] == "write_off")
        self.assertEqual(writeoff["second_approver_id"], "head-nurse-1")
        self.assertEqual(writeoff["second_approval_note"], "Подтверждено комиссией")

        balance = self.service.list_balances(batch["product_id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("4"))

    def test_low_stock_notification_is_created_once_until_read(self) -> None:
        self.receive_available_batch("3")

        first = self.service.generate_low_stock_notifications()
        second = self.service.generate_low_stock_notifications()

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(first[0]["id"], second[0]["id"])
        self.assertIn("Низкий остаток", first[0]["title"])

    def test_low_stock_notification_includes_product_without_stock(self) -> None:
        notifications = self.service.generate_low_stock_notifications()

        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]["product_id"], self.product["id"])
        self.assertEqual(notifications[0]["warehouse_id"], self.warehouse["id"])
        self.assertIn("Свободный остаток", notifications[0]["message"])
        self.assertIn("ниже точки заказа", notifications[0]["message"])

    def test_read_low_stock_notification_allows_new_reminder(self) -> None:
        self.receive_available_batch("3")
        notification = self.service.generate_low_stock_notifications()[0]

        self.service.mark_notification_read(notification["id"])
        new_notification = self.service.generate_low_stock_notifications()[0]

        self.assertNotEqual(notification["id"], new_notification["id"])
        self.assertEqual(len(self.service.list_notifications(unread_only=True)), 1)

    def test_low_stock_notifications_are_scoped_per_warehouse(self) -> None:
        batch = self.receive_available_batch("12")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("3"),
            )
        )

        first = self.service.generate_low_stock_notifications()
        second = self.service.generate_low_stock_notifications()

        self.assertEqual(
            {notification["warehouse_id"] for notification in first},
            {self.warehouse["id"], target["id"]},
        )
        self.assertEqual({notification["id"] for notification in first}, {n["id"] for n in second})
        self.assertEqual(
            self.service.count_notifications(unread_only=True, warehouse_id=target["id"]), 1
        )
        self.assertEqual(
            len(self.service.list_notifications(unread_only=True, warehouse_id=target["id"])), 1
        )

    def test_read_low_stock_notification_allows_new_reminder_only_for_same_warehouse(self) -> None:
        batch = self.receive_available_batch("12")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("3"),
            )
        )
        notifications = self.service.generate_low_stock_notifications()
        target_notification = next(
            notification for notification in notifications if notification["warehouse_id"] == target["id"]
        )

        self.service.mark_notification_read(target_notification["id"])
        refreshed = self.service.generate_low_stock_notifications(warehouse_id=target["id"])

        self.assertEqual(len(refreshed), 1)
        self.assertNotEqual(refreshed[0]["id"], target_notification["id"])
        self.assertEqual(self.service.count_notifications(unread_only=True), 2)
        self.assertEqual(
            self.service.count_notifications(unread_only=True, warehouse_id=target["id"]), 1
        )

    def test_expiry_notification_is_created_once_until_read(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="EXP-1",
                expires_on=datetime.now(UTC).date() + timedelta(days=10),
                quarantine=False,
            )
        )

        first = self.service.generate_expiry_notifications(days=30)
        second = self.service.generate_expiry_notifications(days=30)

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(first[0]["id"], second[0]["id"])
        self.assertEqual(first[0]["notification_type"], "expiry")
        self.assertEqual(first[0]["batch_id"], batch["id"])
        self.assertEqual(first[0]["warehouse_id"], self.warehouse["id"])
        self.assertIn("Скоро истекает срок", first[0]["title"])

    def test_expiry_notification_includes_expired_batch(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="EXPIRED-1",
                expires_on=datetime.now(UTC).date() - timedelta(days=2),
                quarantine=False,
            )
        )

        notifications = self.service.generate_expiry_notifications(days=30)

        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]["batch_id"], batch["id"])
        self.assertIn("Просрочен срок", notifications[0]["title"])
        self.assertIn("Просрочено дней", notifications[0]["message"])

    def test_read_expiry_notification_allows_new_reminder(self) -> None:
        self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="EXP-2",
                expires_on=datetime.now(UTC).date() + timedelta(days=7),
                quarantine=False,
            )
        )
        notification = self.service.generate_expiry_notifications(days=30)[0]

        self.service.mark_notification_read(notification["id"])
        new_notification = self.service.generate_expiry_notifications(days=30)[0]

        self.assertNotEqual(notification["id"], new_notification["id"])
        self.assertEqual(len(self.service.list_notifications(unread_only=True)), 1)

    def test_expiry_notifications_are_scoped_per_warehouse(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("10"),
                unit_price=Decimal("100"),
                lot="EXP-MULTI",
                expires_on=datetime.now(UTC).date() + timedelta(days=5),
                quarantine=False,
            )
        )
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("3"),
            )
        )

        all_notifications = self.service.generate_expiry_notifications(days=30)
        scoped_notifications = self.service.generate_expiry_notifications(
            days=30, warehouse_id=target["id"]
        )

        self.assertEqual(
            {notification["warehouse_id"] for notification in all_notifications},
            {self.warehouse["id"], target["id"]},
        )
        self.assertEqual(len(scoped_notifications), 1)
        self.assertEqual(scoped_notifications[0]["warehouse_id"], target["id"])

    def test_expiry_notifications_ignore_far_future_non_expiring_and_empty_stock(self) -> None:
        far_future = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="FAR",
                expires_on=datetime.now(UTC).date() + timedelta(days=90),
                quarantine=False,
            )
        )
        self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="NO-EXP",
                quarantine=False,
            )
        )
        soon_empty = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("2"),
                unit_price=Decimal("100"),
                lot="EMPTY",
                expires_on=datetime.now(UTC).date() + timedelta(days=3),
                quarantine=False,
            )
        )
        self.service.write_off(
            WriteOffCreate(
                batch_id=soon_empty["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("2"),
                reason="Израсходовано",
            )
        )

        notifications = self.service.generate_expiry_notifications(days=30)

        self.assertEqual(notifications, [])
        self.assertNotIn(far_future["id"], [row.get("batch_id") for row in notifications])

    def test_expiry_notifications_reject_negative_days(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.generate_expiry_notifications(days=-1)

    def test_quarantine_notification_is_created_for_old_quarantine_batch_once(self) -> None:
        batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="Q-OLD",
                quarantine=True,
            )
        )
        old_received_at = (datetime.now(UTC) - timedelta(days=5)).isoformat()
        with self.database.transaction() as connection:
            connection.execute(
                "UPDATE batches SET received_at = ? WHERE id = ?",
                (old_received_at, batch["id"]),
            )

        first = self.service.generate_quarantine_notifications(days=3)
        second = self.service.generate_quarantine_notifications(days=3)

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(first[0]["id"], second[0]["id"])
        self.assertEqual(first[0]["notification_type"], "quarantine")
        self.assertEqual(first[0]["batch_id"], batch["id"])
        self.assertIn("Партия в карантине", first[0]["title"])

    def test_quarantine_notifications_reject_negative_days(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.generate_quarantine_notifications(days=-1)

    def test_abc_xyz_analysis_classifies_consumption_and_reorder_need(self) -> None:
        primary_batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("20"),
                unit_price=Decimal("100"),
                lot="ABC-A",
                quarantine=False,
            )
        )
        secondary = self.service.create_product(
            ProductCreate(
                name="Перчатки",
                sku="GLV-001",
                unit="пара",
                category_id=self.category["id"],
                reorder_point=Decimal("5"),
                safety_stock=Decimal("2"),
            )
        )
        secondary_batch = self.service.receive(
            ReceiptCreate(
                product_id=secondary["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("10"),
                unit_price=Decimal("10"),
                lot="ABC-C",
                quarantine=False,
            )
        )
        self.service.write_off(
            WriteOffCreate(
                batch_id=primary_batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("16"),
                reason="Расход",
            )
        )
        self.service.write_off(
            WriteOffCreate(
                batch_id=secondary_batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("2"),
                reason="Расход",
            )
        )

        analysis = self.service.abc_xyz_analysis(analysis_days=90)
        rows = {row["product_id"]: row for row in analysis["items"]}

        self.assertEqual(analysis["analysis_days"], 90)
        self.assertEqual(rows[self.product["id"]]["abc_class"], "A")
        self.assertEqual(rows[self.product["id"]]["xyz_class"], "Z")
        self.assertEqual(rows[self.product["id"]]["consumption_quantity"], "16")
        self.assertEqual(rows[self.product["id"]]["consumption_value"], "1600")
        self.assertEqual(rows[self.product["id"]]["current_free_quantity"], "4")
        self.assertEqual(rows[self.product["id"]]["recommended_order_quantity"], "6")
        self.assertEqual(rows[self.product["id"]]["recommendation"], "Заказать в первую очередь")
        self.assertEqual(rows[secondary["id"]]["abc_class"], "C")

    def test_abc_xyz_analysis_can_be_limited_to_warehouse(self) -> None:
        batch = self.receive_available_batch("12")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("5"),
            )
        )

        source_analysis = self.service.abc_xyz_analysis(
            analysis_days=90, warehouse_id=self.warehouse["id"]
        )
        target_analysis = self.service.abc_xyz_analysis(
            analysis_days=90, warehouse_id=target["id"]
        )
        source_row = next(row for row in source_analysis["items"] if row["product_id"] == self.product["id"])
        target_row = next(row for row in target_analysis["items"] if row["product_id"] == self.product["id"])

        self.assertEqual(source_analysis["warehouse_id"], self.warehouse["id"])
        self.assertEqual(target_analysis["warehouse_id"], target["id"])
        self.assertEqual(source_row["consumption_quantity"], "5")
        self.assertEqual(target_row["consumption_quantity"], "0")
        self.assertEqual(target_row["current_free_quantity"], "5")

    def test_abc_xyz_analysis_rejects_invalid_period(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.abc_xyz_analysis(analysis_days=0)

    def test_abc_xyz_snapshot_history_persists_analysis_items(self) -> None:
        batch = self.receive_available_batch("12")
        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("3"),
                reason="Расход",
            )
        )

        run = self.service.save_abc_xyz_analysis_snapshot(
            analysis_days=90,
            warehouse_id=self.warehouse["id"],
            actor_id="analyst",
        )
        listed = self.service.list_abc_xyz_runs(warehouse_id=self.warehouse["id"])
        detail = self.service.get_abc_xyz_run(run["id"])

        self.assertEqual(run["warehouse_id"], self.warehouse["id"])
        self.assertEqual(run["source"], "manual")
        self.assertEqual(run["status"], "succeeded")
        self.assertEqual(run["items_count"], len(run["items"]))
        self.assertEqual(self.service.count_abc_xyz_runs(warehouse_id=self.warehouse["id"]), 1)
        self.assertEqual(listed[0]["id"], run["id"])
        product_row = next(row for row in detail["items"] if row["product_id"] == self.product["id"])
        self.assertEqual(product_row["consumption_quantity"], "3")
        self.assertEqual(product_row["current_free_quantity"], "9")

    def test_monthly_abc_xyz_snapshot_does_not_create_duplicate_for_same_period(self) -> None:
        first = self.service.save_monthly_abc_xyz_analysis_snapshot(actor_id="scheduler")
        second = self.service.save_monthly_abc_xyz_analysis_snapshot(actor_id="scheduler")

        self.assertEqual(first["id"], second["id"])
        self.assertEqual(first["source"], "background")
        self.assertEqual(self.service.count_abc_xyz_runs(), 1)

    def test_fefo_writeoff_uses_earliest_expiring_batches_first(self) -> None:
        late_batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("100"),
                lot="LATE",
                expires_on=date(2028, 1, 1),
                quarantine=False,
            )
        )
        early_batch = self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("4"),
                unit_price=Decimal("100"),
                lot="EARLY",
                expires_on=date(2027, 1, 1),
                quarantine=False,
            )
        )

        result = self.service.write_off_fefo(
            WriteOffFefoCreate(
                product_id=self.product["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("6"),
                reason="FEFO списание",
            )
        )
        balances = {row["batch_id"]: row for row in self.service.list_balances(self.product["id"])}

        self.assertEqual(len(result["movement_ids"]), 2)
        self.assertEqual(balances[early_batch["id"]]["total_quantity"], Decimal("0"))
        self.assertEqual(balances[late_batch["id"]]["total_quantity"], Decimal("3"))

    def test_controlled_fefo_writeoff_requires_patient_doctor_and_record(self) -> None:
        product = self.create_controlled_product()
        self.service.receive(
            ReceiptCreate(
                product_id=product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("5"),
                unit_price=Decimal("1000"),
                lot="CTRL-FEFO-1",
                expires_on=date(2027, 1, 1),
                quarantine=False,
            )
        )

        with self.assertRaises(ValidationError):
            self.service.write_off_fefo(
                WriteOffFefoCreate(
                    product_id=product["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="FEFO выдача пациенту",
                    patient_id="patient-1",
                    doctor_id=" ",
                    medical_record_no="MR-1",
                )
            )

        balance = self.service.list_balances(product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("5"))

    def test_fefo_writeoff_rolls_back_when_total_stock_is_not_enough(self) -> None:
        self.receive_available_batch("2")

        with self.assertRaises(InsufficientStockError):
            self.service.write_off_fefo(
                WriteOffFefoCreate(
                    product_id=self.product["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("3"),
                    reason="Недостаточно остатков",
                )
            )

        balance = self.service.list_balances(self.product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("2"))

    def test_release_reservation_restores_free_balance(self) -> None:
        batch = self.receive_available_batch("10")
        reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("6"),
                reserved_for="Операционный день",
            )
        )

        released = self.service.release_reservation(reservation["id"])
        balance = self.service.list_balances(self.product["id"])[0]

        self.assertEqual(released["status"], "released")
        self.assertEqual(balance["reserved_quantity"], Decimal("0"))
        self.assertEqual(balance["free_quantity"], Decimal("10"))

    def test_use_reservation_writes_off_reserved_quantity_once(self) -> None:
        batch = self.receive_available_batch("10")
        reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("6"),
                reserved_for="Операционный день",
            )
        )

        used = self.service.use_reservation(
            reservation["id"],
            ReservationUseCreate(reason="Выдача из резерва"),
        )
        used_again = self.service.use_reservation(
            reservation["id"],
            ReservationUseCreate(reason="Повторная выдача"),
        )
        balance = self.service.list_balances(self.product["id"])[0]
        movements = self.service.list_stock_movements(batch_id=batch["id"])
        write_off_movements = [
            movement for movement in movements if movement["movement_type"] == "write_off"
        ]

        self.assertEqual(used["status"], "used")
        self.assertEqual(used_again["status"], "used")
        self.assertEqual(balance["total_quantity"], Decimal("4"))
        self.assertEqual(balance["reserved_quantity"], Decimal("0"))
        self.assertEqual(balance["free_quantity"], Decimal("4"))
        self.assertEqual(len(write_off_movements), 1)
        self.assertEqual(write_off_movements[0]["quantity"], "6")
        self.assertEqual(write_off_movements[0]["reason"], "Выдача из резерва")

    def test_controlled_reservation_use_requires_patient_doctor_and_record(self) -> None:
        batch = self.receive_controlled_batch("5")
        reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("2"),
                reserved_for="Пациент #42",
            )
        )

        with self.assertRaises(ValidationError):
            self.service.use_reservation(
                reservation["id"],
                ReservationUseCreate(
                    reason="Выдача ПКУ из резерва",
                    patient_id="patient-1",
                    doctor_id="doctor-1",
                ),
            )

        balance = self.service.list_balances(batch["product_id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("5"))
        self.assertEqual(balance["reserved_quantity"], Decimal("2"))

        used = self.service.use_reservation(
            reservation["id"],
            ReservationUseCreate(
                reason="Выдача ПКУ из резерва",
                patient_id="patient-1",
                doctor_id="doctor-1",
                medical_record_no="MR-1",
                second_approver_id="head-nurse-1",
                second_approval_note="Сверено по резерву",
            ),
        )

        balance = self.service.list_balances(batch["product_id"])[0]
        self.assertEqual(used["status"], "used")
        self.assertEqual(balance["total_quantity"], Decimal("3"))
        self.assertEqual(balance["reserved_quantity"], Decimal("0"))

    def test_expire_reservations_releases_only_overdue_reserves(self) -> None:
        batch = self.receive_available_batch("10")
        overdue = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("3"),
                reserved_for="Просроченный резерв",
                expires_at=datetime.now(UTC) - timedelta(hours=1),
            )
        )
        active = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("2"),
                reserved_for="Будущий резерв",
                expires_at=datetime.now(UTC) + timedelta(hours=1),
            )
        )

        expired = self.service.expire_reservations(now=datetime.now(UTC))
        balance = self.service.list_balances(self.product["id"])[0]

        self.assertEqual([row["id"] for row in expired], [overdue["id"]])
        self.assertEqual(self.service.get_reservation(active["id"])["status"], "reserved")
        self.assertEqual(balance["reserved_quantity"], Decimal("2"))

    def test_expire_reservations_can_be_limited_to_warehouse(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("4"),
            )
        )
        main_reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("3"),
                reserved_for="Основной склад",
                expires_at=datetime.now(UTC) - timedelta(hours=1),
            )
        )
        target_reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=target["id"],
                quantity=Decimal("2"),
                reserved_for="Кабинет",
                expires_at=datetime.now(UTC) - timedelta(hours=1),
            )
        )

        expired = self.service.expire_reservations(
            now=datetime.now(UTC), warehouse_id=target["id"]
        )

        self.assertEqual([row["id"] for row in expired], [target_reservation["id"]])
        self.assertEqual(self.service.get_reservation(main_reservation["id"])["status"], "reserved")
        self.assertEqual(self.service.get_reservation(target_reservation["id"])["status"], "released")

    def test_expire_reservations_without_filter_keeps_global_behavior(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("4"),
            )
        )
        main_reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("3"),
                reserved_for="Основной склад",
                expires_at=datetime.now(UTC) - timedelta(hours=1),
            )
        )
        target_reservation = self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=target["id"],
                quantity=Decimal("2"),
                reserved_for="Кабинет",
                expires_at=datetime.now(UTC) - timedelta(hours=1),
            )
        )

        expired = self.service.expire_reservations(now=datetime.now(UTC))

        self.assertEqual(
            {row["id"] for row in expired},
            {main_reservation["id"], target_reservation["id"]},
        )

    def test_audit_log_records_write_operations(self) -> None:
        batch = self.receive_available_batch("5")
        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("1"),
                reason="Проверка аудита",
            ),
            actor_id="nurse-1",
        )

        audit_log = self.service.list_audit_log(limit=20)

        self.assertTrue(any(row["action"] == "write_off" for row in audit_log))
        self.assertTrue(any(row["actor_id"] == "nurse-1" for row in audit_log))

    def test_audit_log_can_be_filtered_by_actor_and_action(self) -> None:
        self.service.update_category(
            self.category["id"],
            CategoryUpdate(name="Аудит категории"),
            actor_id="manager-1",
        )
        self.service.update_supplier(
            self.supplier["id"],
            SupplierUpdate(name="Поставщик аудит", bin=None, phone=None),
            actor_id="manager-2",
        )

        manager_updates = self.service.list_audit_log(
            actor_id="manager-1",
            action="update",
            limit=20,
        )

        self.assertEqual(len(manager_updates), 1)
        self.assertEqual(manager_updates[0]["actor_id"], "manager-1")
        self.assertEqual(manager_updates[0]["action"], "update")
        self.assertEqual(self.service.count_audit_log(actor_id="manager-1", action="update"), 1)

    def test_audit_log_can_be_filtered_by_warehouse_and_redacts_sensitive_payload(self) -> None:
        batch = self.receive_available_batch("10")
        target = self.service.create_warehouse(WarehouseCreate(name="Кабинет 101"))
        self.service.transfer(
            TransferCreate(
                batch_id=batch["id"],
                source_warehouse_id=self.warehouse["id"],
                target_warehouse_id=target["id"],
                quantity=Decimal("4"),
            )
        )
        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=target["id"],
                quantity=Decimal("1"),
                reason="Выдача пациенту",
                patient_id="patient-42",
                doctor_id="doctor-7",
                medical_record_no="MR-99",
            ),
            actor_id="nurse-1",
        )

        target_audit_log = self.service.list_audit_log(warehouse_id=target["id"], limit=20)

        self.assertTrue(target_audit_log)
        self.assertTrue(all(row["warehouse_id"] == target["id"] for row in target_audit_log))
        write_off_entry = next(row for row in target_audit_log if row["action"] == "write_off")
        self.assertEqual(write_off_entry["payload"]["patient_id"], "***")
        self.assertEqual(write_off_entry["payload"]["doctor_id"], "***")
        self.assertEqual(write_off_entry["payload"]["medical_record_no"], "***")
        self.assertEqual(self.service.count_audit_log(warehouse_id=target["id"]), len(target_audit_log))

    def test_inventory_session_locks_warehouse_and_posts_shortage(self) -> None:
        batch = self.receive_available_batch("10")
        session = self.service.create_inventory_session(
            InventoryCreate(warehouse_id=self.warehouse["id"]),
            actor_id="manager-1",
        )
        line = session["lines"][0]

        with self.assertRaises(InventoryLockedError):
            self.service.write_off(
                WriteOffCreate(
                    batch_id=batch["id"],
                    warehouse_id=self.warehouse["id"],
                    quantity=Decimal("1"),
                    reason="Обычное движение во время инвентаризации",
                )
            )

        self.service.update_inventory_line_count(
            session["id"],
            line["id"],
            InventoryLineCountUpdate(actual_quantity=Decimal("7")),
        )
        posted = self.service.post_inventory_session(session["id"], actor_id="manager-1")
        balance = self.service.list_balances(self.product["id"])[0]

        self.assertEqual(posted["status"], InventoryStatus.POSTED)
        self.assertEqual(posted["summary"]["total_lines"], 1)
        self.assertEqual(posted["summary"]["filled_lines"], 1)
        self.assertEqual(posted["summary"]["shortage_lines"], 1)
        self.assertEqual(posted["summary"]["total_shortage_quantity"], Decimal("3"))
        self.assertEqual(balance["total_quantity"], Decimal("7"))
        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("1"),
                reason="После инвентаризации можно",
            )
        )

    def test_inventory_print_form_contains_count_sheet_and_reconciliation_csv(self) -> None:
        self.receive_available_batch("10")
        session = self.service.create_inventory_session(
            InventoryCreate(warehouse_id=self.warehouse["id"]),
            actor_id="manager-1",
        )
        line = session["lines"][0]
        self.service.update_inventory_line_count(
            session["id"],
            line["id"],
            InventoryLineCountUpdate(actual_quantity=Decimal("7")),
        )

        form = self.service.get_inventory_print_form(session["id"])

        self.assertEqual(form["warehouse_name"], "Основной склад")
        self.assertEqual(form["summary"]["shortage_lines"], 1)
        self.assertEqual(form["lines"][0]["product_name"], "Физраствор")
        self.assertIn("Товар;SKU;Ед.;Партия;Срок годности;Ожидается;Факт", form["count_sheet_csv"])
        self.assertIn("Физраствор;NACL-001;флакон;LOT-1;2027-01-01;10;", form["count_sheet_csv"])
        self.assertIn("Расхождение", form["reconciliation_csv"])
        self.assertIn("Физраствор;NACL-001;флакон;LOT-1;2027-01-01;10;7;-3", form["reconciliation_csv"])

    def test_inventory_session_filters_categories_and_stores_responsibles(self) -> None:
        self.receive_available_batch("10")
        second_category = self.service.create_category(CategoryCreate(name="Расходники"))
        second_product = self.service.create_product(
            ProductCreate(
                name="Перчатки",
                sku="GLV-001",
                unit="пара",
                category_id=second_category["id"],
            )
        )
        self.service.receive(
            ReceiptCreate(
                product_id=second_product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("3"),
                unit_price=Decimal("15"),
                lot="GLV-LOT",
                expires_on=None,
                quarantine=False,
            )
        )

        session = self.service.create_inventory_session(
            InventoryCreate(
                warehouse_id=self.warehouse["id"],
                category_ids=[second_category["id"]],
                responsible_ids=["head-nurse", "head-nurse", "manager"],
            ),
            actor_id="manager-1",
        )

        self.assertEqual(session["category_ids"], [second_category["id"]])
        self.assertEqual(session["responsible_ids"], ["head-nurse", "manager"])
        self.assertEqual(len(session["lines"]), 1)
        self.assertEqual(session["lines"][0]["product_id"], second_product["id"])

    def test_controlled_substance_ledger_export_contains_required_fields(self) -> None:
        batch = self.receive_controlled_batch("2")
        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("1"),
                reason="Назначение врача",
                patient_id="patient-1",
                doctor_id="doctor-1",
                medical_record_no="MR-1",
                second_approver_id="head-nurse",
            )
        )

        export = self.service.export_controlled_substance_ledger(warehouse_id=self.warehouse["id"])

        self.assertEqual(export["filename"], "sklad-controlled-substances-ledger.csv")
        self.assertIn("Пациент", export["csv"])
        self.assertIn("patient-1", export["csv"])
        self.assertIn("head-nurse", export["csv"])

    def test_inventory_session_posts_surplus(self) -> None:
        self.receive_available_batch("10")
        session = self.service.create_inventory_session(
            InventoryCreate(warehouse_id=self.warehouse["id"])
        )
        line = session["lines"][0]

        self.service.update_inventory_line_count(
            session["id"],
            line["id"],
            InventoryLineCountUpdate(actual_quantity=Decimal("12.5")),
        )
        self.service.post_inventory_session(session["id"])
        balance = self.service.list_balances(self.product["id"])[0]

        self.assertEqual(balance["total_quantity"], Decimal("12.5"))

    def test_inventory_post_rejects_actual_below_reserved_quantity(self) -> None:
        batch = self.receive_available_batch("10")
        self.service.reserve(
            ReservationCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("6"),
                reserved_for="Операционный день",
            )
        )
        session = self.service.create_inventory_session(
            InventoryCreate(warehouse_id=self.warehouse["id"])
        )
        line = session["lines"][0]
        self.service.update_inventory_line_count(
            session["id"],
            line["id"],
            InventoryLineCountUpdate(actual_quantity=Decimal("5")),
        )

        with self.assertRaises(ValidationError):
            self.service.post_inventory_session(session["id"])

        balance = self.service.list_balances(self.product["id"])[0]
        self.assertEqual(balance["total_quantity"], Decimal("10"))
        self.assertEqual(balance["reserved_quantity"], Decimal("6"))

    def test_cancel_inventory_session_unlocks_warehouse_without_adjustments(self) -> None:
        batch = self.receive_available_batch("10")
        session = self.service.create_inventory_session(
            InventoryCreate(warehouse_id=self.warehouse["id"])
        )
        line = session["lines"][0]
        self.service.update_inventory_line_count(
            session["id"],
            line["id"],
            InventoryLineCountUpdate(actual_quantity=Decimal("1")),
        )

        cancelled = self.service.cancel_inventory_session(session["id"])
        balance = self.service.list_balances(self.product["id"])[0]

        self.assertEqual(cancelled["status"], InventoryStatus.CANCELLED)
        self.assertEqual(balance["total_quantity"], Decimal("10"))
        self.service.write_off(
            WriteOffCreate(
                batch_id=batch["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("1"),
                reason="После отмены можно",
            )
        )



    def test_generate_supplier_contract_expiry_notifications(self) -> None:
        from app.domain.schemas import SupplierCreate
        from datetime import date, timedelta
        today = date.today()
        expiring_soon = self.service.create_supplier(
            SupplierCreate(name="Скоро истекает", contract_expires_on=today + timedelta(days=10))
        )
        expiring_far = self.service.create_supplier(
            SupplierCreate(name="Не скоро", contract_expires_on=today + timedelta(days=60))
        )
        notifs = self.service.generate_supplier_contract_expiry_notifications(days=30)
        types = [n["notification_type"] for n in notifs]
        titles = [n["title"] for n in notifs]
        self.assertTrue(all(t == "supplier_contract_expiry" for t in types))
        self.assertTrue(any("Скоро истекает" in title for title in titles))
        self.assertFalse(any("Не скоро" in title for title in titles))
        # Duplicate call should not create new notifications (idempotent)
        notifs2 = self.service.generate_supplier_contract_expiry_notifications(days=30)
        self.assertEqual(len(notifs), len(notifs2))
        # Negative days should raise
        with self.assertRaises(Exception):
            self.service.generate_supplier_contract_expiry_notifications(days=-1)

    def test_create_grafana_alert_notification_stores_and_retrieves(self) -> None:
        result = self.service.create_grafana_alert_notification(
            title="[CRITICAL] DiskFull — firing",
            message="Диск заполнен более чем на 95%",
            severity="critical",
        )
        self.assertEqual(result["notification_type"], "grafana_alert")
        self.assertEqual(result["title"], "[CRITICAL] DiskFull — firing")
        self.assertEqual(result["message"], "Диск заполнен более чем на 95%")
        self.assertFalse(result["is_read"])
        self.assertIsNone(result["warehouse_id"])
        # Long title/message are truncated
        long = self.service.create_grafana_alert_notification(
            title="x" * 300,
            message="y" * 2000,
        )
        self.assertLessEqual(len(long["title"]), 255)
        self.assertLessEqual(len(long["message"]), 1000)
        # Appears in list_notifications
        items = self.service.list_notifications()
        types = [i["notification_type"] for i in items]
        self.assertIn("grafana_alert", types)


class MisProcedureIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.database = SQLiteDatabase(":memory:")
        self.database.init_schema()
        self.service = WarehouseService(self.database)
        self.category = self.service.create_category(CategoryCreate(name="Медикаменты"))
        self.supplier = self.service.create_supplier(SupplierCreate(name="ТОО Поставщик"))
        self.warehouse = self.service.create_warehouse(
            WarehouseCreate(name="Кабинет 101", mis_clinic_id="clinic-1", mis_room_id="room-101")
        )
        self.product = self.service.create_product(
            ProductCreate(
                name="Шприц 5 мл",
                sku="SYR-005",
                unit="шт",
                category_id=self.category["id"],
            )
        )
        self.service.receive(
            ReceiptCreate(
                product_id=self.product["id"],
                supplier_id=self.supplier["id"],
                warehouse_id=self.warehouse["id"],
                quantity=Decimal("10"),
                unit_price=Decimal("100"),
                lot="LOT-1",
                expires_on=date(2027, 1, 1),
                quarantine=False,
            )
        )
        self.template = self.service.create_procedure_consumption_template(
            {
                "mis_clinic_id": "clinic-1",
                "service_code": "INJECTION",
                "name": "Внутримышечная инъекция",
                "items": [{"product_id": self.product["id"], "quantity": "2"}],
            },
            actor_id="admin",
        )

    def test_procedure_event_writes_off_stock(self) -> None:
        result = self.service.process_mis_procedure_event(
            mis_clinic_id="clinic-1",
            mis_room_id="room-101",
            service_code="INJECTION",
            mis_event_id="evt-1",
            patient_id="patient-1",
            doctor_id="doctor-1",
            medical_record_no="mr-1",
        )
        self.assertEqual(result["status"], "processed")
        self.assertEqual(result["warehouse_id"], self.warehouse["id"])
        balances = self.service.list_balances(self.product["id"])
        self.assertEqual(balances[0]["free_quantity"], Decimal("8"))

    def test_duplicate_event_is_idempotent(self) -> None:
        self.service.process_mis_procedure_event(
            mis_clinic_id="clinic-1",
            mis_room_id="room-101",
            service_code="INJECTION",
            mis_event_id="evt-dup",
        )
        result = self.service.process_mis_procedure_event(
            mis_clinic_id="clinic-1",
            mis_room_id="room-101",
            service_code="INJECTION",
            mis_event_id="evt-dup",
        )
        self.assertEqual(result["status"], "already_processed")
        balances = self.service.list_balances(self.product["id"])
        # Only the first delivery should have decremented stock
        self.assertEqual(balances[0]["free_quantity"], Decimal("8"))

    def test_missing_warehouse_mapping_raises_not_found(self) -> None:
        with self.assertRaises(NotFoundError):
            self.service.process_mis_procedure_event(
                mis_clinic_id="clinic-1",
                mis_room_id="room-999",
                service_code="INJECTION",
                mis_event_id="evt-2",
            )

    def test_missing_template_raises_not_found(self) -> None:
        with self.assertRaises(NotFoundError):
            self.service.process_mis_procedure_event(
                mis_clinic_id="clinic-1",
                mis_room_id="room-101",
                service_code="UNKNOWN-PROCEDURE",
                mis_event_id="evt-3",
            )

    def test_insufficient_stock_propagates_and_event_not_marked_processed(self) -> None:
        self.service.create_procedure_consumption_template(
            {
                "mis_clinic_id": "clinic-1",
                "service_code": "BIG-PROCEDURE",
                "name": "Большая процедура",
                "items": [{"product_id": self.product["id"], "quantity": "999"}],
            },
            actor_id="admin",
        )
        with self.assertRaises(InsufficientStockError):
            self.service.process_mis_procedure_event(
                mis_clinic_id="clinic-1",
                mis_room_id="room-101",
                service_code="BIG-PROCEDURE",
                mis_event_id="evt-4",
            )
        # Failed event must not be marked processed, so a retry after restocking can succeed
        result = self.service.process_mis_procedure_event(
            mis_clinic_id="clinic-1",
            mis_room_id="room-101",
            service_code="INJECTION",
            mis_event_id="evt-4",
        )
        self.assertEqual(result["status"], "processed")

    def test_delete_procedure_consumption_template(self) -> None:
        self.service.delete_procedure_consumption_template(self.template["id"], actor_id="admin")
        templates = self.service.list_procedure_consumption_templates(mis_clinic_id="clinic-1")
        self.assertEqual(templates, [])


class SupplierApplicationTest(TestCase):
    def setUp(self) -> None:
        self.database = SQLiteDatabase(":memory:")
        self.database.init_schema()
        self.service = WarehouseService(self.database)

    def submit(self, email: str = "newsupplier@example.kz", **overrides) -> dict:
        payload = {
            "name": "ТОО Новый Поставщик",
            "bin": "123456789012",
            "email": email,
            "phone": "+77001234567",
            "contact_person": "Иванов Иван",
            "city": "Алматы",
            "delivery_days": 5,
            "notes": "Готовы поставлять расходники",
        }
        payload.update(overrides)
        return self.service.submit_supplier_application(SupplierApplicationCreate(**payload), actor_id=email)

    def test_submit_creates_pending_application(self) -> None:
        application = self.submit()
        self.assertEqual(application["status"], "pending")
        self.assertEqual(application["supplier_id"], None)
        self.assertEqual(self.service.count_supplier_applications("pending"), 1)

    def test_duplicate_active_application_for_same_email_is_rejected(self) -> None:
        self.submit()
        with self.assertRaises(ValidationError):
            self.submit()

    def test_resubmission_allowed_after_rejection(self) -> None:
        application = self.submit()
        self.service.review_supplier_application(
            application["id"], SupplierApplicationReview(status="rejected", reason="БИН не подтверждён"), "admin"
        )
        # No exception: a new application for the same email is allowed once the old one is resolved.
        second = self.submit()
        self.assertEqual(second["status"], "pending")

    def test_approve_creates_supplier_and_grants_portal_access(self) -> None:
        application = self.submit()
        approved = self.service.review_supplier_application(
            application["id"],
            SupplierApplicationReview(status="approved"),
            "admin",
            password_hash="hashed-secret",
        )
        self.assertEqual(approved["status"], "approved")
        self.assertIsNotNone(approved["supplier_id"])
        suppliers = self.service.list_suppliers()
        supplier = next(s for s in suppliers if s["id"] == approved["supplier_id"])
        self.assertEqual(supplier["name"], "ТОО Новый Поставщик")
        self.assertEqual(supplier["email"], "newsupplier@example.kz")
        self.assertTrue(supplier["portal_access_enabled"])
        self.assertIsNotNone(supplier["password_hash"])

    def test_approve_matches_existing_supplier_by_bin_instead_of_duplicating(self) -> None:
        existing = self.service.create_supplier(SupplierCreate(name="ТОО Старый Поставщик", bin="123456789012"))
        application = self.submit()
        approved = self.service.review_supplier_application(
            application["id"], SupplierApplicationReview(status="approved"), "admin"
        )
        self.assertEqual(approved["supplier_id"], existing["id"])
        suppliers = self.service.list_suppliers()
        matching = [s for s in suppliers if s["bin"] == "123456789012"]
        self.assertEqual(len(matching), 1)

    def test_reject_does_not_create_supplier(self) -> None:
        application = self.submit()
        rejected = self.service.review_supplier_application(
            application["id"], SupplierApplicationReview(status="rejected", reason="Недостаточно данных"), "admin"
        )
        self.assertEqual(rejected["status"], "rejected")
        self.assertIsNone(rejected["supplier_id"])
        self.assertEqual(self.service.list_suppliers(), [])

    def test_needs_changes_does_not_create_supplier_and_can_be_resubmitted_later(self) -> None:
        application = self.submit()
        updated = self.service.review_supplier_application(
            application["id"],
            SupplierApplicationReview(status="needs_changes", reason="Уточните БИН"),
            "admin",
        )
        self.assertEqual(updated["status"], "needs_changes")
        self.assertIsNone(updated["supplier_id"])

    def test_list_supplier_applications_filters_by_status(self) -> None:
        app1 = self.submit(email="one@example.kz")
        self.submit(email="two@example.kz")
        self.service.review_supplier_application(
            app1["id"], SupplierApplicationReview(status="approved"), "admin"
        )
        pending = self.service.list_supplier_applications(status="pending")
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["email"], "two@example.kz")
        approved = self.service.list_supplier_applications(status="approved")
        self.assertEqual(len(approved), 1)
        self.assertEqual(approved[0]["email"], "one@example.kz")
