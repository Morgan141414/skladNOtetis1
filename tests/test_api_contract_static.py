import ast
from pathlib import Path
from unittest import TestCase

from app.domain.schemas import SafeStockDocumentDetail, SafeStockDocumentLine, SafeStockMovement


ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = ROOT / "app" / "api" / "routes.py"
DEPENDENCIES_PATH = ROOT / "app" / "api" / "dependencies.py"
CONFIG_PATH = ROOT / "app" / "core" / "config.py"


class APIContractStaticTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tree = ast.parse(ROUTES_PATH.read_text())

    def test_primary_routes_have_response_model(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        for function_name in (
            "create_category",
            "update_category",
            "delete_category",
            "create_supplier",
            "list_supplier_price_history",
            "update_supplier",
            "create_warehouse",
            "resolve_tetis_warehouse_ids",
            "update_warehouse",
            "set_inventory_lock",
            "list_product_units",
            "create_product",
            "update_product",
            "delete_product",
            "get_product_barcode_label",
            "get_product_barcode_labels",
            "get_batch",
            "get_batch_price_label",
            "get_batch_price_labels",
            "get_batch_movements",
            "get_batch_traceability",
            "recall_batch",
            "list_batch_recalls",
            "receive",
            "create_receipt_document",
            "create_writeoff_document",
            "create_transfer_document",
            "create_department_return_document",
            "create_supplier_return_document",
            "create_repack_document",
            "get_stock_document",
            "get_repack_print_form",
            "get_transfer_print_form",
            "list_batch_transformations",
            "post_stock_document",
            "approve_stock_document",
            "cancel_stock_document",
            "update_batch_status",
            "write_off",
            "write_off_fefo",
            "transfer",
            "return_from_department",
            "return_to_supplier",
            "reserve",
            "release_reservation",
            "expire_reservations",
            "create_inventory_session",
            "get_inventory_session",
            "get_inventory_print_form",
            "update_inventory_line_count",
            "post_inventory_session",
            "cancel_inventory_session",
            "list_balances",
            "abc_xyz_analysis",
            "generate_low_stock_notifications",
            "generate_expiry_notifications",
            "list_notifications",
            "list_audit_log",
            "export_controlled_substance_ledger",
            "mark_notification_read",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                self.assertTrue(
                    self._has_decorator_keyword(functions[function_name], "response_model"),
                    f"{function_name} must define response_model",
                )

    def test_map_error_uses_machine_readable_error_codes(self) -> None:
        source = ROUTES_PATH.read_text()

        for code in ("not_found", "conflict", "forbidden", "validation_error", "internal_error"):
            with self.subTest(code=code):
                self.assertIn(f'"code": "{code}"', source)

    def test_readiness_endpoint_reports_database_runtime(self) -> None:
        routes_source = ROUTES_PATH.read_text()
        dependencies_source = DEPENDENCIES_PATH.read_text()
        config_source = CONFIG_PATH.read_text()

        self.assertIn('@router.get("/health/ready")', routes_source)
        self.assertIn("get_database_readiness", routes_source)
        self.assertIn("HTTP_503_SERVICE_UNAVAILABLE", routes_source)
        self.assertIn('deployment_mode: Literal["demo", "staging", "production"] = "demo"', config_source)
        self.assertIn('database_backend: Literal["sqlite", "postgresql"] = "sqlite"', config_source)
        self.assertIn("database_url_matches_backend", config_source)
        self.assertIn("database_backend_allowed_for_mode", config_source)
        self.assertIn("runtime_configuration_error", config_source)
        self.assertIn("PostgresDatabase(settings.database_url)", dependencies_source)
        self.assertIn("PostgreSQL runtime adapter is enabled", dependencies_source)
        self.assertIn("PostgresIdempotencyRepository", dependencies_source)

    def test_catalog_item_reviews_accept_photo_and_display_name(self) -> None:
        routes_source = ROUTES_PATH.read_text()
        service_source = (ROOT / "app" / "services" / "warehouse.py").read_text()
        sqlite_source = (ROOT / "app" / "storage" / "sqlite.py").read_text()

        for snippet in (
            "image_url: str | None",
            "reviewer_name: str | None",
            "image_url=body.image_url",
            "reviewer_name=body.reviewer_name",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, routes_source)
        for snippet in (
            "INSERT INTO catalog_item_reviews",
            "image_url, reviewer_name, status",
            "Review image URL must be an absolute URL or uploaded media path",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, service_source)
        for snippet in (
            "CREATE TABLE IF NOT EXISTS catalog_item_reviews",
            "image_url TEXT",
            "reviewer_name TEXT",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, sqlite_source)

    def test_background_jobs_are_explicitly_configured_and_lifespan_managed(self) -> None:
        main_source = (ROOT / "app" / "main.py").read_text()
        config_source = CONFIG_PATH.read_text()
        jobs_source = (ROOT / "app" / "services" / "background_jobs.py").read_text()

        for snippet in (
            "background_jobs_enabled: bool = False",
            "background_jobs_interval_seconds: int = 3600",
            "background_jobs_expiry_days: int = 30",
            "background_jobs_actor_id: str = \"system-scheduler\"",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, config_source)

        for snippet in (
            "async def lifespan",
            "settings.background_jobs_enabled",
            "WarehouseBackgroundJobs",
            "PeriodicJobRunner",
            "runner.start()",
            "await runner.stop()",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, main_source)

        for snippet in (
            "asyncio.to_thread",
            "expire_reservations(actor_id=self.actor_id)",
            "generate_low_stock_notifications()",
            "generate_expiry_notifications(days=self.expiry_days)",
            "self._run_lock.locked()",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, jobs_source)

    def test_dev_header_auth_is_behind_explicit_setting(self) -> None:
        dependencies_source = DEPENDENCIES_PATH.read_text()
        config_source = CONFIG_PATH.read_text()
        routes_source = ROUTES_PATH.read_text()

        self.assertIn("public_access_enabled: bool = True", config_source)
        self.assertIn("dev_auth_enabled: bool = False", config_source)
        self.assertIn("if settings.public_access_enabled", dependencies_source)
        self.assertIn("except (AuthenticationError, ValidationError):", dependencies_source)
        self.assertIn("if not settings.dev_auth_enabled", dependencies_source)
        self.assertIn("HTTP_401_UNAUTHORIZED", dependencies_source)
        self.assertIn('"code": "unauthorized"', dependencies_source)
        self.assertIn("allow_dev_default=settings.dev_auth_enabled", dependencies_source)
        self.assertIn("if not settings.dev_auth_enabled", routes_source)

    def test_critical_mutating_routes_have_idempotency_guard(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        for function_name in (
            "receive",
            "create_receipt_document",
            "create_writeoff_document",
            "create_transfer_document",
            "create_department_return_document",
            "create_supplier_return_document",
            "create_repack_document",
            "update_batch_status",
            "recall_batch",
            "post_stock_document",
            "approve_stock_document",
            "cancel_stock_document",
            "write_off",
            "write_off_fefo",
            "transfer",
            "return_from_department",
            "return_to_supplier",
            "reserve",
            "release_reservation",
            "expire_reservations",
            "create_inventory_session",
            "post_inventory_session",
            "cancel_inventory_session",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                function = functions[function_name]
                arg_names = {arg.arg for arg in function.args.args}
                self.assertIn("idempotency_key", arg_names)
                self.assertIn("idempotency_store", arg_names)
                self.assertTrue(self._calls_function(function, "run_idempotent"))

    def test_primary_routes_have_actor_context_dependency(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        for function_name in (
            "create_category",
            "update_category",
            "delete_category",
            "create_supplier",
            "update_supplier",
            "create_warehouse",
            "update_warehouse",
            "set_inventory_lock",
            "create_product",
            "update_product",
            "delete_product",
            "get_batch",
            "get_batch_movements",
            "get_batch_traceability",
            "receive",
            "create_receipt_document",
            "create_writeoff_document",
            "create_transfer_document",
            "create_department_return_document",
            "create_supplier_return_document",
            "create_repack_document",
            "get_stock_document",
            "list_batch_transformations",
            "get_batch",
            "get_batch_movements",
            "get_batch_traceability",
            "recall_batch",
            "list_batch_recalls",
            "post_stock_document",
            "approve_stock_document",
            "cancel_stock_document",
            "update_batch_status",
            "write_off",
            "write_off_fefo",
            "transfer",
            "return_from_department",
            "return_to_supplier",
            "reserve",
            "release_reservation",
            "expire_reservations",
            "create_inventory_session",
            "get_inventory_session",
            "update_inventory_line_count",
            "post_inventory_session",
            "cancel_inventory_session",
            "list_balances",
            "abc_xyz_analysis",
            "generate_low_stock_notifications",
            "generate_expiry_notifications",
            "list_notifications",
            "list_audit_log",
            "mark_notification_read",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                arg_names = {arg.arg for arg in functions[function_name].args.args}
                self.assertIn("actor_ctx", arg_names)

    def test_object_id_routes_enforce_warehouse_scope(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        for function_name in (
            "get_stock_document",
            "post_stock_document",
            "cancel_stock_document",
            "release_reservation",
            "get_inventory_session",
            "update_inventory_line_count",
            "post_inventory_session",
            "cancel_inventory_session",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                self.assertTrue(
                    self._calls_function(functions[function_name], "require_stock_access"),
                    f"{function_name} must enforce warehouse scope from the loaded object",
                )

        for function_name in (
            "get_batch",
            "get_batch_movements",
            "get_batch_traceability",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                self.assertTrue(
                    self._calls_function(functions[function_name], "require_batch_read_scope"),
                    f"{function_name} must enforce batch warehouse scope",
                )

    def test_batch_status_update_enforces_all_batch_warehouses(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        function = functions["update_batch_status"]
        route_source = ROUTES_PATH.read_text()

        self.assertTrue(self._calls_function(function, "run_idempotent"))
        self.assertTrue(self._calls_function(function, "require_stock_access"))
        self.assertIn("get_batch_warehouse_ids(batch_id)", route_source)
        self.assertIn("for warehouse_id in warehouse_ids", route_source)
        service_source = (ROUTES_PATH.parents[1] / "services" / "warehouse.py").read_text()
        self.assertIn("Batch has no stock balances", service_source)
        self.assertIn("for warehouse_id in warehouse_ids", service_source)

    def test_expire_reservations_is_scoped_by_warehouse_filter(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        function = functions["expire_reservations"]
        arg_names = {arg.arg for arg in function.args.args}

        self.assertIn("warehouse_id", arg_names)
        self.assertTrue(self._calls_function(function, "require_warehouse_filter"))
        route_source = ROUTES_PATH.read_text()
        self.assertIn('payload={"warehouse_id": warehouse_id}', route_source)
        self.assertIn("actor_id=actor_id, warehouse_id=warehouse_id", route_source)

    def test_notifications_are_scoped_by_warehouse_filter(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        route_source = ROUTES_PATH.read_text()

        for function_name in (
            "generate_low_stock_notifications",
            "generate_expiry_notifications",
            "list_notifications",
            "mark_notification_read",
        ):
            with self.subTest(function=function_name):
                function = functions[function_name]
                if function_name != "mark_notification_read":
                    arg_names = {arg.arg for arg in function.args.args}
                    self.assertIn("warehouse_id", arg_names)
                self.assertTrue(self._calls_function(function, "require_warehouse_filter"))

        self.assertIn("generate_low_stock_notifications(warehouse_id=warehouse_id)", route_source)
        self.assertIn(
            "generate_expiry_notifications(days=days, warehouse_id=warehouse_id)",
            route_source,
        )
        self.assertIn("warehouse_id=warehouse_id", route_source)
        self.assertIn("get_notification(notification_id)", route_source)

    def test_analytics_are_scoped_by_warehouse_filter(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        function = functions["abc_xyz_analysis"]
        arg_names = {arg.arg for arg in function.args.args}
        route_source = ROUTES_PATH.read_text()

        self.assertIn("warehouse_id", arg_names)
        self.assertIn("days", arg_names)
        self.assertTrue(self._calls_function(function, "require_warehouse_filter"))
        self.assertIn("abc_xyz_analysis(analysis_days=days, warehouse_id=warehouse_id)", route_source)

    def test_analytics_history_routes_are_scoped(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        route_source = ROUTES_PATH.read_text()

        for function_name in ("create_abc_xyz_run", "list_abc_xyz_runs", "get_abc_xyz_run"):
            with self.subTest(function=function_name):
                function = functions[function_name]
                self.assertTrue(self._calls_function(function, "require_warehouse_filter"))

        self.assertIn("/analytics/abc-xyz/runs", route_source)
        self.assertIn("/analytics/abc-xyz/history", route_source)
        self.assertIn("save_abc_xyz_analysis_snapshot", route_source)

    def test_quarantine_review_routes_are_scoped(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        route_source = ROUTES_PATH.read_text()

        for function_name in (
            "list_quarantine_reviews",
            "get_quarantine_review",
            "get_quarantine_review_protocol",
            "update_quarantine_review",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                self.assertTrue(
                    self._calls_function(functions[function_name], "require_warehouse_filter")
                    or self._calls_function(functions[function_name], "require_stock_access")
                )

        self.assertIn("/quarantine-reviews", route_source)
        self.assertIn("/quarantine-reviews/{review_id}/protocol", route_source)
        self.assertIn("QuarantineReviewPage", route_source)
        self.assertIn("QuarantineReviewProtocol", route_source)
        self.assertIn("QuarantineReviewUpdate", route_source)

    def test_sensor_routes_are_scoped_and_exposed(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        route_source = ROUTES_PATH.read_text()

        for function_name in (
            "create_sensor_device",
            "list_sensor_devices",
            "update_sensor_device",
            "record_sensor_reading",
            "list_sensor_readings",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                self.assertTrue(
                    self._calls_function(functions[function_name], "require_warehouse_filter")
                    or self._calls_function(functions[function_name], "require_stock_access")
                )

        self.assertIn("/sensor-devices", route_source)
        self.assertIn("/sensor-readings", route_source)
        self.assertIn("SensorReadingPage", route_source)

    def test_audit_log_is_scoped_by_warehouse_filter(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        function = functions["list_audit_log"]
        arg_names = {arg.arg for arg in function.args.args}
        route_source = ROUTES_PATH.read_text()

        self.assertIn("warehouse_id", arg_names)
        self.assertTrue(self._calls_function(function, "require_warehouse_filter"))
        self.assertIn("warehouse_id=warehouse_id", route_source)

    def test_realtime_publish_is_wrapped_as_best_effort(self) -> None:
        source = ROUTES_PATH.read_text()

        self.assertIn("async def publish_event", source)
        self.assertIn("logger.exception", source)
        self.assertEqual(source.count("manager.broadcast("), 1)

    def test_balances_websocket_checks_actor_and_warehouse_scope(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        function = functions["balances_ws"]

        self.assertTrue(self._calls_function(function, "actor_from_headers"))
        self.assertTrue(self._calls_function(function, "actor_from_bearer_token"))
        self.assertTrue(self._calls_function(function, "require_permission"))
        self.assertTrue(self._calls_function(function, "require_warehouse_filter"))
        route_source = ROUTES_PATH.read_text()
        self.assertIn("access_token", route_source)
        self.assertIn("authorization", route_source)
        self.assertIn("warehouse_scope", route_source)

    def test_list_routes_have_limit_and_offset(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        for function_name in (
            "list_balances",
            "get_batch",
            "get_batch_movements",
            "get_batch_traceability",
            "list_stock_movements",
            "list_notifications",
            "list_audit_log",
        ):
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                arg_names = {arg.arg for arg in functions[function_name].args.args}
                self.assertIn("limit", arg_names)
                self.assertIn("offset", arg_names)

    def test_stock_movements_are_scoped_and_redacted(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        function = functions["list_stock_movements"]
        arg_names = {arg.arg for arg in function.args.args}
        service_source = (ROUTES_PATH.parents[1] / "services" / "warehouse.py").read_text()

        self.assertIn("warehouse_id", arg_names)
        self.assertTrue(self._calls_function(function, "require_warehouse_filter"))
        self.assertIn("_redact_movement_payload", service_source)
        self.assertIn("medical_record_no", service_source)
        self.assertIn("second_approver_id", service_source)

    def test_read_routes_use_safe_stock_response_models(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        expected_models = {
            "get_batch": "BatchDetail",
            "get_batch_movements": "list[SafeStockMovement]",
            "get_batch_traceability": "BatchTraceability",
            "get_stock_document": "SafeStockDocumentDetail",
            "list_stock_documents": "StockDocumentPage",
            "list_batch_transformations": "BatchTransformationPage",
            "list_batch_recalls": "BatchRecallPage",
            "list_stock_movements": "StockMovementPage",
        }

        for function_name, model_name in expected_models.items():
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                self.assertEqual(
                    self._decorator_keyword_source(functions[function_name], "response_model"),
                    model_name,
                )

    def test_safe_stock_read_models_do_not_expose_sensitive_fields(self) -> None:
        sensitive_fields = {"patient_id", "doctor_id", "medical_record_no"}

        for model in (SafeStockDocumentDetail, SafeStockDocumentLine, SafeStockMovement):
            with self.subTest(model=model.__name__):
                self.assertFalse(sensitive_fields & self._model_fields(model))

    def test_list_routes_use_pagination_envelope_models(self) -> None:
        functions = {
            node.name: node
            for node in ast.walk(self.tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        expected_models = {
            "list_balances": "BalancePage",
            "list_stock_documents": "StockDocumentPage",
            "list_stock_movements": "StockMovementPage",
            "list_notifications": "NotificationPage",
            "list_audit_log": "AuditLogPage",
            "list_supplier_price_history": "SupplierPriceHistoryPage",
        }

        for function_name, model_name in expected_models.items():
            with self.subTest(function=function_name):
                self.assertIn(function_name, functions)
                self.assertEqual(
                    self._decorator_keyword_name(functions[function_name], "response_model"),
                    model_name,
                )

    def test_postgresql_schema_contains_production_constraints(self) -> None:
        sql_path = ROUTES_PATH.parents[1] / "db" / "sql" / "0001_initial_postgresql.sql"
        sql = sql_path.read_text()

        for snippet in (
            "uq_inventory_sessions_one_active",
            "stock_documents_supplier_matches_type",
            "approved_by TEXT",
            "approved_at TIMESTAMPTZ",
            "'approved'",
            "second_approver_id TEXT",
            "second_approval_note TEXT",
            "stock_movements_type_check",
            "idx_stock_document_lines_document_id",
            "CREATE TABLE IF NOT EXISTS batch_transformations",
            "idx_batch_transformations_source_batch",
            "idx_batch_transformations_target_batch",
            "idx_batch_transformations_document",
            "idx_batch_transformations_warehouse_created",
            "'repack'",
            "'repack_out'",
            "'repack_in'",
            "idx_inventory_lines_session_id",
            "CREATE TABLE IF NOT EXISTS inventory_responsibles",
            "CREATE TABLE IF NOT EXISTS inventory_session_categories",
            "CREATE TABLE IF NOT EXISTS supplier_price_history",
            "idx_supplier_price_history_supplier_product_recorded",
            "idx_audit_log_created",
            "idx_audit_log_warehouse_created",
            "idx_notifications_warehouse_read",
            "uq_notifications_unread_low_stock_warehouse_product",
            "uq_notifications_unread_expiry_warehouse_batch",
            "uq_notifications_unread_sensor_warning_device",
            "CREATE TABLE IF NOT EXISTS purchase_requests",
            "idx_purchase_requests_warehouse_status_created",
            "uq_purchase_requests_open_draft_product_warehouse",
            "purchase_requests_status_check",
            "CREATE TABLE IF NOT EXISTS abc_xyz_runs",
            "CREATE TABLE IF NOT EXISTS abc_xyz_run_items",
            "idx_abc_xyz_runs_warehouse_generated",
            "uq_abc_xyz_runs_period",
            "CREATE TABLE IF NOT EXISTS quarantine_reviews",
            "idx_quarantine_reviews_warehouse_status_due",
            "quarantine_reviews_status_check",
            "CREATE TABLE IF NOT EXISTS batch_recalls",
            "idx_batch_recalls_batch_created",
            "idx_batch_recalls_created",
            "CREATE TABLE IF NOT EXISTS sensor_devices",
            "CREATE TABLE IF NOT EXISTS sensor_readings",
            "idx_sensor_devices_warehouse",
            "idx_sensor_readings_warehouse_recorded",
            "sensor_readings_status_check",
            "device_id BIGINT REFERENCES sensor_devices(id)",
            "sensor_reading_id BIGINT REFERENCES sensor_readings(id)",
            "CREATE TABLE IF NOT EXISTS outbox_events",
            "CREATE TABLE IF NOT EXISTS idempotency_keys",
            "UNIQUE(actor_id, key)",
            "idempotency_keys_status_check",
            "tetis_org_id TEXT",
            "external_tetis_id TEXT",
            "idx_warehouses_tetis_org_id",
            "uq_warehouses_tetis_org_external",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, sql)

    def test_abc_xyz_history_has_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0003_abc_xyz_history.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0002_warehouse_tetis_mapping"',
            "CREATE TABLE IF NOT EXISTS abc_xyz_runs",
            "CREATE TABLE IF NOT EXISTS abc_xyz_run_items",
            "uq_abc_xyz_runs_period",
            "idx_abc_xyz_run_items_run",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_quarantine_reviews_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0004_quarantine_reviews.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0003_abc_xyz_history"',
            "CREATE TABLE IF NOT EXISTS quarantine_reviews",
            "quarantine_reviews_status_check",
            "idx_quarantine_reviews_warehouse_status_due",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_sensor_conditions_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0005_sensor_conditions.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0004_quarantine_reviews"',
            "CREATE TABLE IF NOT EXISTS sensor_devices",
            "CREATE TABLE IF NOT EXISTS sensor_readings",
            "idx_sensor_readings_warehouse_recorded",
            "sensor_readings_status_check",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_sensor_warning_notifications_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0010_sensor_warning_notifications.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0009_controlled_writeoff_second_confirmation"',
            "device_id BIGINT REFERENCES sensor_devices(id)",
            "sensor_reading_id BIGINT REFERENCES sensor_readings(id)",
            "uq_notifications_unread_sensor_warning_device",
            "notification_type = 'sensor_warning'",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_inventory_metadata_and_price_history_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0011_inventory_metadata_price_history.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0010_sensor_warning_notifications"',
            "CREATE TABLE IF NOT EXISTS inventory_responsibles",
            "CREATE TABLE IF NOT EXISTS inventory_session_categories",
            "CREATE TABLE IF NOT EXISTS supplier_price_history",
            "idx_supplier_price_history_supplier_product_recorded",
            "batch_backfill",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_supplier_profile_fields_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0012_supplier_profile_fields.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0011_inventory_metadata_price_history"',
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS address TEXT",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS rating INTEGER",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS is_preferred BOOLEAN NOT NULL DEFAULT FALSE",
            "suppliers_rating_range",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_catalog_soft_delete_has_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0013_catalog_soft_delete.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0012_supplier_profile_fields"',
            "ALTER TABLE categories ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE",
            "ALTER TABLE products ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE",
            "idx_categories_active_name",
            "idx_products_active_name",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_supplier_card_fields_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0014_supplier_card_fields.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0013_catalog_soft_delete"',
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS contact_person TEXT",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS email TEXT",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS contract_number TEXT",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS contract_expires_on DATE",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS payment_terms TEXT",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS notes TEXT",
            "idx_suppliers_contract_expires",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_warehouse_zone_limits_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0015_warehouse_zone_limits.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0014_supplier_card_fields"',
            "ALTER TABLE warehouses ADD COLUMN IF NOT EXISTS storage_zone TEXT",
            "ALTER TABLE warehouses ADD COLUMN IF NOT EXISTS capacity_limit NUMERIC",
            "ALTER TABLE warehouses ADD COLUMN IF NOT EXISTS storage_conditions TEXT",
            "ALTER TABLE warehouses ADD COLUMN IF NOT EXISTS responsible_person TEXT",
            "idx_warehouses_storage_zone",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_batch_serial_numbers_have_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0016_batch_serial_numbers.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0015_warehouse_zone_limits"',
            "ALTER TABLE batches ADD COLUMN IF NOT EXISTS serial_number TEXT",
            "ALTER TABLE stock_document_lines ADD COLUMN IF NOT EXISTS serial_number TEXT",
            "idx_batches_serial_number",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_tetis_warehouse_mapping_has_forward_migration(self) -> None:
        migration_path = (
            ROUTES_PATH.parents[1]
            / "db"
            / "migrations"
            / "versions"
            / "0002_warehouse_tetis_mapping.py"
        )
        migration = migration_path.read_text()

        for snippet in (
            'down_revision = "0001_initial_postgresql"',
            "ALTER TABLE warehouses ADD COLUMN IF NOT EXISTS tetis_org_id TEXT",
            "ALTER TABLE warehouses ADD COLUMN IF NOT EXISTS external_tetis_id TEXT",
            "idx_warehouses_tetis_org_id",
            "uq_warehouses_tetis_org_external",
            "WHERE tetis_org_id IS NOT NULL AND external_tetis_id IS NOT NULL",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)

    def test_tetis_warehouse_mapping_has_admin_lookup_endpoint(self) -> None:
        routes_source = ROUTES_PATH.read_text()
        schemas_source = (ROOT / "app" / "domain" / "schemas.py").read_text()

        for snippet in (
            'class TetisWarehouseMapping(Row):',
            "warehouse_ids: list[int]",
            '@router.get("/tetis/orgs/{tetis_org_id}/warehouse-ids", response_model=TetisWarehouseMapping)',
            "def resolve_tetis_warehouse_ids(",
            "require_permission(actor_ctx, Permission.ADMIN_USERS)",
            '"warehouse_ids": service.list_warehouse_ids_for_tetis_org(tetis_org_id)',
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, routes_source + schemas_source)

    def test_marketplace_inquiries_track_source_channel(self) -> None:
        routes_source = ROUTES_PATH.read_text()
        service_source = (ROOT / "app" / "services" / "warehouse.py").read_text()
        migration_source = (
            ROOT
            / "app"
            / "db"
            / "migrations"
            / "versions"
            / "0045_marketplace_inquiry_source.py"
        ).read_text()

        for snippet in (
            'source: str = Field(default="marqet", pattern="^(marqet|qpartner|api)$")',
            'source: str = Field(default="qpartner", pattern="^(marqet|qpartner|api)$")',
            "body.source",
            "source=body.source",
            "source=source",
            "def _validate_marketplace_inquiry_source",
            "def _validate_marketplace_inquiry_status",
            "mi.source = ?",
            "ADD COLUMN IF NOT EXISTS source TEXT NOT NULL DEFAULT 'marqet'",
            "idx_marketplace_inquiries_source",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, routes_source + service_source + migration_source)

    def test_purchase_order_persists_delivery_and_escrow_terms(self) -> None:
        routes_source = ROUTES_PATH.read_text()
        service_source = (ROOT / "app" / "services" / "warehouse.py").read_text()

        for snippet in (
            'delivery_type: str | None = Field(default=None, pattern="^(pickup|courier|freight|postal|buyer_arranges)$")',
            "delivery_price: float | None = Field(default=None, ge=0)",
            "escrow_amount: float | None = Field(default=None, ge=0)",
            "delivery_type, delivery_price, delivery_included, escrow_amount",
            'buyer_data.get("delivery_type")',
            'buyer_data.get("delivery_price")',
            'buyer_data.get("delivery_included", False)',
            'buyer_data.get("escrow_amount")',
            "SELECT id, escrow_status FROM purchase_orders WHERE inquiry_id = ?",
            "Тип доставки",
            "Стоимость доставки",
            "Доставка включена",
            "Эскроу",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, routes_source + service_source)

    def test_supplier_login_builds_token_after_authentication(self) -> None:
        routes_source = ROUTES_PATH.read_text()
        login_start = routes_source.index("def supplier_login")
        login_end = routes_source.index("@router.post(\n    \"/suppliers/{supplier_id}/portal-access\"", login_start)
        login_source = routes_source[login_start:login_end]

        self.assertIn("supplier = svc.get_supplier_by_email(body.email)", login_source)
        self.assertIn("verify_password(body.password, supplier[\"password_hash\"])", login_source)
        self.assertIn("\"sub\": f\"supplier:{supplier['id']}\"", login_source)
        self.assertIn("\"roles\": [\"supplier\"]", login_source)
        self.assertIn("\"supplier_id\": supplier[\"id\"]", login_source)
        self.assertNotIn("tetis_user_id", login_source)
        self.assertNotIn("user is not None", login_source)

    def _has_decorator_keyword(self, node: ast.AST, keyword_name: str) -> bool:
        decorators = getattr(node, "decorator_list", [])
        for decorator in decorators:
            if not isinstance(decorator, ast.Call):
                continue
            for keyword in decorator.keywords:
                if keyword.arg == keyword_name:
                    return True
        return False

    def _calls_function(self, node: ast.AST, function_name: str) -> bool:
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if child.func.id == function_name:
                    return True
        return False

    def _decorator_keyword_name(self, node: ast.AST, keyword_name: str) -> str | None:
        decorators = getattr(node, "decorator_list", [])
        for decorator in decorators:
            if not isinstance(decorator, ast.Call):
                continue
            for keyword in decorator.keywords:
                if keyword.arg != keyword_name:
                    continue
                if isinstance(keyword.value, ast.Name):
                    return keyword.value.id
        return None

    def _decorator_keyword_source(self, node: ast.AST, keyword_name: str) -> str | None:
        decorators = getattr(node, "decorator_list", [])
        for decorator in decorators:
            if not isinstance(decorator, ast.Call):
                continue
            for keyword in decorator.keywords:
                if keyword.arg == keyword_name:
                    return ast.unparse(keyword.value)
        return None

    def _model_fields(self, model: type) -> set[str]:
        if hasattr(model, "model_fields"):
            return set(model.model_fields)
        fields: set[str] = set()
        for parent in reversed(model.__mro__):
            fields.update(getattr(parent, "__annotations__", {}))
        return fields
