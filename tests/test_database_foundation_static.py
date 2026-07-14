from pathlib import Path
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[1]


class DatabaseFoundationStaticTest(TestCase):
    def test_alembic_baseline_points_to_reviewed_postgresql_sql(self) -> None:
        migration_path = ROOT / "app" / "db" / "migrations" / "versions" / "0001_initial_postgresql.py"
        migration = migration_path.read_text()

        self.assertIn('revision = "0001_initial_postgresql"', migration)
        self.assertIn("0001_initial_postgresql.sql", migration)
        self.assertIn("op.execute(sql_path.read_text())", migration)

    def test_alembic_environment_uses_sklad_database_url(self) -> None:
        env = (ROOT / "app" / "db" / "migrations" / "env.py").read_text()

        self.assertIn("get_settings", env)
        self.assertIn('config.set_main_option("sqlalchemy.url", settings.database_url)', env)

    def test_alembic_heads_are_merged_for_marketplace_branch(self) -> None:
        merge = (
            ROOT
            / "app"
            / "db"
            / "migrations"
            / "versions"
            / "0046_merge_supplier_offers_marketplace_inquiry_source.py"
        ).read_text()

        self.assertIn(
            'revision = "0046_merge_supplier_offers_marketplace_inquiry_source"',
            merge,
        )
        self.assertIn('"0018_supplier_offers"', merge)
        self.assertIn('"0045_marketplace_inquiry_source"', merge)
        self.assertIn('"0047_listing_expiry_promotion"', merge)
        self.assertIn("def upgrade() -> None:", merge)
        self.assertIn("def downgrade() -> None:", merge)

    def test_marketplace_refund_requests_have_auditable_storage(self) -> None:
        migration = (
            ROOT
            / "app"
            / "db"
            / "migrations"
            / "versions"
            / "0050_marketplace_refund_requests.py"
        ).read_text()
        sqlite_schema = (ROOT / "app" / "storage" / "sqlite.py").read_text()
        service = (ROOT / "app" / "services" / "warehouse.py").read_text()

        for snippet in (
            "CREATE TABLE IF NOT EXISTS marketplace_refund_requests",
            "actor_id TEXT NOT NULL",
            "supplier_id BIGINT NOT NULL REFERENCES suppliers(id)",
            "uq_marketplace_refund_requests_active_order",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, migration)
        self.assertIn("CREATE TABLE IF NOT EXISTS marketplace_refund_requests", sqlite_schema)
        self.assertIn("INSERT INTO marketplace_refund_requests", service)
        self.assertIn("status = 'refunded'", service)

    def test_unit_of_work_has_commit_rollback_boundary(self) -> None:
        uow = (ROOT / "app" / "db" / "uow.py").read_text()

        self.assertIn("class UnitOfWork", uow)
        self.assertIn("self.session.commit()", uow)
        self.assertIn("self.session.rollback()", uow)

    def test_sqlalchemy_models_cover_runtime_foundation_tables(self) -> None:
        models = (ROOT / "app" / "db" / "models.py").read_text()

        for table_name in (
            "stock_balances",
            "stock_documents",
            "audit_log",
            "idempotency_keys",
            "outbox_events",
        ):
            with self.subTest(table=table_name):
                self.assertIn(f'__tablename__ = "{table_name}"', models)

        self.assertIn("warehouse_id: Mapped[int | None]", models)

    def test_project_metadata_contains_production_database_dependencies(self) -> None:
        pyproject = (ROOT / "pyproject.toml").read_text()

        for dependency in ("SQLAlchemy", "alembic", "psycopg", "redis"):
            with self.subTest(dependency=dependency):
                self.assertIn(dependency, pyproject)

    def test_idempotency_repository_has_sqlite_and_postgresql_adapters(self) -> None:
        repository = (ROOT / "app" / "repositories" / "idempotency.py").read_text()

        self.assertIn("class IdempotencyRepository", repository)
        self.assertIn("class SQLiteIdempotencyRepository", repository)
        self.assertIn("class PostgresIdempotencyRepository", repository)
        self.assertIn("DuplicateIdempotencyKeyError", repository)

    def test_postgresql_runtime_adapter_and_migration_tools_exist(self) -> None:
        adapter = (ROOT / "app" / "storage" / "postgresql.py").read_text()
        dependencies = (ROOT / "app" / "api" / "dependencies.py").read_text()
        preflight = (ROOT / "scripts" / "sklad_sqlite_preflight.py").read_text()
        migrator = (ROOT / "scripts" / "sklad_sqlite_to_postgres.py").read_text()
        reconcile = (ROOT / "scripts" / "sklad_postgres_reconcile.py").read_text()
        runtime_smoke = (ROOT / "scripts" / "sklad_postgres_runtime_smoke.py").read_text()

        self.assertIn("class PostgresDatabase", adapter)
        self.assertIn("translate_sqlite_query", adapter)
        self.assertIn("insert_and_get_id", adapter)
        self.assertIn("PostgresDatabase(settings.database_url)", dependencies)
        self.assertIn("PostgresIdempotencyRepository", dependencies)
        self.assertIn("PRAGMA integrity_check", preflight)
        self.assertIn("foreign_key_check", preflight)
        self.assertIn("setval", migrator)
        self.assertIn("Jsonb", migrator)
        self.assertIn("Compare a SKLAD SQLite snapshot", reconcile)
        self.assertIn("stock_balance_totals", reconcile)
        self.assertIn("movement_totals", reconcile)
        self.assertIn("Status count mismatch", reconcile)
        self.assertIn("Run a mutating PostgreSQL runtime smoke test", runtime_smoke)
        self.assertIn('/health/ready', runtime_smoke)
        self.assertIn('/stock-documents/transfers', runtime_smoke)
        self.assertIn('/purchase-requests/generate', runtime_smoke)
        self.assertIn("Expected at least one low-stock notification", runtime_smoke)

    def test_default_compose_uses_postgresql_runtime(self) -> None:
        compose = (ROOT / "docker-compose.yml").read_text()
        demo_compose = (ROOT / "docker-compose.demo.yml").read_text()
        dockerfile = (ROOT / "Dockerfile").read_text()

        self.assertIn("SKLAD_DEPLOYMENT_MODE: staging", compose)
        self.assertIn("SKLAD_DATABASE_BACKEND: postgresql", compose)
        self.assertIn("SKLAD_DATABASE_URL: ${SKLAD_DATABASE_URL:?", compose)
        self.assertIn('SKLAD_PUBLIC_ACCESS_ENABLED: "false"', compose)
        self.assertIn("SKLAD_JWT_HMAC_SECRET: ${SKLAD_JWT_HMAC_SECRET:?", compose)
        self.assertIn("POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?", compose)
        self.assertNotIn("sklad" + "_dev_password", compose)
        self.assertNotIn("change-this" + "-staging-secret", compose)
        self.assertIn("alembic upgrade head", compose)
        self.assertNotIn("sqlite:////data/sklad.db", compose)
        self.assertIn("SKLAD_DEPLOYMENT_MODE: demo", demo_compose)
        self.assertIn("SKLAD_DATABASE_BACKEND: sqlite", demo_compose)
        self.assertIn("COPY alembic.ini ./alembic.ini", dockerfile)
        self.assertIn("COPY frontend ./frontend", dockerfile)

    def test_postgresql_runtime_uses_conflict_safe_generation_paths(self) -> None:
        service = (ROOT / "app" / "services" / "warehouse.py").read_text()

        self.assertIn("_upsert_purchase_request_postgresql", service)
        self.assertIn("_insert_purchase_request_if_absent_postgresql", service)
        self.assertIn("_insert_low_stock_notification_if_absent_postgresql", service)
        self.assertIn("_insert_expiry_notification_if_absent_postgresql", service)
        self.assertIn("_upsert_sensor_warning_notification_postgresql", service)
        self.assertIn("ON CONFLICT (warehouse_id, product_id) WHERE status = 'draft'", service)
        self.assertIn(
            "WHERE notification_type = 'low_stock' AND is_read = FALSE",
            service,
        )
        self.assertIn(
            "WHERE notification_type = 'expiry' AND is_read = FALSE",
            service,
        )
        self.assertIn(
            "WHERE notification_type = 'sensor_warning' AND is_read = FALSE",
            service,
        )

    def test_postgresql_migration_runbook_documents_safe_cutover(self) -> None:
        readme = (ROOT / "README.md").read_text()
        runbook = (ROOT / "docs" / "postgresql-migration-runbook.md").read_text()

        self.assertIn("docs/postgresql-migration-runbook.md", readme)
        self.assertNotIn("PostgreSQL runtime adapter is still a production migration task", readme)
        for snippet in (
            "Freeze Writes",
            "SQLite Preflight",
            "Load To PostgreSQL",
            "Reconcile",
            "Runtime Smoke",
            "Rollback",
            "scripts/sklad_sqlite_preflight.py",
            "scripts/sklad_sqlite_to_postgres.py",
            "scripts/sklad_postgres_reconcile.py",
            "scripts/sklad_postgres_runtime_smoke.py",
        ):
            with self.subTest(snippet=snippet):
                self.assertIn(snippet, runbook)
