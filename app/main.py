from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge, Histogram

from app.api.dependencies import get_database
from app.api.routes import router
from app.core.config import get_settings
from app.core.request_context import set_request_context, new_request_id
from app.services.background_jobs import PeriodicJobRunner, WarehouseBackgroundJobs
from app.services.warehouse import WarehouseService

# ── Business metrics ──────────────────────────────────────────────────────────
stock_movements_total = Counter(
    "sklad_stock_movements_total",
    "Total stock movement operations",
    ["movement_type", "warehouse_id"],
)
write_offs_total = Counter(
    "sklad_write_offs_total",
    "Total write-off operations",
    ["warehouse_id"],
)
receipts_total = Counter(
    "sklad_receipts_total",
    "Total receipt (incoming) operations",
    ["warehouse_id"],
)
purchase_requests_total = Counter(
    "sklad_purchase_requests_total",
    "Total purchase requests created",
    ["status"],
)
active_inventory_sessions = Gauge(
    "sklad_active_inventory_sessions",
    "Number of inventory sessions currently in progress",
)
active_auctions = Gauge(
    "sklad_active_auctions",
    "Number of currently active auctions",
)
low_stock_notifications = Gauge(
    "sklad_low_stock_notifications_pending",
    "Number of unread low-stock notifications",
)
# ─────────────────────────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    # Initialize OIDC if enabled
    if settings.oidc_enabled and settings.oidc_discovery_url:
        try:
            import httpx as _httpx
            from app.security.oidc import init_oidc
            discovery = _httpx.get(settings.oidc_discovery_url, timeout=5.0).json()
            jwks_uri = discovery.get("jwks_uri")
            if jwks_uri:
                init_oidc(jwks_uri)
            else:
                import logging as _logging
                _logging.getLogger(__name__).warning("OIDC discovery missing jwks_uri")
        except Exception:
            import logging as _logging
            _logging.getLogger(__name__).exception("Failed to initialize OIDC")
    runner: PeriodicJobRunner | None = None
    if settings.background_jobs_enabled:
        jobs = WarehouseBackgroundJobs(
            lambda: WarehouseService(get_database()),
            expiry_days=settings.background_jobs_expiry_days,
            actor_id=settings.background_jobs_actor_id,
            db=get_database(),
            telegram_bot_token=settings.telegram_bot_token,
            telegram_chat_id=settings.telegram_chat_id,
        )
        runner = PeriodicJobRunner(
            jobs,
            interval_seconds=settings.background_jobs_interval_seconds,
        )
        app.state.background_job_runner = runner
        runner.start()

    # Expose business metric objects on app.state so routes can update them
    app.state.metrics = {
        "stock_movements_total": stock_movements_total,
        "write_offs_total": write_offs_total,
        "receipts_total": receipts_total,
        "purchase_requests_total": purchase_requests_total,
        "active_inventory_sessions": active_inventory_sessions,
        "active_auctions": active_auctions,
        "low_stock_notifications": low_stock_notifications,
    }

    # Optional Redis Pub/Sub
    redis_url = settings.redis_url
    if redis_url:
        from app.services.pubsub import init_redis
        await init_redis(redis_url)

    try:
        yield
    finally:
        if runner:
            await runner.stop()
        from app.services.pubsub import close_redis
        await close_redis()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Medical warehouse accounting service",
        lifespan=lifespan,
    )

    # Prometheus HTTP instrumentation (request latency, counts, status codes)
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=False,
        excluded_handlers=["/metrics", "/sklad/metrics", "/health", "/sklad/health"],
    ).instrument(app)
    instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)
    instrumentator.expose(app, endpoint="/sklad/metrics", include_in_schema=False)

    app.include_router(router)
    app.include_router(router, prefix="/sklad")

    from app.api.payments import payment_router
    app.include_router(payment_router)

    @app.middleware("http")
    async def request_context_middleware(request, call_next):
        rid = request.headers.get("X-Request-Id") or new_request_id()
        # Real IP: respect X-Forwarded-For from nginx
        ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or request.headers.get("X-Real-IP", "")
            or (request.client.host if request.client else "")
        )
        ua = request.headers.get("User-Agent", "")
        set_request_context(rid, ip, ua)
        response = await call_next(request)
        response.headers["X-Request-Id"] = rid
        return response

    frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
    uploads_dir = Path(__file__).resolve().parents[1] / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    (uploads_dir / "certificates").mkdir(exist_ok=True)
    (uploads_dir / "products").mkdir(exist_ok=True)
    (uploads_dir / "catalog").mkdir(exist_ok=True)

    if frontend_dir.exists():
        # Uploads must be mounted before /sklad so that /sklad/uploads/ takes priority
        if uploads_dir.exists():
            app.mount("/sklad/uploads", StaticFiles(directory=uploads_dir), name="uploads_sklad")
        app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")
        app.mount("/sklad", StaticFiles(directory=frontend_dir, html=True), name="frontend_sklad")

        @app.get("/app", include_in_schema=False)
        def frontend_redirect():
            return RedirectResponse(url="/app/")

        @app.get("/sklad", include_in_schema=False)
        def sklad_frontend_redirect():
            return RedirectResponse(url="/sklad/")

        supplier_dir = frontend_dir / "supplier"
        if supplier_dir.exists():
            app.mount("/supplier", StaticFiles(directory=supplier_dir, html=True), name="supplier_frontend")

            @app.get("/supplier", include_in_schema=False)
            def supplier_frontend_redirect():
                return RedirectResponse(url="/supplier/")

    # Serve uploaded files at /uploads/ (internal/direct access)
    if uploads_dir.exists():
        app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

    return app


app = create_app()
