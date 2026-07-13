import hashlib
import hmac
import logging
from datetime import date
from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Body, Depends, File, Header, HTTPException, Query, Response, UploadFile, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.domain.errors import (
    AuthenticationError,
    BatchUnavailableError,
    ConflictError,
    InsufficientStockError,
    InventoryLockedError,
    NotFoundError,
    PermissionDeniedError,
    ValidationError,
)
from app.domain.schemas import (
    AbcXyzAnalysis,
    AbcXyzRunDetail,
    AbcXyzRunPage,
    AuditLogEntry,
    AuditLogPage,
    Balance,
    BalancePage,
    BatchDetail,
    BatchPriceLabel,
    BatchPriceLabelBatch,
    BatchPriceLabelBatchRequest,
    BatchStatusUpdate,
    Batch,
    BatchRecallCreate,
    BatchRecallPage,
    BatchRecallResult,
    BatchTransformationPage,
    BatchTraceability,
    Category,
    CategoryCreate,
    CategoryUpdate,
    ControlledSubstanceLedgerPage,
    ControlledSubstanceLedgerExport,
    DepartmentReturnDocumentCreate,
    DepartmentReturnCreate,
    FefoWriteOffResult,
    InventoryCreate,
    InventoryPrintForm,
    InventoryLine,
    InventoryLineCountUpdate,
    InventorySessionDetail,
    Notification,
    NotificationPage,
    ProductCreate,
    NotificationReadUpdate,
    Product,
    ProductBarcodeLabel,
    ProductBarcodeLabelBatch,
    ProductBarcodeLabelBatchRequest,
    PurchaseRequest,
    PurchaseRequestCreate,
    PurchaseRequestStatusUpdate,
    ProductUpdate,
    QuarantineReview,
    QuarantineReviewPage,
    QuarantineReviewProtocol,
    QuarantineReviewUpdate,
    ReceiptCreate,
    ReceiptDocumentCreate,
    RepackDocumentCreate,
    RepackPrintForm,
    Reservation,
    ReservationCreate,
    ReservationUseCreate,
    SafeStockDocumentDetail,
    SafeStockMovement,
    SensorDevice,
    SensorDeviceCreate,
    SensorDeviceUpdate,
    SensorReading,
    SensorReadingCreate,
    SensorReadingPage,
    StockDocumentDetail,
    StockDocumentPage,
    StockMovement,
    StockMovementPage,
    Supplier,
    SupplierApplication,
    SupplierApplicationCreate,
    SupplierApplicationPage,
    SupplierApplicationReview,
    SupplierApplicationReviewResponse,
    SupplierCreate,
    SupplierPriceHistoryPage,
    SupplierUpdate,
    SupplierReturnDocumentCreate,
    SupplierReturnResult,
    SupplierReturnCreate,
    TetisWarehouseMapping,
    TransferCreate,
    TransferDocumentCreate,
    TransferPrintForm,
    TransferResult,
    Warehouse,
    WarehouseCreate,
    WarehouseLockUpdate,
    WarehouseUpdate,
    WriteOffCreate,
    WriteOffFefoCreate,
    WriteOffDocumentCreate,
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserUpdate,
    UserOut,
    ShipmentCreate,
    ShipmentUpdate,
    Shipment,
    ShipmentPage,
)
from app.services.idempotency import IdempotencyStore, run_idempotent
from app.services.warehouse import WarehouseService
from app.realtime.manager import manager
from app.security.rbac import (
    ActorContext,
    Permission,
    Role,
    actor_from_headers,
    require_permission,
    require_permission_or_supplier,
    require_stock_access,
    require_supplier_scope,
    require_warehouse_filter,
)
from app.security.tokens import actor_from_bearer_token
from app.security.password import hash_password, verify_password

from fastapi import Request as Request  # noqa: F401
from .dependencies import (
    get_actor_context,
    get_database,
    get_database_readiness,
    get_idempotency_store,
    get_warehouse_service,
)

router = APIRouter(prefix="/api/v1")
logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/ready")
def readiness():
    readiness_status = get_database_readiness()
    if readiness_status["status"] != "ok":
        details = {
            key: value
            for key, value in readiness_status.items()
            if key not in {"status", "detail"}
        }
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": "service_unavailable",
                "message": readiness_status["detail"],
                "details": details,
            },
        )
    return readiness_status


@router.get("/admin/jobs")
def get_job_status(
    request: Request,
    db=Depends(get_database),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    require_permission(actor_ctx, Permission.ADMIN_USERS)
    runner = getattr(request.app.state, "background_job_runner", None)
    status_info = {
        "enabled": runner is not None,
        "is_running": getattr(runner, "is_running", False),
        "last_ran_at": getattr(runner, "last_ran_at", None),
        "last_result": None,
    }
    last = getattr(runner, "last_result", None)
    if last is not None:
        import dataclasses
        status_info["last_result"] = dataclasses.asdict(last)
    try:
        with db.transaction() as conn:
            rows = conn.execute(
                "SELECT id, job_name, status, started_at, finished_at, duration_ms, result_json, error_text "
                "FROM job_log ORDER BY started_at DESC LIMIT 20"
            ).fetchall()
        status_info["history"] = [dict(r) for r in (rows or [])]
    except Exception:
        status_info["history"] = []
    return status_info


@router.post("/admin/jobs/trigger")
async def trigger_jobs(
    request: Request,
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    require_permission(actor_ctx, Permission.ADMIN_USERS)
    runner = getattr(request.app.state, "background_job_runner", None)
    if runner is None:
        raise HTTPException(
            status_code=503,
            detail={"code": "jobs_disabled", "message": "Background jobs are disabled"},
        )
    if runner.is_running:
        raise HTTPException(
            status_code=409,
            detail={"code": "already_running", "message": "Jobs are already running"},
        )
    import asyncio
    asyncio.create_task(runner.run_once())
    return {"triggered": True}


@router.post("/admin/test-telegram", status_code=204)
def test_telegram_notification(
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        from app.services.telegram_notifier import notify_critical
        settings = get_settings()
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            raise ValidationError("Telegram не настроен (SKLAD_TELEGRAM_BOT_TOKEN, SKLAD_TELEGRAM_CHAT_ID)")
        notify_critical(settings.telegram_bot_token, settings.telegram_chat_id,
            "Тест", "Тестовое сообщение из системы склада. Telegram подключён!")
    except Exception as error:
        raise map_error(error) from error


@router.get("/me")
def current_actor(actor_ctx: ActorContext = Depends(get_actor_context)):
    response = {
        "actor_id": actor_ctx.actor_id,
        "roles": sorted(role.value for role in actor_ctx.roles),
        "warehouse_ids": sorted(actor_ctx.warehouse_ids),
        "department": actor_ctx.department,
        "supplier_id": actor_ctx.supplier_id,
        "permissions": sorted(permission.value for permission in actor_ctx.permissions),
    }
    # If JWT has no supplier_id, check DB — approval may have happened since last auth
    if actor_ctx.supplier_id is None:
        try:
            svc = get_warehouse_service()
            actor_id_str = actor_ctx.actor_id or ""
            db_user = None
            if actor_id_str and not actor_id_str.isdigit():
                db_user = svc.get_user_by_username(f"tetis:{actor_id_str}")
            elif actor_id_str and actor_id_str.isdigit():
                db_user = svc.get_user_by_id(int(actor_id_str))
            if db_user is not None and db_user.get("supplier_id"):
                response["access_needs_refresh"] = True
        except Exception:
            pass
    return response



class MeProfileUpdate(BaseModel):
    full_name: str

class MePasswordChange(BaseModel):
    current_password: str
    new_password: str

@router.patch("/me/profile", tags=["auth"])
def update_my_profile(body: MeProfileUpdate, actor_ctx: ActorContext = Depends(get_actor_context)):
    """Update own display name."""
    if not body.full_name or len(body.full_name.strip()) < 1:
        raise HTTPException(status_code=400, detail={"code": "bad_request", "message": "Name is required", "details": {}})
    svc = get_warehouse_service()
    actor_id = actor_ctx.actor_id
    user = (svc.get_user_by_id(int(actor_id)) if actor_id and actor_id.isdigit() else None) or svc.get_user_by_username(actor_id)
    if not user:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "User not found", "details": {}})
    svc.update_user(user["id"], {"full_name": body.full_name.strip()})
    return {"ok": True, "full_name": body.full_name.strip()}

@router.post("/me/password", tags=["auth"])
def change_my_password(body: MePasswordChange, actor_ctx: ActorContext = Depends(get_actor_context)):
    """Change own password (requires current password)."""
    if not body.new_password or len(body.new_password) < 8:
        raise HTTPException(status_code=400, detail={"code": "bad_request", "message": "Password must be at least 8 characters", "details": {}})
    svc = get_warehouse_service()
    actor_id = actor_ctx.actor_id
    user = (svc.get_user_by_id(int(actor_id)) if actor_id and actor_id.isdigit() else None) or svc.get_user_by_username(actor_id)
    if not user:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "User not found", "details": {}})
    user_full = svc.get_user_by_username(user["username"])
    if not user_full or not verify_password(body.current_password, user_full["password_hash"]):
        raise HTTPException(status_code=401, detail={"code": "unauthorized", "message": "Текущий пароль неверный", "details": {}})
    new_hash = hash_password(body.new_password)
    svc.update_user(user["id"], {"password_hash": new_hash})
    return {"ok": True}

@router.post("/auth/login", response_model=TokenResponse, tags=["auth"])
def login(body: LoginRequest) -> TokenResponse:
    """Authenticate with username and password, returns JWT."""
    settings = get_settings()
    if not settings.jwt_hmac_secret:
        raise HTTPException(status_code=500, detail={"code": "server_error", "message": "JWT not configured", "details": {}})
    svc = get_warehouse_service()
    user = svc.get_user_by_username(body.username)
    if user is None or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail={"code": "unauthorized", "message": "Invalid credentials", "details": {}})
    import time, json as _json
    roles = [r.strip() for r in user["roles"].split(",") if r.strip()]
    wh_ids = user["warehouse_ids"]
    if isinstance(wh_ids, str):
        wh_ids = _json.loads(wh_ids)
    wh_ids = wh_ids or []
    now = int(time.time())
    payload = {
        "sub": str(user["id"]),
        "iss": settings.jwt_issuer or "tetis",
        "aud": settings.jwt_audience or "sklad",
        "iat": now,
        "exp": now + 8 * 3600,
        "roles": roles,
        "warehouse_ids": wh_ids,
        "full_name": user["full_name"],
        "username": user["username"],
    }
    if user.get("department"):
        payload["department"] = user["department"]
    if user.get("supplier_id") is not None:
        payload["supplier_id"] = user["supplier_id"]
        if "supplier" not in roles:
            payload["roles"] = roles + ["supplier"]
    from app.security.tokens import encode_jwt_hs256
    token = encode_jwt_hs256(payload, settings.jwt_hmac_secret)
    return TokenResponse(access_token=token)


from app.domain.schemas import SupplierLoginRequest, SupplierPortalAccessResponse  # noqa: E402, F811


class RegisterRequest(BaseModel):
    username: str
    full_name: str
    password: str
    role: str = "warehouse_manager"


@router.post("/auth/register", response_model=TokenResponse, status_code=201, tags=["auth"])
def register(body: RegisterRequest) -> TokenResponse:
    """Self-registration for standalone sklad. Creates a new user and returns a JWT."""
    allowed_roles = {"warehouse_manager", "supplier"}
    if body.role not in allowed_roles:
        raise HTTPException(status_code=400, detail={"code": "bad_request", "message": "Invalid role", "details": {}})
    if not body.username or len(body.username) < 3:
        raise HTTPException(status_code=400, detail={"code": "bad_request", "message": "Username must be at least 3 characters", "details": {}})
    if not body.password or len(body.password) < 8:
        raise HTTPException(status_code=400, detail={"code": "bad_request", "message": "Password must be at least 8 characters", "details": {}})
    settings = get_settings()
    if not settings.jwt_hmac_secret:
        raise HTTPException(status_code=500, detail={"code": "server_error", "message": "JWT not configured", "details": {}})
    svc = get_warehouse_service()
    existing = svc.get_user_by_username(body.username)
    if existing:
        raise HTTPException(status_code=409, detail={"code": "conflict", "message": "Пользователь с таким логином уже существует", "details": {}})
    pw_hash = hash_password(body.password)

    supplier_id = None
    if body.role == "supplier":
        # Auto-create supplier record and link to user
        from app.domain.schemas import SupplierCreate
        supplier_data = SupplierCreate(name=body.full_name)
        supplier = svc.create_supplier(supplier_data, actor_id="register")
        supplier_id = supplier["id"]
        user = svc.create_user(body.username, body.full_name, pw_hash, [body.role], [], None, supplier_id)
    else:
        user = svc.create_user(body.username, body.full_name, pw_hash, [body.role], [], None, None)

    import time
    roles = [body.role]
    now = int(time.time())
    payload = {
        "sub": str(user["id"]),
        "iss": settings.jwt_issuer or "sklad",
        "aud": settings.jwt_audience or "sklad",
        "iat": now,
        "exp": now + 8 * 3600,
        "roles": roles,
        "warehouse_ids": [],
        "full_name": body.full_name,
        "username": body.username,
    }
    if supplier_id is not None:
        payload["supplier_id"] = supplier_id
    from app.security.tokens import encode_jwt_hs256
    token = encode_jwt_hs256(payload, settings.jwt_hmac_secret)
    return TokenResponse(access_token=token)


@router.post("/auth/supplier-login", response_model=TokenResponse, tags=["auth"])
def supplier_login(body: SupplierLoginRequest) -> TokenResponse:
    """Authenticate a supplier with email and password, returns a JWT scoped
    to that supplier (Role.SUPPLIER + supplier_id claim, no warehouse_ids)."""
    settings = get_settings()
    if not settings.jwt_hmac_secret:
        raise HTTPException(status_code=500, detail={"code": "server_error", "message": "JWT not configured", "details": {}})
    svc = get_warehouse_service()
    supplier = svc.get_supplier_by_email(body.email)
    if supplier is None or not verify_password(body.password, supplier["password_hash"]):
        raise HTTPException(status_code=401, detail={"code": "unauthorized", "message": "Invalid credentials", "details": {}})
    import time
    now = int(time.time())
    payload = {
        "sub": f"supplier:{supplier['id']}",
        "iss": settings.jwt_issuer or "tetis",
        "aud": settings.jwt_audience or "sklad",
        "iat": now,
        "exp": now + 8 * 3600,
        "roles": ["supplier"],
        "warehouse_ids": [],
        "supplier_id": supplier["id"],
        "full_name": supplier["name"],
        "username": supplier["email"],
    }
    from app.security.tokens import encode_jwt_hs256
    token = encode_jwt_hs256(payload, settings.jwt_hmac_secret)
    return TokenResponse(access_token=token)


@router.post(
    "/suppliers/{supplier_id}/portal-access",
    response_model=SupplierPortalAccessResponse,
    tags=["catalog"],
    summary="Grant/rotate a supplier's portal login (staff only)",
)
def grant_supplier_portal_access(
    supplier_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> SupplierPortalAccessResponse:
    """Generates a fresh password for the supplier's portal login. The
    plaintext is returned exactly once in this response — it is never
    stored anywhere, only its bcrypt hash. Staff must relay it to the
    supplier themselves (phone/email outside the system)."""
    require_permission(actor_ctx, Permission.ADMIN_USERS)
    import secrets
    generated_password = secrets.token_urlsafe(9)
    updated = service.set_supplier_portal_access(supplier_id, hash_password(generated_password), actor_ctx.actor_id)
    if not updated.get("email"):
        raise HTTPException(status_code=422, detail={"code": "validation_error", "message": "У поставщика не указан email", "details": {}})
    return SupplierPortalAccessResponse(
        supplier_id=supplier_id, email=updated["email"], generated_password=generated_password,
    )


@router.delete(
    "/suppliers/{supplier_id}/portal-access",
    tags=["catalog"],
    summary="Revoke a supplier's portal login (staff only)",
)
def revoke_supplier_portal_access(
    supplier_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    require_permission(actor_ctx, Permission.ADMIN_USERS)
    service.revoke_supplier_portal_access(supplier_id, actor_ctx.actor_id)
    return {"supplier_id": supplier_id, "portal_access_enabled": False}


@router.post("/supplier-applications", status_code=status.HTTP_201_CREATED, response_model=SupplierApplication, tags=["suppliers"])
def submit_supplier_application(
    payload: SupplierApplicationCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    authorization: str | None = Header(default=None),
) -> SupplierApplication:
    try:
        # Anonymous (cold) submissions are keyed by email. If the request carries a
        # valid sklad/tetis bearer token, key the application to that real tetis
        # actor instead — this lets approval auto-link the requester's account
        # (sklad_users.supplier_id) without an admin manually typing an ID.
        actor_id = payload.email
        if authorization:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() == "bearer" and token.strip():
                settings = get_settings()
                if settings.jwt_hmac_secret:
                    try:
                        actor_ctx = actor_from_bearer_token(
                            token.strip(),
                            secret=settings.jwt_hmac_secret,
                            issuer=settings.jwt_issuer,
                            audience=settings.jwt_audience,
                            leeway_seconds=settings.jwt_clock_skew_seconds,
                        )
                        actor_id = f"tetis-actor:{actor_ctx.actor_id}"
                    except Exception:
                        pass
        return service.submit_supplier_application(payload, actor_id=actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/tetis/supplier-applications", response_model=SupplierApplicationPage, tags=["suppliers"])
def list_supplier_applications(
    status_filter: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_supplier_applications(status_filter, safe_limit, safe_offset),
            "total": service.count_supplier_applications(status_filter),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/tetis/supplier-applications/{application_id}", response_model=SupplierApplication, tags=["suppliers"])
def get_supplier_application(
    application_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        return service.get_supplier_application(application_id)
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/tetis/supplier-applications/{application_id}/review",
    response_model=SupplierApplicationReviewResponse,
    tags=["suppliers"],
)
def review_supplier_application(
    application_id: int,
    payload: SupplierApplicationReview,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        application = service.review_supplier_application(
            application_id,
            payload,
            reviewer_id=actor_ctx.actor_id,
            password_hash=None,
        )
        return {
            "application": application,
            "supplier_id": application.get("supplier_id"),
            "email": application.get("email"),
            "generated_password": None,
        }
    except Exception as error:
        raise map_error(error) from error


@router.post("/sklad/token", response_model=TokenResponse, tags=["auth"])
def exchange_tetis_token(
    body: dict = Body(default={}),
    authorization: str | None = Header(default=None),
) -> TokenResponse:
    """Exchange a Tetis platform JWT for a sklad JWT."""
    settings = get_settings()
    if not settings.jwt_hmac_secret:
        raise HTTPException(status_code=500, detail={"code": "server_error", "message": "JWT not configured", "details": {}})
    if not authorization:
        raise HTTPException(status_code=401, detail={"code": "unauthorized", "message": "Bearer token required", "details": {}})
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(status_code=401, detail={"code": "unauthorized", "message": "Bearer token required", "details": {}})
    TETIS_SECRETS = ["local-dev-secret", "HcYnreHTy__68b2O1Zn1CACarfle5YjgBvT7syWg4Sg"]
    if settings.mis_sso_secret:
        TETIS_SECRETS = TETIS_SECRETS + [settings.mis_sso_secret]
    payload = None
    for _secret in TETIS_SECRETS:
        try:
            from app.security.tokens import decode_jwt_hs256
            payload = decode_jwt_hs256(token.strip(), secret=_secret)
            break
        except Exception:
            continue
    if payload is None:
        raise HTTPException(status_code=401, detail={"code": "unauthorized", "message": "Invalid Tetis token", "details": {}})
    tetis_user_id = payload.get("sub", "")
    print(f"TETIS_EXCHANGE sub={tetis_user_id} role={payload.get('role','')}", flush=True)
    svc = get_warehouse_service()
    mis_clinic_id = payload.get("mis_clinic_id")
    if mis_clinic_id:
        # Embedded from the MIS sidebar (see docs/tetis-sso-acl.md for the Tetis equivalent):
        # MIS already mapped its own role to a sklad role and put it in the `role` claim;
        # scope warehouse access to whatever warehouses are mapped to this MIS clinic.
        roles = [payload.get("role") or "warehouse_manager"]
        wh_ids = svc.list_warehouse_ids_by_mis_clinic(str(mis_clinic_id))
        full_name = payload.get("full_name") or tetis_user_id
        actor_id = tetis_user_id
        supplier_id = None
    elif (user := svc.get_user_by_username(f"tetis:{tetis_user_id}")) is None:
        roles = ["warehouse_manager"]
        wh_ids = []
        full_name = tetis_user_id
        actor_id = tetis_user_id
        supplier_id = None
    else:
        import json as _json
        roles = [r.strip() for r in user["roles"].split(",") if r.strip()]
        wh_ids = user["warehouse_ids"]
        if isinstance(wh_ids, str):
            wh_ids = _json.loads(wh_ids)
        wh_ids = wh_ids or []
        full_name = user["full_name"]
        actor_id = str(user["id"])
        supplier_id = user.get("supplier_id")
    import time
    now = int(time.time())
    sklad_payload = {
        "sub": actor_id,
        "iss": settings.jwt_issuer or "tetis",
        "aud": settings.jwt_audience or "sklad",
        "iat": now,
        "exp": now + 8 * 3600,
        "roles": roles,
        "warehouse_ids": wh_ids,
        "full_name": full_name,
    }
    if supplier_id is not None:
        sklad_payload["supplier_id"] = supplier_id
        if "supplier" not in roles:
            sklad_payload["roles"] = roles + ["supplier"]
    from app.security.tokens import encode_jwt_hs256
    sklad_token = encode_jwt_hs256(sklad_payload, settings.jwt_hmac_secret)
    return TokenResponse(access_token=sklad_token)


@router.post("/cameras-token", tags=["auth"])
def get_cameras_token(
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> dict:
    """Issue a short-lived cameras-system JWT for the current sklad user.

    The cameras backend verifies this token at POST /api/sso/tetis-exchange
    using the shared CAMERAS_SSO_SECRET / SKLAD_CAMERAS_SSO_SECRET.
    """
    settings = get_settings()
    if not settings.cameras_sso_secret:
        raise HTTPException(
            status_code=503,
            detail={"code": "cameras_not_configured", "message": "Camera system is not enabled on this server", "details": {}},
        )

    svc = get_warehouse_service()

    # Resolve the company identifier (tetis_org_id from warehouses).
    # Falls back to the smallest warehouse_id so isolation is always enforced.
    tenant_id: int | None = None
    if actor_ctx.warehouse_ids:
        org_id_str = svc.get_tetis_org_id_for_warehouses(list(actor_ctx.warehouse_ids))
        if org_id_str:
            try:
                tenant_id = int(org_id_str)
            except (ValueError, TypeError):
                import hashlib as _hl
                tenant_id = int(_hl.sha256(org_id_str.encode()).hexdigest()[:8], 16) % 2147483647

    if tenant_id is None:
        if actor_ctx.warehouse_ids:
            tenant_id = min(actor_ctx.warehouse_ids)
        else:
            raise HTTPException(
                status_code=403,
                detail={"code": "no_warehouse_scope", "message": "No warehouse scope assigned", "details": {}},
            )

    # Map sklad role to cameras role
    role_names = {r.value if hasattr(r, "value") else str(r) for r in actor_ctx.roles}
    cameras_role = "admin" if role_names & {"warehouse_manager", "head_nurse"} else "employee"

    import time as _time
    from app.security.tokens import encode_jwt_hs256 as _encode
    now = int(_time.time())
    cameras_payload = {
        "org_id": str(tenant_id),
        "role": cameras_role,
        "iat": now,
        "exp": now + 900,  # 15 minutes — cameras frontend re-exchanges on page load
    }
    token = _encode(cameras_payload, settings.cameras_sso_secret)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users", response_model=list[UserOut], tags=["users"])
def list_users(actor_ctx: ActorContext = Depends(get_actor_context)) -> list[UserOut]:
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        svc = get_warehouse_service()
        users = svc.list_users()
        return [_user_row_to_out(u) for u in users]
    except Exception as error:
        raise map_error(error) from error


@router.post("/users", status_code=201, response_model=UserOut, tags=["users"])
def create_user(body: UserCreate, actor_ctx: ActorContext = Depends(get_actor_context)) -> UserOut:
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        svc = get_warehouse_service()
        existing = svc.get_user_by_username(body.username)
        if existing:
            raise HTTPException(status_code=409, detail={"code": "conflict", "message": "Username already exists", "details": {}})
        pw_hash = hash_password(body.password)
        user = svc.create_user(body.username, body.full_name, pw_hash, body.roles, body.warehouse_ids, body.department, body.supplier_id)
        return _user_row_to_out(user)
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.get("/users/{user_id}", response_model=UserOut, tags=["users"])
def get_user(user_id: int, actor_ctx: ActorContext = Depends(get_actor_context)) -> UserOut:
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        svc = get_warehouse_service()
        user = svc.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "User not found", "details": {}})
        return _user_row_to_out(user)
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.patch("/users/{user_id}", response_model=UserOut, tags=["users"])
def update_user(user_id: int, body: UserUpdate, actor_ctx: ActorContext = Depends(get_actor_context)) -> UserOut:
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        svc = get_warehouse_service()
        updates = body.model_dump(exclude_unset=True)
        if "password" in updates:
            updates["password_hash"] = hash_password(updates.pop("password"))
        user = svc.update_user(user_id, updates)
        if user is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "User not found", "details": {}})
        return _user_row_to_out(user)
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.delete("/users/{user_id}", status_code=204, tags=["users"])
def deactivate_user(user_id: int, actor_ctx: ActorContext = Depends(get_actor_context)) -> None:
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        svc = get_warehouse_service()
        svc.update_user(user_id, {"is_active": False})
    except Exception as error:
        raise map_error(error) from error


def _user_row_to_out(row: dict) -> UserOut:
    import json as _json
    roles = [r.strip() for r in row["roles"].split(",") if r.strip()]
    wh_ids = row["warehouse_ids"]
    if isinstance(wh_ids, str):
        wh_ids = _json.loads(wh_ids)
    return UserOut(
        id=row["id"],
        username=row["username"],
        full_name=row["full_name"],
        roles=roles,
        warehouse_ids=wh_ids or [],
        department=row.get("department"),
        supplier_id=row.get("supplier_id"),
        is_active=row["is_active"],
        created_at=str(row["created_at"]),
    )


def actor(actor_ctx: ActorContext = Depends(get_actor_context)) -> str:
    return actor_ctx.actor_id


def map_error(error: Exception) -> HTTPException:
    if isinstance(error, NotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "not_found", "message": str(error), "details": {}},
        )
    if isinstance(error, (ConflictError, InsufficientStockError, InventoryLockedError, BatchUnavailableError)):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "conflict", "message": str(error), "details": {}},
        )
    if isinstance(error, PermissionDeniedError):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "forbidden", "message": str(error), "details": {}},
        )
    if isinstance(error, ValidationError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "validation_error", "message": str(error), "details": {}},
        )
    if isinstance(error, ValueError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "bad_request", "message": str(error), "details": {}},
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={"code": "internal_error", "message": "Internal error", "details": {}},
    )


async def publish_event(event: str, payload: dict) -> None:
    try:
        await manager.broadcast(event, payload)
    except Exception:
        logger.exception("Failed to publish realtime event %s", event)


def require_batch_read_scope(
    service: WarehouseService, actor_ctx: ActorContext, batch_id: int
) -> None:
    warehouse_ids = service.get_batch_warehouse_ids(batch_id)
    if not warehouse_ids:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return
    for warehouse_id in warehouse_ids:
        require_stock_access(actor_ctx, Permission.STOCK_READ, warehouse_id)


@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=Category)
def create_category(
    data: CategoryCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.create_category(data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/categories", response_model=list[Category])
def list_categories(
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_categories(safe_limit, safe_offset, q=q)
    except Exception as error:
        raise map_error(error) from error


@router.patch("/categories/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.update_category(category_id, data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.delete("/categories/{category_id}", response_model=Category)
def delete_category(
    category_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.delete_category(category_id, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/suppliers", status_code=status.HTTP_201_CREATED, response_model=Supplier)
def create_supplier(
    data: SupplierCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.create_supplier(data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/suppliers", response_model=list[Supplier])
def list_suppliers(
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_suppliers(safe_limit, safe_offset, q=q)
    except Exception as error:
        raise map_error(error) from error


@router.get("/suppliers/{supplier_id}/price-history", response_model=SupplierPriceHistoryPage)
def list_supplier_price_history(
    supplier_id: int,
    product_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission_or_supplier(actor_ctx, Permission.STOCK_READ)
        require_supplier_scope(actor_ctx, supplier_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_supplier_price_history(supplier_id, product_id, safe_limit, safe_offset),
            "total": service.count_supplier_price_history(supplier_id, product_id),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.patch("/suppliers/{supplier_id}", response_model=Supplier)
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.update_supplier(supplier_id, data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/warehouses", status_code=status.HTTP_201_CREATED, response_model=Warehouse)
def create_warehouse(
    data: WarehouseCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.create_warehouse(data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/warehouses", response_model=list[Warehouse])
def list_warehouses(
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_warehouses(safe_limit, safe_offset, q=q)
    except Exception as error:
        raise map_error(error) from error


@router.get("/tetis/orgs/{tetis_org_id}/warehouse-ids", response_model=TetisWarehouseMapping)
def resolve_tetis_warehouse_ids(
    tetis_org_id: str,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        return {
            "tetis_org_id": tetis_org_id.strip(),
            "warehouse_ids": service.list_warehouse_ids_for_tetis_org(tetis_org_id),
        }
    except Exception as error:
        raise map_error(error) from error


@router.patch("/warehouses/{warehouse_id}", response_model=Warehouse)
def update_warehouse(
    warehouse_id: int,
    data: WarehouseUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.update_warehouse(warehouse_id, data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.patch("/warehouses/{warehouse_id}/inventory-lock", response_model=Warehouse)
def set_inventory_lock(
    warehouse_id: int,
    data: WarehouseLockUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_stock_access(actor_ctx, Permission.INVENTORY_MANAGE, warehouse_id)
        return service.set_inventory_lock(warehouse_id, data.inventory_lock, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/sensor-devices", status_code=status.HTTP_201_CREATED, response_model=SensorDevice)
def create_sensor_device(
    data: SensorDeviceCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_stock_access(actor_ctx, Permission.CATALOG_WRITE, data.warehouse_id)
        return service.create_sensor_device(data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/sensor-devices", response_model=list[SensorDevice])
def list_sensor_devices(
    warehouse_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_sensor_devices(warehouse_id, safe_limit, safe_offset)
    except Exception as error:
        raise map_error(error) from error


@router.patch("/sensor-devices/{device_id}", response_model=SensorDevice)
def update_sensor_device(
    device_id: int,
    data: SensorDeviceUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        current = service.get_sensor_device(device_id)
        require_stock_access(actor_ctx, Permission.CATALOG_WRITE, current["warehouse_id"])
        require_stock_access(actor_ctx, Permission.CATALOG_WRITE, data.warehouse_id)
        return service.update_sensor_device(device_id, data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/sensor-readings", status_code=status.HTTP_201_CREATED, response_model=SensorReading)
async def record_sensor_reading(
    data: SensorReadingCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        device = service.get_sensor_device(data.device_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, device["warehouse_id"])
        reading = service.record_sensor_reading(data, actor_id)
        await publish_event(
            "sensor.reading.created",
            {
                "device_id": reading["device_id"],
                "warehouse_id": reading["warehouse_id"],
                "temperature_c": reading["temperature_c"],
                "humidity_percent": reading["humidity_percent"],
                "status": reading["status"],
            },
        )
        if reading["status"] == "warning":
            await publish_event(
                "notifications.updated",
                {
                    "notification_type": "sensor_warning",
                    "warehouse_id": reading["warehouse_id"],
                    "device_id": reading["device_id"],
                },
            )
        return reading
    except Exception as error:
        raise map_error(error) from error


@router.get("/sensor-readings", response_model=SensorReadingPage)
def list_sensor_readings(
    warehouse_id: int | None = None,
    device_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        if device_id is not None:
            device = service.get_sensor_device(device_id)
            require_stock_access(actor_ctx, Permission.STOCK_READ, device["warehouse_id"])
        else:
            require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_sensor_readings(
                warehouse_id=warehouse_id,
                device_id=device_id,
                limit=safe_limit,
                offset=safe_offset,
            ),
            "total": service.count_sensor_readings(
                warehouse_id=warehouse_id,
                device_id=device_id,
            ),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/product-units", response_model=list[str])
def list_product_units(
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.list_product_units()
    except Exception as error:
        raise map_error(error) from error


@router.get("/products", response_model=list[Product])
def list_products(
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_products(safe_limit, safe_offset, q=q)
    except Exception as error:
        raise map_error(error) from error


@router.post("/products", status_code=status.HTTP_201_CREATED, response_model=Product)
def create_product(
    data: ProductCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.create_product(data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.patch("/products/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    data: ProductUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.update_product(product_id, data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.delete("/products/{product_id}", response_model=Product)
def delete_product(
    product_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.delete_product(product_id, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/products/{product_id}/barcode-label", response_model=ProductBarcodeLabel)
def get_product_barcode_label(
    product_id: int,
    symbology: str = "code128",
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.get_product_barcode_label(product_id, symbology=symbology)
    except Exception as error:
        raise map_error(error) from error


@router.get("/products/by-barcode/{barcode}", response_model=Product)
def get_product_by_barcode(
    barcode: str,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        product = service.get_product_by_barcode(barcode)
        if product is None:
            raise NotFoundError(f"Товар со штрихкодом «{barcode}» не найден")
        return product
    except Exception as error:
        raise map_error(error) from error


@router.post("/products/barcode-labels", response_model=ProductBarcodeLabelBatch)
def get_product_barcode_labels(
    data: ProductBarcodeLabelBatchRequest,
    symbology: str = "code128",
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.get_product_barcode_labels(data.product_ids, symbology=symbology)
    except Exception as error:
        raise map_error(error) from error


@router.get("/batches", response_model=list[Batch])
def list_batches(
    warehouse_id: int | None = None,
    product_id: int | None = None,
    supplier_id: int | None = None,
    status: str | None = None,
    expires_before: date | None = None,
    expires_after: date | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_batches(
            warehouse_id=warehouse_id,
            limit=safe_limit,
            offset=safe_offset,
            product_id=product_id,
            supplier_id=supplier_id,
            status=status,
            expires_before=expires_before,
            expires_after=expires_after,
        )
    except Exception as error:
        raise map_error(error) from error


@router.post("/batches/price-labels", response_model=BatchPriceLabelBatch)
def get_batch_price_labels(
    data: BatchPriceLabelBatchRequest,
    symbology: str = "code128",
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.get_batch_price_labels(data.batch_ids, symbology=symbology)
    except Exception as error:
        raise map_error(error) from error


@router.get("/batches/{batch_id}", response_model=BatchDetail)
def get_batch(
    batch_id: int,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_batch_read_scope(service, actor_ctx, batch_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.get_batch_detail(batch_id, safe_limit, safe_offset)
    except Exception as error:
        raise map_error(error) from error


@router.get("/batches/{batch_id}/price-label", response_model=BatchPriceLabel)
def get_batch_price_label(
    batch_id: int,
    symbology: str = "code128",
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_batch_read_scope(service, actor_ctx, batch_id)
        return service.get_batch_price_label(batch_id, symbology=symbology)
    except Exception as error:
        raise map_error(error) from error


@router.get("/batches/{batch_id}/movements", response_model=list[SafeStockMovement])
def get_batch_movements(
    batch_id: int,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_batch_read_scope(service, actor_ctx, batch_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_stock_movements(batch_id=batch_id, limit=safe_limit, offset=safe_offset)
    except Exception as error:
        raise map_error(error) from error


@router.get("/batches/{batch_id}/traceability", response_model=BatchTraceability)
def get_batch_traceability(
    batch_id: int,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_batch_read_scope(service, actor_ctx, batch_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.get_batch_traceability(batch_id, safe_limit, safe_offset)
    except Exception as error:
        raise map_error(error) from error


class ReceiptPrintForm(BaseModel):
    document_type: str = "receipt"
    batch_id: int
    product_name: str
    sku: str | None
    lot: str
    serial_number: str | None
    expires_on: str | None
    unit_price: str
    quantity: str
    unit: str | None
    warehouse_name: str
    supplier_name: str
    received_at: str
    barcode: str | None


@router.get("/batches/{batch_id}/receipt-print-form", response_model=ReceiptPrintForm)
def get_batch_receipt_print_form(
    batch_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_batch_read_scope(service, actor_ctx, batch_id)
        return service.get_batch_receipt_print_form(batch_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/batches/{batch_id}/recall", response_model=BatchRecallResult)
async def recall_batch(
    batch_id: int,
    data: BatchRecallCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        warehouse_ids = service.get_batch_warehouse_ids(batch_id)
        for warehouse_id in warehouse_ids:
            require_stock_access(actor_ctx, Permission.DOCUMENT_POST, warehouse_id)
        result, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/batches/{batch_id}/recall",
            payload=data,
            response_status=status.HTTP_200_OK,
            resource_type="batch_recall",
            operation=lambda: service.recall_batch(batch_id, data, actor_id),
        )
        if not replayed:
            await publish_event(
                "batch.recalled",
                {
                    "batch_id": batch_id,
                    "warehouse_ids": [row["warehouse_id"] for row in result["affected_warehouses"]],
                },
            )
            await publish_event(
                "batch.status.updated",
                {"batch_id": batch_id, "status": result["batch"]["status"]},
            )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.get("/batch-recalls", response_model=BatchRecallPage)
def list_batch_recalls(
    batch_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        if batch_id is not None:
            require_batch_read_scope(service, actor_ctx, batch_id)
        elif actor_ctx.warehouse_ids:
            raise PermissionDeniedError("Batch filter is required for scoped actor")
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_batch_recalls(batch_id=batch_id, limit=safe_limit, offset=safe_offset),
            "total": service.count_batch_recalls(batch_id=batch_id),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.post("/batches/{batch_id}/unblock")
async def unblock_batch(
    batch_id: int,
    data: dict = Body(default={"reason": ""}),
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        warehouse_ids = service.get_batch_warehouse_ids(batch_id)
        for warehouse_id in warehouse_ids:
            require_stock_access(actor_ctx, Permission.DOCUMENT_POST, warehouse_id)
        result = service.unblock_batch(batch_id, reason=data.get("reason", ""), actor_id=actor_id)
        await publish_event("batch.status.updated", {"batch_id": batch_id, "status": result["status"]})
        return result
    except Exception as error:
        raise map_error(error) from error


@router.get("/recalls/stats")
def recall_stats(
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.get_recall_stats()
    except Exception as error:
        raise map_error(error) from error


@router.post("/receipts", status_code=status.HTTP_201_CREATED, response_model=Batch)
async def receive(
    data: ReceiptCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_RECEIVE, data.warehouse_id)
        batch, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/receipts",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="batch",
            operation=lambda: service.receive(data, actor_id),
        )
        if not replayed:
            await publish_event(
                "stock.balance.updated",
                {"product_id": data.product_id, "batch_id": batch["id"], "warehouse_id": data.warehouse_id},
            )
        return batch
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/stock-documents/receipts",
    status_code=status.HTTP_201_CREATED,
    response_model=StockDocumentDetail,
)
def create_receipt_document(
    data: ReceiptDocumentCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, data.warehouse_id)
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/stock-documents/receipts",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_document",
            operation=lambda: service.create_receipt_document(data, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/stock-documents/write-offs",
    status_code=status.HTTP_201_CREATED,
    response_model=StockDocumentDetail,
)
def create_writeoff_document(
    data: WriteOffDocumentCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, data.warehouse_id)
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/stock-documents/write-offs",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_document",
            operation=lambda: service.create_writeoff_document(data, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/stock-documents/transfers",
    status_code=status.HTTP_201_CREATED,
    response_model=StockDocumentDetail,
)
def create_transfer_document(
    data: TransferDocumentCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, data.source_warehouse_id)
        for line in data.lines:
            require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, line.target_warehouse_id)
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/stock-documents/transfers",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_document",
            operation=lambda: service.create_transfer_document(data, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/stock-documents/returns/from-department",
    status_code=status.HTTP_201_CREATED,
    response_model=StockDocumentDetail,
)
def create_department_return_document(
    data: DepartmentReturnDocumentCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, data.source_warehouse_id)
        for line in data.lines:
            require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, line.target_warehouse_id)
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/stock-documents/returns/from-department",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_document",
            operation=lambda: service.create_department_return_document(data, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/stock-documents/returns/to-supplier",
    status_code=status.HTTP_201_CREATED,
    response_model=StockDocumentDetail,
)
def create_supplier_return_document(
    data: SupplierReturnDocumentCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, data.warehouse_id)
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/stock-documents/returns/to-supplier",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_document",
            operation=lambda: service.create_supplier_return_document(data, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.get("/stock-documents/{document_id}", response_model=SafeStockDocumentDetail)
def get_stock_document(
    document_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        document = service.get_stock_document(document_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, document["warehouse_id"])
        return document
    except Exception as error:
        raise map_error(error) from error


@router.get("/stock-documents/{document_id}/repack-print-form", response_model=RepackPrintForm)
def get_repack_print_form(
    document_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        form = service.get_repack_print_form(document_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, form["warehouse_id"])
        return form
    except Exception as error:
        raise map_error(error) from error


@router.get("/stock-documents/{document_id}/transfer-print-form", response_model=TransferPrintForm)
def get_transfer_print_form(
    document_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        form = service.get_transfer_print_form(document_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, form["source_warehouse_id"])
        for line in form["lines"]:
            require_stock_access(actor_ctx, Permission.STOCK_READ, line["target_warehouse_id"])
        return form
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/stock-documents/repack",
    status_code=status.HTTP_201_CREATED,
    response_model=StockDocumentDetail,
)
def create_repack_document(
    data: RepackDocumentCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, data.warehouse_id)
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/stock-documents/repack",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_document",
            operation=lambda: service.create_repack_document(data, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.get("/stock-documents", response_model=StockDocumentPage)
def list_stock_documents(
    warehouse_id: int | None = None,
    document_type: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        items = [
            service.get_stock_document(document["id"])
            for document in service.list_stock_documents(
                warehouse_id=warehouse_id,
                limit=safe_limit,
                offset=safe_offset,
                document_type=document_type,
                status=status,
            )
        ]
        return {
            "items": items,
            "total": service.count_stock_documents(
                warehouse_id=warehouse_id,
                document_type=document_type,
                status=status,
            ),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/batch-transformations", response_model=BatchTransformationPage)
def list_batch_transformations(
    warehouse_id: int | None = None,
    batch_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_batch_transformations(
                warehouse_id=warehouse_id,
                batch_id=batch_id,
                limit=safe_limit,
                offset=safe_offset,
            ),
            "total": service.count_batch_transformations(
                warehouse_id=warehouse_id,
                batch_id=batch_id,
            ),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.post("/stock-documents/{document_id}/post", response_model=StockDocumentDetail)
async def post_stock_document(
    document_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        document_for_scope = service.get_stock_document(document_id)
        require_stock_access(actor_ctx, Permission.DOCUMENT_POST, document_for_scope["warehouse_id"])
        document, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/stock-documents/{document_id}/post",
            payload={"document_id": document_id},
            response_status=status.HTTP_200_OK,
            resource_type="stock_document",
            operation=lambda: service.post_stock_document(document_id, actor_id),
        )
        if not replayed:
            await publish_event(
                "stock.document.posted",
                {
                    "id": document["id"],
                    "document_type": document["document_type"],
                    "warehouse_id": document["warehouse_id"],
                },
            )
            await publish_event(
                "stock.balance.updated",
                {"warehouse_id": document["warehouse_id"], "document_id": document["id"]},
            )
            for line in document["lines"]:
                if line.get("target_warehouse_id") is not None:
                    await publish_event(
                        "stock.balance.updated",
                        {
                            "warehouse_id": line["target_warehouse_id"],
                            "document_id": document["id"],
                            "batch_id": line["batch_id"],
                        },
                    )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.post("/stock-documents/{document_id}/approve", response_model=StockDocumentDetail)
def approve_stock_document(
    document_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        document_for_scope = service.get_stock_document(document_id)
        require_stock_access(actor_ctx, Permission.DOCUMENT_POST, document_for_scope["warehouse_id"])
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/stock-documents/{document_id}/approve",
            payload={"document_id": document_id},
            response_status=status.HTTP_200_OK,
            resource_type="stock_document",
            operation=lambda: service.approve_stock_document(document_id, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.post("/stock-documents/{document_id}/cancel", response_model=StockDocumentDetail)
def cancel_stock_document(
    document_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        document_for_scope = service.get_stock_document(document_id)
        require_stock_access(actor_ctx, Permission.DOCUMENT_POST, document_for_scope["warehouse_id"])
        document, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/stock-documents/{document_id}/cancel",
            payload={"document_id": document_id},
            response_status=status.HTTP_200_OK,
            resource_type="stock_document",
            operation=lambda: service.cancel_stock_document(document_id, actor_id),
        )
        return document
    except Exception as error:
        raise map_error(error) from error


@router.patch("/batches/{batch_id}/status", response_model=Batch)
async def update_batch_status(
    batch_id: int,
    data: BatchStatusUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        warehouse_ids = service.get_batch_warehouse_ids(batch_id)
        for warehouse_id in warehouse_ids:
            require_stock_access(actor_ctx, Permission.STOCK_RECEIVE, warehouse_id)
        batch, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="PATCH",
            path=f"/api/v1/batches/{batch_id}/status",
            payload={"batch_id": batch_id, "status": data.status, "reason": data.reason},
            response_status=status.HTTP_200_OK,
            resource_type="batch",
            operation=lambda: service.update_batch_status(
                batch_id, data.status, data.reason, actor_id
            ),
        )
        if not replayed:
            for warehouse_id in warehouse_ids:
                await publish_event(
                    "batch.status.updated",
                    {"batch_id": batch_id, "warehouse_id": warehouse_id, "status": batch["status"]},
                )
        return batch
    except Exception as error:
        raise map_error(error) from error


@router.get("/quarantine-reviews", response_model=QuarantineReviewPage)
def list_quarantine_reviews(
    warehouse_id: int | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_quarantine_reviews(
                warehouse_id=warehouse_id,
                status=status,
                limit=safe_limit,
                offset=safe_offset,
            ),
            "total": service.count_quarantine_reviews(
                warehouse_id=warehouse_id,
                status=status,
            ),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/quarantine-reviews/{review_id}", response_model=QuarantineReview)
def get_quarantine_review(
    review_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        review = service.get_quarantine_review(review_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, review["warehouse_id"])
        return review
    except Exception as error:
        raise map_error(error) from error


@router.get("/quarantine-reviews/{review_id}/protocol", response_model=QuarantineReviewProtocol)
def get_quarantine_review_protocol(
    review_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        protocol = service.get_quarantine_review_protocol(review_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, protocol["warehouse_id"])
        return protocol
    except Exception as error:
        raise map_error(error) from error


@router.patch("/quarantine-reviews/{review_id}", response_model=QuarantineReview)
async def update_quarantine_review(
    review_id: int,
    data: QuarantineReviewUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        review = service.get_quarantine_review(review_id)
        require_stock_access(actor_ctx, Permission.STOCK_RECEIVE, review["warehouse_id"])
        updated = service.update_quarantine_review(review_id, data, actor_id)
        await publish_event(
            "batch.status.updated",
            {
                "batch_id": updated["batch_id"],
                "warehouse_id": updated["warehouse_id"],
                "quarantine_review_status": updated["status"],
            },
        )
        return updated
    except Exception as error:
        raise map_error(error) from error


@router.post("/write-offs", status_code=status.HTTP_201_CREATED, response_model=StockMovement)
async def write_off(
    data: WriteOffCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_WRITEOFF, data.warehouse_id)
        movement, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/write-offs",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_movement",
            operation=lambda: service.write_off(data, actor_id),
        )
        if not replayed:
            await publish_event(
                "stock.balance.updated",
                {"batch_id": data.batch_id, "warehouse_id": data.warehouse_id},
            )
        return movement
    except Exception as error:
        raise map_error(error) from error


@router.post("/write-offs/fefo", status_code=status.HTTP_201_CREATED, response_model=FefoWriteOffResult)
async def write_off_fefo(
    data: WriteOffFefoCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_WRITEOFF, data.warehouse_id)
        result, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/write-offs/fefo",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="stock_movement",
            operation=lambda: service.write_off_fefo(data, actor_id),
        )
        if not replayed:
            await publish_event(
                "stock.balance.updated",
                {"product_id": data.product_id, "warehouse_id": data.warehouse_id},
            )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.get("/stock-movements", response_model=StockMovementPage)
def list_stock_movements(
    batch_id: int | None = None,
    product_id: int | None = None,
    warehouse_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        items = service.list_stock_movements(
            batch_id=batch_id,
            product_id=product_id,
            warehouse_id=warehouse_id,
            limit=safe_limit,
            offset=safe_offset,
        )
        return {
            "items": items,
            "total": service.count_stock_movements(
                batch_id=batch_id,
                product_id=product_id,
                warehouse_id=warehouse_id,
            ),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/controlled-substances/ledger", response_model=ControlledSubstanceLedgerPage)
def list_controlled_substance_ledger(
    warehouse_id: int | None = None,
    product_id: int | None = None,
    batch_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.AUDIT_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_controlled_substance_ledger(
                warehouse_id=warehouse_id,
                product_id=product_id,
                batch_id=batch_id,
                limit=safe_limit,
                offset=safe_offset,
            ),
            "total": service.count_controlled_substance_ledger(
                warehouse_id=warehouse_id,
                product_id=product_id,
                batch_id=batch_id,
            ),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/controlled-substances/ledger/export", response_model=ControlledSubstanceLedgerExport)
def export_controlled_substance_ledger(
    warehouse_id: int | None = None,
    product_id: int | None = None,
    batch_id: int | None = None,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.AUDIT_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        return service.export_controlled_substance_ledger(
            warehouse_id=warehouse_id,
            product_id=product_id,
            batch_id=batch_id,
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/suppliers/map", response_model=list, tags=["suppliers"])
def suppliers_map(
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> list:
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.list_suppliers_with_geo()
    except Exception as error:
        raise map_error(error) from error


@router.post("/shipments", status_code=201, response_model=Shipment, tags=["logistics"])
def create_shipment_route(
    body: ShipmentCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Shipment:
    try:
        require_permission(actor_ctx, Permission.STOCK_RECEIVE)
        row = service.create_shipment(body.model_dump())
        return _shipment_row(row)
    except Exception as error:
        raise map_error(error) from error


@router.get("/shipments", response_model=ShipmentPage, tags=["logistics"])
def list_shipments_route(
    supplier_id: int | None = None,
    status_filter: str | None = None,
    limit: int = 50,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> ShipmentPage:
    try:
        require_permission_or_supplier(actor_ctx, Permission.STOCK_READ)
        if Role.SUPPLIER in actor_ctx.roles:
            supplier_id = actor_ctx.supplier_id
        result = service.list_shipments(supplier_id=supplier_id, status=status_filter, limit=limit, offset=offset)
        return ShipmentPage(items=[_shipment_row(r) for r in result["items"]], total=result["total"])
    except Exception as error:
        raise map_error(error) from error


@router.patch("/shipments/{shipment_id}", response_model=Shipment, tags=["logistics"])
def update_shipment_route(
    shipment_id: int,
    body: ShipmentUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Shipment:
    try:
        require_permission_or_supplier(actor_ctx, Permission.STOCK_RECEIVE)
        row = service.get_shipment(shipment_id)
        if row is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Shipment not found", "details": {}})
        if Role.SUPPLIER in actor_ctx.roles:
            require_supplier_scope(actor_ctx, row["supplier_id"])
            allowed = {"current_city", "current_lat", "current_lng", "estimated_arrival", "notes", "status"}
            updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if k in allowed}
        else:
            updates = body.model_dump(exclude_unset=True)
        row = service.update_shipment(shipment_id, updates)
        if row is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Shipment not found", "details": {}})
        return _shipment_row(row)
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


def _shipment_row(row: dict) -> Shipment:
    return Shipment(
        id=row["id"],
        supplier_id=row["supplier_id"],
        reference=row.get("reference"),
        status=row["status"],
        origin_city=row.get("origin_city"),
        origin_lat=float(row["origin_lat"]) if row.get("origin_lat") is not None else None,
        origin_lng=float(row["origin_lng"]) if row.get("origin_lng") is not None else None,
        destination_warehouse_id=row.get("destination_warehouse_id"),
        current_city=row.get("current_city"),
        current_lat=float(row["current_lat"]) if row.get("current_lat") is not None else None,
        current_lng=float(row["current_lng"]) if row.get("current_lng") is not None else None,
        estimated_arrival=row.get("estimated_arrival"),
        notes=row.get("notes"),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


@router.get("/controlled-substances/ledger/pdf", tags=["controlled-substances"])
def controlled_ledger_pdf(
    warehouse_id: int | None = None,
    product_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Response:
    """Export ПКУ-журнал as PDF with Cyrillic support, running balance and signature block."""
    try:
        require_permission(actor_ctx, Permission.AUDIT_READ)

        entries = service.list_controlled_substance_ledger(
            warehouse_id=warehouse_id,
            product_id=product_id,
            limit=10000,
            offset=0,
        )

        if date_from or date_to:
            def _in_range(e: dict) -> bool:
                dt_str = str(e.get("created_at", ""))[:10]
                if date_from and dt_str < str(date_from):
                    return False
                if date_to and dt_str > str(date_to):
                    return False
                return True
            entries = [e for e in entries if _in_range(e)]

        warehouses_map = {w["id"]: w["name"] for w in service.list_warehouses(limit=500, offset=0)}

        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import io, os as _os

        FONT_DIR = "/usr/share/fonts/truetype/dejavu"
        FONT_R = "DejaVuSans"
        FONT_B = "DejaVuSans-Bold"
        try:
            pdfmetrics.registerFont(TTFont(FONT_R, _os.path.join(FONT_DIR, "DejaVuSans.ttf")))
            pdfmetrics.registerFont(TTFont(FONT_B, _os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
        except Exception:
            FONT_R = "Helvetica"
            FONT_B = "Helvetica-Bold"

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                                leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                                topMargin=1.5 * cm, bottomMargin=1.5 * cm)

        ts = ParagraphStyle("t", fontName=FONT_B, fontSize=11, spaceAfter=4, leading=14)
        ss = ParagraphStyle("s", fontName=FONT_R, fontSize=8, spaceAfter=8,
                            textColor=colors.HexColor("#374151"))
        fs = ParagraphStyle("f", fontName=FONT_R, fontSize=7,
                            textColor=colors.HexColor("#6b7280"))
        gs = ParagraphStyle("g", fontName=FONT_R, fontSize=8, leading=12)

        today_str = date.today().strftime("%d.%m.%Y")
        period = (
            f"{date_from.strftime('%d.%m.%Y') if date_from else '—'}"
            f" — {date_to.strftime('%d.%m.%Y') if date_to else today_str}"
        )
        wh_label = warehouses_map.get(warehouse_id, f"склад #{warehouse_id}") if warehouse_id else "все склады"

        story = []
        story.append(Paragraph("ЖУРНАЛ ПРЕДМЕТНО-КОЛИЧЕСТВЕННОГО УЧЁТА", ts))
        story.append(Paragraph(
            f"наркотических средств, психотропных веществ и прекурсоров  |  "
            f"Склад: {wh_label}  |  Период: {period}  |  Сформирован: {today_str}",
            ss,
        ))

        headers = [
            "Дата", "Наименование товара", "Партия / серия",
            "Поступ.", "Спис.", "Остаток",
            "Пациент", "Врач", "№ ист. болезни",
            "2-й подтверждающий", "Склад / кабинет",
        ]
        col_widths = [1.9*cm, 5*cm, 2.5*cm, 1.7*cm, 1.7*cm, 1.8*cm,
                      3.2*cm, 3.2*cm, 2.4*cm, 3.2*cm, 2.7*cm]

        # Compute running balance (entries are DESC → reverse for running sum)
        from decimal import Decimal as _D
        asc = list(reversed(entries))
        bal_map: dict[tuple, _D] = {}
        bals: list[_D] = []
        for e in asc:
            key = (e.get("batch_id"), e.get("warehouse_id"))
            cur = bal_map.get(key, _D("0"))
            qty = _D(str(e.get("quantity") or 0))
            mt = e.get("movement_type", "")
            if mt in ("receipt", "batch_receipt", "return_from_department", "department_return"):
                cur += qty
            else:
                cur -= qty
            bal_map[key] = cur
            bals.append(cur)
        bals.reverse()

        table_data = [headers]
        in_types = {"receipt", "batch_receipt", "return_from_department", "department_return"}
        for i, e in enumerate(entries):
            mt = e.get("movement_type", "")
            is_in = mt in in_types
            qty = str(e.get("quantity") or "")
            wn = warehouses_map.get(e.get("warehouse_id"), str(e.get("warehouse_id") or ""))
            table_data.append([
                str(e.get("created_at", ""))[:10],
                str(e.get("product_name") or "")[:50],
                str(e.get("lot") or "")[:20],
                qty if is_in else "",
                qty if not is_in else "",
                str(bals[i]),
                str(e.get("patient_id") or ""),
                str(e.get("doctor_id") or ""),
                str(e.get("medical_record_no") or ""),
                str(e.get("second_approver_id") or ""),
                wn[:30],
            ])

        if not entries:
            table_data.append(["Нет данных за выбранный период"] + [""] * (len(headers) - 1))

        tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), FONT_B),
            ("FONTSIZE", (0, 0), (-1, 0), 7),
            ("FONTNAME", (0, 1), (-1, -1), FONT_R),
            ("FONTSIZE", (0, 1), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (3, 0), (5, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.4 * cm))
        n_in = sum(1 for e in entries if e.get("movement_type") in in_types)
        n_off = sum(1 for e in entries if e.get("movement_type") == "write_off")
        story.append(Paragraph(
            f"Всего записей: {len(entries)} | поступлений: {n_in} | списаний: {n_off}",
            fs,
        ))
        story.append(Spacer(1, 0.6 * cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#9ca3af")))
        story.append(Spacer(1, 0.4 * cm))

        sigs = [
            "Заведующий складом: _______________________________ / _____________ /",
            "Ответственное лицо: _______________________________ / _____________ /",
            f"Дата подписи: {today_str}",
        ]
        sig_tbl = Table([[Paragraph(s, gs) for s in sigs]], colWidths=[9.5*cm, 9.5*cm, 6*cm])
        sig_tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(sig_tbl)

        doc.build(story)
        buf.seek(0)
        fname = f"pku-ledger-{date.today().strftime('%Y%m%d')}.pdf"
        return Response(
            content=buf.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{fname}"'},
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("PKU PDF generation error")
        raise HTTPException(
            status_code=500,
            detail={"code": "internal_error", "message": str(exc), "details": {}},
        ) from exc


@router.post("/transfers", status_code=status.HTTP_201_CREATED, response_model=TransferResult)
async def transfer(
    data: TransferCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_TRANSFER, data.source_warehouse_id)
        require_stock_access(actor_ctx, Permission.STOCK_TRANSFER, data.target_warehouse_id)
        result, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/transfers",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="transfer",
            operation=lambda: service.transfer(data, actor_id),
        )
        if not replayed:
            await publish_event(
                "stock.transfer.posted",
                {
                    "batch_id": data.batch_id,
                    "source_warehouse_id": data.source_warehouse_id,
                    "target_warehouse_id": data.target_warehouse_id,
                },
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": data.batch_id, "warehouse_id": data.source_warehouse_id},
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": data.batch_id, "warehouse_id": data.target_warehouse_id},
            )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/returns/from-department",
    status_code=status.HTTP_201_CREATED,
    response_model=TransferResult,
)
async def return_from_department(
    data: DepartmentReturnCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_TRANSFER, data.source_warehouse_id)
        require_stock_access(actor_ctx, Permission.STOCK_TRANSFER, data.target_warehouse_id)
        result, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/returns/from-department",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="return_from_department",
            operation=lambda: service.return_from_department(data, actor_id),
        )
        if not replayed:
            await publish_event(
                "stock.return.posted",
                {
                    "return_type": "from_department",
                    "batch_id": data.batch_id,
                    "source_warehouse_id": data.source_warehouse_id,
                    "target_warehouse_id": data.target_warehouse_id,
                },
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": data.batch_id, "warehouse_id": data.source_warehouse_id},
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": data.batch_id, "warehouse_id": data.target_warehouse_id},
            )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/returns/to-supplier",
    status_code=status.HTTP_201_CREATED,
    response_model=SupplierReturnResult,
)
async def return_to_supplier(
    data: SupplierReturnCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_TRANSFER, data.warehouse_id)
        result, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/returns/to-supplier",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="return_to_supplier",
            operation=lambda: service.return_to_supplier(data, actor_id),
        )
        if not replayed:
            await publish_event(
                "stock.return.posted",
                {
                    "return_type": "to_supplier",
                    "batch_id": data.batch_id,
                    "warehouse_id": data.warehouse_id,
                    "supplier_id": data.supplier_id,
                },
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": data.batch_id, "warehouse_id": data.warehouse_id},
            )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.post("/reservations", status_code=status.HTTP_201_CREATED, response_model=Reservation)
async def reserve(
    data: ReservationCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_RESERVE, data.warehouse_id)
        reservation, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/reservations",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="reservation",
            operation=lambda: service.reserve(data, actor_id),
        )
        if not replayed:
            await publish_event(
                "reservation.created",
                {"batch_id": data.batch_id, "warehouse_id": data.warehouse_id, "id": reservation["id"]},
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": data.batch_id, "warehouse_id": data.warehouse_id},
            )
        return reservation
    except Exception as error:
        raise map_error(error) from error


@router.get("/reservations", response_model=list[Reservation])
def list_reservations(
    warehouse_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_RESERVE)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_reservations(warehouse_id, safe_limit, safe_offset)
    except Exception as error:
        raise map_error(error) from error


@router.post("/reservations/{reservation_id}/release", response_model=Reservation)
async def release_reservation(
    reservation_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        reservation_for_scope = service.get_reservation(reservation_id)
        require_stock_access(actor_ctx, Permission.STOCK_RESERVE, reservation_for_scope["warehouse_id"])
        reservation, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/reservations/{reservation_id}/release",
            payload={"reservation_id": reservation_id},
            response_status=status.HTTP_200_OK,
            resource_type="reservation",
            operation=lambda: service.release_reservation(reservation_id, actor_id),
        )
        if not replayed:
            await publish_event(
                "reservation.released",
                {
                    "id": reservation["id"],
                    "batch_id": reservation["batch_id"],
                    "warehouse_id": reservation["warehouse_id"],
                },
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": reservation["batch_id"], "warehouse_id": reservation["warehouse_id"]},
            )
        return reservation
    except Exception as error:
        raise map_error(error) from error


@router.post("/reservations/{reservation_id}/use", response_model=Reservation)
async def use_reservation(
    reservation_id: int,
    data: ReservationUseCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        reservation_for_scope = service.get_reservation(reservation_id)
        require_stock_access(
            actor_ctx, Permission.STOCK_WRITEOFF, reservation_for_scope["warehouse_id"]
        )
        reservation, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/reservations/{reservation_id}/use",
            payload={"reservation_id": reservation_id, "data": data},
            response_status=status.HTTP_200_OK,
            resource_type="reservation",
            operation=lambda: service.use_reservation(reservation_id, data, actor_id),
        )
        if not replayed:
            await publish_event(
                "reservation.used",
                {
                    "id": reservation["id"],
                    "batch_id": reservation["batch_id"],
                    "warehouse_id": reservation["warehouse_id"],
                },
            )
            await publish_event(
                "stock.balance.updated",
                {"batch_id": reservation["batch_id"], "warehouse_id": reservation["warehouse_id"]},
            )
        return reservation
    except Exception as error:
        raise map_error(error) from error


@router.post("/reservations/expire", response_model=list[Reservation])
async def expire_reservations(
    warehouse_id: int | None = None,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_RESERVE)
        require_warehouse_filter(actor_ctx, warehouse_id)
        reservations, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/reservations/expire",
            payload={"warehouse_id": warehouse_id},
            response_status=status.HTTP_200_OK,
            resource_type="reservation_expiration",
            operation=lambda: service.expire_reservations(
                actor_id=actor_id, warehouse_id=warehouse_id
            ),
        )
        if not replayed:
            for reservation in reservations:
                await publish_event(
                    "reservation.released",
                    {
                        "id": reservation["id"],
                        "batch_id": reservation["batch_id"],
                        "warehouse_id": reservation["warehouse_id"],
                    },
            )
        return reservations
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/inventory-sessions",
    status_code=status.HTTP_201_CREATED,
    response_model=InventorySessionDetail,
)
def create_inventory_session(
    data: InventoryCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        require_stock_access(actor_ctx, Permission.INVENTORY_MANAGE, data.warehouse_id)
        session, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path="/api/v1/inventory-sessions",
            payload=data,
            response_status=status.HTTP_201_CREATED,
            resource_type="inventory_session",
            operation=lambda: service.create_inventory_session(data, actor_id),
        )
        return session
    except Exception as error:
        raise map_error(error) from error


@router.get("/inventory-sessions", response_model=list[InventorySessionDetail])
def list_inventory_sessions(
    warehouse_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return [
            service.get_inventory_session(session["id"])
            for session in service.list_inventory_sessions(warehouse_id, safe_limit, safe_offset)
        ]
    except Exception as error:
        raise map_error(error) from error


@router.get("/inventory-sessions/{session_id}", response_model=InventorySessionDetail)
def get_inventory_session(
    session_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        session = service.get_inventory_session(session_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, session["warehouse_id"])
        return session
    except Exception as error:
        raise map_error(error) from error


@router.get("/inventory-sessions/{session_id}/print-form", response_model=InventoryPrintForm)
def get_inventory_print_form(
    session_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        form = service.get_inventory_print_form(session_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, form["warehouse_id"])
        return form
    except Exception as error:
        raise map_error(error) from error


@router.patch("/inventory-sessions/{session_id}/lines/{line_id}", response_model=InventoryLine)
def update_inventory_line_count(
    session_id: int,
    line_id: int,
    data: InventoryLineCountUpdate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        session_for_scope = service.get_inventory_session(session_id)
        require_stock_access(actor_ctx, Permission.INVENTORY_MANAGE, session_for_scope["warehouse_id"])
        return service.update_inventory_line_count(session_id, line_id, data, actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/inventory-sessions/{session_id}/post", response_model=InventorySessionDetail)
async def post_inventory_session(
    session_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        session_for_scope = service.get_inventory_session(session_id)
        require_stock_access(actor_ctx, Permission.INVENTORY_MANAGE, session_for_scope["warehouse_id"])
        session, replayed = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/inventory-sessions/{session_id}/post",
            payload={"session_id": session_id},
            response_status=status.HTTP_200_OK,
            resource_type="inventory_session",
            operation=lambda: service.post_inventory_session(session_id, actor_id),
        )
        if not replayed:
            await publish_event(
                "inventory.posted",
                {"id": session["id"], "warehouse_id": session["warehouse_id"]},
            )
            await publish_event(
                "stock.balance.updated",
                {"warehouse_id": session["warehouse_id"], "inventory_session_id": session["id"]},
            )
        return session
    except Exception as error:
        raise map_error(error) from error


@router.post("/inventory-sessions/{session_id}/cancel", response_model=InventorySessionDetail)
def cancel_inventory_session(
    session_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        session_for_scope = service.get_inventory_session(session_id)
        require_stock_access(actor_ctx, Permission.INVENTORY_MANAGE, session_for_scope["warehouse_id"])
        session, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_id,
            method="POST",
            path=f"/api/v1/inventory-sessions/{session_id}/cancel",
            payload={"session_id": session_id},
            response_status=status.HTTP_200_OK,
            resource_type="inventory_session",
            operation=lambda: service.cancel_inventory_session(session_id, actor_id),
        )
        return session
    except Exception as error:
        raise map_error(error) from error


def pagination_meta(limit: int, offset: int) -> tuple[int, int]:
    return max(1, min(limit, 500)), max(0, offset)



@router.get("/balances/pdf", tags=["balances"])
def balances_pdf(
    warehouse_id: int | None = None,
    report_date: str | None = None,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    """Export current stock balances as PDF."""
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        import io
        from datetime import datetime, UTC
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from fastapi.responses import HTMLResponse, Response

        try:
            pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
            font_name = "DejaVu"
        except Exception:
            font_name = "Helvetica"

        balances = service.list_balances(warehouse_id=warehouse_id, limit=5000, offset=0)
        products = {p["id"]: p for p in service.list_products(limit=5000)}
        warehouses = {w["id"]: w for w in service.list_warehouses()}

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
                                leftMargin=1.5*cm, rightMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)

        style_h = ParagraphStyle("h", fontName=font_name, fontSize=13, spaceAfter=6, leading=16)
        style_sub = ParagraphStyle("sub", fontName=font_name, fontSize=9, textColor=colors.gray, spaceAfter=12)
        style_cell = ParagraphStyle("c", fontName=font_name, fontSize=8, leading=10)

        as_of = report_date or datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
        wh_label = warehouses.get(warehouse_id, {}).get("name", "Все склады") if warehouse_id else "Все склады"

        elements = [
            Paragraph("Остатки товаров на складе", style_h),
            Paragraph(f"Склад: {wh_label}   ·   По состоянию на: {as_of}", style_sub),
        ]

        headers = ["Товар", "SKU", "Серия", "Склад", "Свободно", "В резерве", "Годен до", "Статус"]
        data = [headers]
        for row in balances:
            prod = products.get(row.get("product_id") if isinstance(row, dict) else row.product_id, {})
            wh = warehouses.get(row.get("warehouse_id") if isinstance(row, dict) else row.warehouse_id, {})
            def rv(key, _row=row):
                return _row.get(key, "") if isinstance(_row, dict) else getattr(_row, key, "")
            data.append([
                Paragraph(str(prod.get("name", u"—"))[:40], style_cell),
                str(prod.get("sku", u"—") or u"—")[:12],
                str(rv("batch_id")),
                str(wh.get("name", u"—") or u"—")[:20],
                str(rv("free_quantity") or 0),
                str(rv("reserved_quantity") or 0),
                str(rv("expires_on") or u"—"),
                str(rv("batch_status") or u"—"),
            ])

        col_widths = [6*cm, 2*cm, 2*cm, 4*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]
        tbl = Table(data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), font_name),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#25636f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), font_name),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5fbf8")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c8ded6")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.extend([tbl, Spacer(1, 0.5*cm)])
        elements.append(Paragraph(f"Итого позиций: {len(balances)}", style_sub))
        doc.build(elements)
        buf.seek(0)
        return Response(
            content=buf.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="balances_{as_of[:10]}.pdf"'},
        )
    except Exception as error:
        raise map_error(error) from error

@router.get("/balances", response_model=BalancePage)
def list_balances(
    product_id: int | None = None,
    warehouse_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_balances(product_id, warehouse_id, safe_limit, safe_offset),
            "total": service.count_balances(product_id, warehouse_id),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/analytics/abc-xyz", response_model=AbcXyzAnalysis)
def abc_xyz_analysis(
    warehouse_id: int | None = None,
    days: int = 90,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        return service.abc_xyz_analysis(analysis_days=days, warehouse_id=warehouse_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/analytics/abc-xyz/apply-suggestions")
def apply_xyz_reorder_suggestions(
    analysis_days: int = 90,
    warehouse_id: int | None = None,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    """Apply XYZ-based reorder point suggestions to products."""
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        if warehouse_id is not None:
            require_warehouse_filter(actor_ctx, warehouse_id)
        return service.apply_xyz_reorder_suggestions(
            analysis_days=analysis_days, warehouse_id=warehouse_id, actor_id=actor_id
        )
    except Exception as e:
        raise map_error(e) from e


@router.post("/analytics/abc-xyz/runs", response_model=AbcXyzRunDetail)
def create_abc_xyz_run(
    warehouse_id: int | None = None,
    days: int = 90,
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.DOCUMENT_CREATE)
        require_warehouse_filter(actor_ctx, warehouse_id)
        return service.save_abc_xyz_analysis_snapshot(
            analysis_days=days,
            warehouse_id=warehouse_id,
            actor_id=actor_id,
            source="manual",
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/analytics/abc-xyz/history", response_model=AbcXyzRunPage)
def list_abc_xyz_runs(
    warehouse_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_abc_xyz_runs(
                warehouse_id=warehouse_id,
                limit=safe_limit,
                offset=safe_offset,
            ),
            "total": service.count_abc_xyz_runs(warehouse_id=warehouse_id),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/analytics/abc-xyz/history/{run_id}", response_model=AbcXyzRunDetail)
def get_abc_xyz_run(
    run_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        run = service.get_abc_xyz_run(run_id)
        require_warehouse_filter(actor_ctx, run["warehouse_id"])
        return run
    except Exception as error:
        raise map_error(error) from error


@router.post("/purchase-requests/generate", response_model=list[PurchaseRequest])
def generate_purchase_requests(
    warehouse_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, warehouse_id)
        return service.generate_purchase_requests(warehouse_id=warehouse_id, actor_id=actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/purchase-requests/generate-auto", response_model=list[PurchaseRequest])
def generate_purchase_requests_auto(
    warehouse_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    service: WarehouseService = Depends(get_warehouse_service),
):
    return generate_purchase_requests(
        warehouse_id=warehouse_id,
        actor_ctx=actor_ctx,
        actor_id=actor_id,
        service=service,
    )


@router.post("/purchase-requests", status_code=status.HTTP_201_CREATED, response_model=PurchaseRequest)
def create_purchase_request(
    payload: PurchaseRequestCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, payload.warehouse_id)
        return service.create_purchase_request(payload, actor_id=actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/purchase-requests", response_model=list[PurchaseRequest])
def list_purchase_requests(
    warehouse_id: int | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return service.list_purchase_requests(
            warehouse_id=warehouse_id,
            status=status,
            limit=safe_limit,
            offset=safe_offset,
        )
    except Exception as error:
        raise map_error(error) from error


@router.patch("/purchase-requests/{request_id}", response_model=PurchaseRequest)
def update_purchase_request_status(
    request_id: int,
    payload: PurchaseRequestStatusUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        current = service.get_purchase_request(request_id)
        require_stock_access(actor_ctx, Permission.DOCUMENT_CREATE, current["warehouse_id"])
        return service.update_purchase_request_status(request_id, payload, actor_id=actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/notifications/generate-low-stock", response_model=list[Notification])
def generate_low_stock_notifications(
    warehouse_id: int | None = None,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.NOTIFICATIONS_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        return service.generate_low_stock_notifications(warehouse_id=warehouse_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/notifications/generate-expiry", response_model=list[Notification])
def generate_expiry_notifications(
    warehouse_id: int | None = None,
    days: int = 30,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.NOTIFICATIONS_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        return service.generate_expiry_notifications(days=days, warehouse_id=warehouse_id)
    except Exception as error:
        raise map_error(error) from error


# === CONTROLLED SUBSTANCE LIMITS ===

@router.get("/controlled-substances/limits", tags=["controlled-substances"])
def list_controlled_limits(
    warehouse_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_READ, warehouse_id)
        return service.list_controlled_limits(warehouse_id)
    except Exception as e:
        raise map_error(e) from e


class ControlledLimitBody(BaseModel):
    warehouse_id: int
    product_id: int
    max_quantity: float
    unit: str | None = None


@router.put("/controlled-substances/limits", tags=["controlled-substances"])
def upsert_controlled_limit(
    body: ControlledLimitBody,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_stock_access(actor_ctx, Permission.CATALOG_WRITE, body.warehouse_id)
        return service.upsert_controlled_limit(
            body.warehouse_id, body.product_id, body.max_quantity, body.unit
        )
    except Exception as e:
        raise map_error(e) from e


@router.delete("/controlled-substances/limits/{limit_id}", status_code=204, tags=["controlled-substances"])
def delete_controlled_limit(
    limit_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        service.delete_controlled_limit(limit_id)
    except Exception as e:
        raise map_error(e) from e


@router.get("/controlled-substances/limits/violations", tags=["controlled-substances"])
def check_controlled_limit_violations(
    warehouse_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_READ, warehouse_id)
        return service.check_controlled_limit_violations(warehouse_id)
    except Exception as e:
        raise map_error(e) from e


@router.post("/notifications/generate-controlled-inventory", response_model=list[Notification])
def generate_controlled_inventory_notifications(
    warehouse_id: int | None = None,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.NOTIFICATIONS_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        return service.generate_controlled_inventory_reminder(warehouse_id=warehouse_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/notifications/generate-quarantine", response_model=list[Notification])
def generate_quarantine_notifications(
    warehouse_id: int | None = None,
    days: int = 3,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.NOTIFICATIONS_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        return service.generate_quarantine_notifications(days=days, warehouse_id=warehouse_id)
    except Exception as error:
        raise map_error(error) from error



@router.post("/notifications/generate-supplier-contracts", response_model=list[Notification])
def generate_supplier_contract_expiry_notifications(
    days: int = 30,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.NOTIFICATIONS_READ)
        return service.generate_supplier_contract_expiry_notifications(days=days)
    except Exception as error:
        raise map_error(error) from error

@router.get("/notifications", response_model=NotificationPage)
def list_notifications(
    unread_only: bool = False,
    warehouse_id: int | None = None,
    limit: int = 100,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.NOTIFICATIONS_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_notifications(
                unread_only, safe_limit, safe_offset, warehouse_id=warehouse_id
            ),
            "total": service.count_notifications(unread_only, warehouse_id=warehouse_id),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.get("/audit-log", response_model=AuditLogPage)
def list_audit_log(
    entity_type: str | None = None,
    warehouse_id: int | None = None,
    actor_id: str | None = None,
    action: str | None = None,
    limit: int = 100,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.AUDIT_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return {
            "items": service.list_audit_log(
                entity_type,
                safe_limit,
                safe_offset,
                warehouse_id=warehouse_id,
                actor_id=actor_id,
                action=action,
            ),
            "total": service.count_audit_log(
                entity_type,
                warehouse_id=warehouse_id,
                actor_id=actor_id,
                action=action,
            ),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.patch("/notifications/{notification_id}/read", response_model=Notification)
def mark_notification_read(
    notification_id: int,
    data: NotificationReadUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.NOTIFICATIONS_READ)
        notification = service.get_notification(notification_id)
        require_warehouse_filter(actor_ctx, notification["warehouse_id"])
        return service.mark_notification_read(notification_id, data.is_read)
    except Exception as error:
        raise map_error(error) from error




# ── Summary stats (for Grafana, monitoring, etc.) ────────────────────────────

@router.get("/stats/summary")
def get_stats_summary(
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.get_stats_summary()
    except Exception as error:
        raise map_error(error) from error


# ── Grafana Alertmanager webhook ──────────────────────────────────────────────

class GrafanaAlertAnnotations(BaseModel):
    summary: str = ""
    description: str = ""

class GrafanaAlert(BaseModel):
    status: str = "firing"
    labels: dict = {}
    annotations: GrafanaAlertAnnotations = GrafanaAlertAnnotations()
    fingerprint: str = ""

class GrafanaWebhookPayload(BaseModel):
    version: str = "1"
    status: str = "firing"
    alerts: list[GrafanaAlert] = []
    commonLabels: dict = {}
    commonAnnotations: dict = {}
    externalURL: str = ""
    groupKey: str = ""


@router.post("/webhooks/grafana", status_code=status.HTTP_204_NO_CONTENT)
def grafana_webhook(
    payload: GrafanaWebhookPayload,
    authorization: str | None = Header(default=None, alias="Authorization"),
    service: WarehouseService = Depends(get_warehouse_service),
):
    settings = get_settings()
    if settings.grafana_webhook_token:
        expected = f"Bearer {settings.grafana_webhook_token}"
        if authorization != expected:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "unauthorized", "message": "Invalid or missing webhook token"},
            )
    for alert in payload.alerts:
        alertname = alert.labels.get("alertname") or "Grafana Alert"
        severity = alert.labels.get("severity") or payload.commonLabels.get("severity") or "warning"
        summary = alert.annotations.summary or alert.annotations.description or alertname
        description = alert.annotations.description or ""
        if description and description != summary:
            message = f"{summary}\n{description}"
        else:
            message = summary
        title = f"[{severity.upper()}] {alertname} — {alert.status}"
        service.create_grafana_alert_notification(title=title, message=message, severity=severity)


@router.websocket("/ws/balances")
async def balances_ws(
    websocket: WebSocket, warehouse_id: int | None = None, access_token: str | None = None
):
    try:
        settings = get_settings()
        if not settings.dev_auth_enabled:
            token = access_token
            authorization = websocket.headers.get("authorization")
            if authorization:
                scheme, _, raw_token = authorization.partition(" ")
                if scheme.lower() != "bearer" or not raw_token.strip():
                    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                token = raw_token.strip()
            if not token or not settings.jwt_hmac_secret:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
            actor_ctx = actor_from_bearer_token(
                token,
                secret=settings.jwt_hmac_secret,
                issuer=settings.jwt_issuer,
                audience=settings.jwt_audience,
                leeway_seconds=settings.jwt_clock_skew_seconds,
            )
        else:
            actor_ctx = actor_from_headers(
                actor_id=websocket.headers.get("x-actor-id", "system"),
                roles_header=websocket.headers.get("x-actor-roles"),
                warehouse_ids_header=websocket.headers.get("x-actor-warehouse-ids"),
                department=websocket.headers.get("x-actor-department"),
                allow_dev_default=settings.dev_auth_enabled,
            )
        require_permission(actor_ctx, Permission.STOCK_READ)
        require_warehouse_filter(actor_ctx, warehouse_id)
    except (AuthenticationError, PermissionDeniedError, ValidationError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    warehouse_scope = None
    if Role.WAREHOUSE_MANAGER not in actor_ctx.roles:
        warehouse_scope = frozenset({warehouse_id}) if warehouse_id is not None else actor_ctx.warehouse_ids

    await manager.connect(websocket, warehouse_scope=warehouse_scope)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# === AI ASSISTANT ===

from app.domain.schemas import (  # noqa: F811
    AiRiskAnalysisRequest, AiRiskAnalysisResult,
    AiSinglePurchaseAnalysis, AiSinglePurchaseResult,
    AuctionCreate, AuctionOut, AuctionBid, AuctionBidCreate, AuctionPage,
)
from app.services.ai_assistant import analyze_purchase_risk, analyze_single_purchase


@router.post("/ai/analyze-purchases", response_model=AiRiskAnalysisResult, tags=["ai"])
def ai_analyze_purchases(
    body: AiRiskAnalysisRequest,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_RECEIVE)
        settings = get_settings()
        if not settings.anthropic_api_key:
            raise HTTPException(status_code=503, detail={"code": "service_unavailable",
                "message": "AI не настроен (SKLAD_ANTHROPIC_API_KEY не задан)", "details": {}})
        requests = service.list_purchase_requests(status="pending",
            warehouse_id=body.warehouse_id, limit=20, offset=0)
        if body.purchase_request_ids:
            requests = [r for r in requests if r["id"] in body.purchase_request_ids]
        price_history: list = []
        for req in requests[:5]:
            ph = service.list_supplier_price_history(product_id=req["product_id"], limit=3, offset=0)
            price_history.extend(ph.get("items", []))
        abc_data = service.abc_xyz_analysis(warehouse_id=body.warehouse_id)
        result = analyze_purchase_risk(
            purchase_requests=requests, price_history=price_history,
            abc_xyz_data=abc_data.get("items", []),
            anthropic_api_key=settings.anthropic_api_key,
        )
        return AiRiskAnalysisResult(**result)
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.post("/ai/analyze-single-purchase", response_model=AiSinglePurchaseResult, tags=["ai"])
def ai_analyze_single_purchase(
    body: AiSinglePurchaseAnalysis,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_RECEIVE)
        settings = get_settings()
        if not settings.anthropic_api_key:
            raise HTTPException(status_code=503, detail={"code": "service_unavailable",
                "message": "AI не настроен", "details": {}})
        product = service.get_product(body.product_id)
        if not product:
            from app.domain.errors import NotFoundError as _NFE
            raise _NFE("Product not found")
        ph = service.list_supplier_price_history(product_id=body.product_id, limit=5, offset=0)
        supplier_name = None
        if body.supplier_id:
            sup = service.get_supplier(body.supplier_id)
            if sup:
                supplier_name = sup["name"]
        balances = service.list_balances(product_id=body.product_id,
            warehouse_id=body.warehouse_id, limit=100, offset=0)
        current_stock = sum(float(b.get("free_quantity", 0)) for b in balances.get("items", []))
        abc_items = service.abc_xyz_analysis(warehouse_id=body.warehouse_id)
        abc_item = next((i for i in abc_items.get("items", []) if i.get("product_id") == body.product_id), None)
        result = analyze_single_purchase(
            product_name=product["name"], quantity=float(body.quantity),
            unit_price=body.unit_price, supplier_name=supplier_name,
            price_history=ph.get("items", []), current_stock=current_stock,
            reorder_point=float(product.get("reorder_point", 0)),
            abc_class=abc_item.get("abc_class") if abc_item else None,
            xyz_class=abc_item.get("xyz_class") if abc_item else None,
            anthropic_api_key=settings.anthropic_api_key,
        )
        return AiSinglePurchaseResult(**result)
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


# === AUCTIONS ===

def _auction_row(row: dict) -> AuctionOut:
    return AuctionOut(
        id=row["id"], title=row["title"], description=row.get("description"),
        product_id=row["product_id"], product_name=row.get("product_name"),
        warehouse_id=row["warehouse_id"], quantity=row["quantity"], unit=row.get("unit", "шт"),
        start_price=row["start_price"], current_price=row["current_price"],
        min_price=row["min_price"], step_amount=row["step_amount"],
        step_interval_seconds=row["step_interval_seconds"], status=row["status"],
        winner_supplier_id=row.get("winner_supplier_id"), winner_bid=row.get("winner_bid"),
        starts_at=str(row["starts_at"]) if row.get("starts_at") else None,
        ends_at=str(row["ends_at"]) if row.get("ends_at") else None,
        next_step_at=str(row["next_step_at"]) if row.get("next_step_at") else None,
        created_by=row["created_by"], created_at=str(row["created_at"]),
        bid_count=int(row.get("bid_count", 0)),
    )



# ─── Repack Templates ───────────────────────────────────────────────────────

class RepackTemplateOut(BaseModel):
    id: int
    name: str
    source_product_id: int | None = None
    source_product_name: str | None = None
    target_product_id: int
    target_product_name: str | None = None
    quantity_factor: str
    loss_factor: str
    target_unit_price: str | None = None
    reason: str | None = None
    created_by: str
    created_at: str


class RepackTemplateCreate(BaseModel):
    name: str
    source_product_id: int | None = None
    target_product_id: int
    quantity_factor: float = 1.0
    loss_factor: float = 0.0
    target_unit_price: float | None = None
    reason: str | None = None


@router.get("/repack-templates", response_model=list[RepackTemplateOut], tags=["repacking"])
def list_repack_templates(
    source_product_id: int | None = None,
    db=Depends(get_database),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    require_permission(actor_ctx, Permission.STOCK_READ)
    service = WarehouseService(db)
    return service.list_repack_templates(source_product_id=source_product_id)


@router.post("/repack-templates", status_code=201, response_model=RepackTemplateOut, tags=["repacking"])
def create_repack_template(
    body: RepackTemplateCreate,
    db=Depends(get_database),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    require_permission(actor_ctx, Permission.STOCK_WRITEOFF)
    service = WarehouseService(db)
    try:
        return service.create_repack_template(body.model_dump(), actor_id=actor_ctx.actor_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/repack-templates/{template_id}", status_code=204, tags=["repacking"])
def delete_repack_template(
    template_id: int,
    db=Depends(get_database),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    require_permission(actor_ctx, Permission.STOCK_WRITEOFF)
    service = WarehouseService(db)
    try:
        service.delete_repack_template(template_id, actor_id=actor_ctx.actor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/auctions", status_code=201, response_model=AuctionOut, tags=["auctions"])
def create_auction(
    body: AuctionCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        row = service.create_auction(body.model_dump(), actor_id=actor_ctx.actor_id)
        return _auction_row(row)
    except Exception as e:
        raise map_error(e) from e


@router.get("/auctions", response_model=AuctionPage, tags=["auctions"])
def list_auctions(
    status: str | None = None, limit: int = 20, offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission_or_supplier(actor_ctx, Permission.STOCK_READ)
        result = service.list_auctions(status=status, limit=limit, offset=offset)
        return AuctionPage(items=[_auction_row(r) for r in result["items"]], total=result["total"])
    except Exception as e:
        raise map_error(e) from e


@router.get("/auctions/{auction_id}", response_model=AuctionOut, tags=["auctions"])
def get_auction(
    auction_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        row = service.get_auction(auction_id)
        if not row:
            from app.domain.errors import NotFoundError as _NFE
            raise _NFE("Auction not found")
        return _auction_row(row)
    except Exception as e:
        raise map_error(e) from e


@router.post("/auctions/{auction_id}/start", response_model=AuctionOut, tags=["auctions"])
async def start_auction(
    auction_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        row = service.start_auction(auction_id)
        if not row:
            from app.domain.errors import NotFoundError as _NFE
            raise _NFE("Auction not found or not in draft")
        out = _auction_row(row)
        await publish_event("auction_started", {"auction_id": auction_id, "status": "active"})
        return out
    except Exception as e:
        raise map_error(e) from e


@router.post("/auctions/{auction_id}/close", response_model=AuctionOut, tags=["auctions"])
async def close_auction(
    auction_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        row = service.close_auction(auction_id)
        if not row:
            from app.domain.errors import NotFoundError as _NFE
            raise _NFE("Auction not found or not active")
        out = _auction_row(row)
        winner = row.get("winner_supplier_id")
        await publish_event("auction_closed", {"auction_id": auction_id, "status": "closed", "winner_supplier_id": winner, "final_price": float(row.get("current_price") or 0)})
        return out
    except Exception as e:
        raise map_error(e) from e


@router.post("/auctions/{auction_id}/bids", status_code=201, response_model=AuctionBid, tags=["auctions"])
async def place_bid(
    auction_id: int, body: AuctionBidCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission_or_supplier(actor_ctx, Permission.STOCK_RECEIVE)
        require_supplier_scope(actor_ctx, body.supplier_id)
        row = service.place_bid(auction_id, body.supplier_id, float(body.bid_amount))
        bid = AuctionBid(id=row["id"], auction_id=row["auction_id"], supplier_id=row["supplier_id"],
                          bid_amount=row["bid_amount"], created_at=str(row["created_at"]))
        await publish_event("auction_bid", {
            "auction_id": auction_id,
            "supplier_id": body.supplier_id,
            "bid_amount": float(body.bid_amount),
        })
        return bid
    except Exception as e:
        raise map_error(e) from e


@router.get("/auctions/{auction_id}/bids", response_model=list[AuctionBid], tags=["auctions"])
def list_auction_bids(
    auction_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission_or_supplier(actor_ctx, Permission.STOCK_READ)
        rows = service.list_auction_bids(auction_id)
        if Role.SUPPLIER in actor_ctx.roles:
            rows = [r for r in rows if r["supplier_id"] == actor_ctx.supplier_id]
        return [AuctionBid(id=r["id"], auction_id=r["auction_id"], supplier_id=r["supplier_id"],
                           supplier_name=r.get("supplier_name"), bid_amount=r["bid_amount"],
                           created_at=str(r["created_at"])) for r in rows]
    except Exception as e:
        raise map_error(e) from e


# === BARCODE / LABEL REPRINT ===

@router.post("/products/{product_id}/mark-reprinted", tags=["labels"])
def mark_product_reprinted(
    product_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        service.mark_product_reprinted(product_id)
        return {"ok": True}
    except Exception as e:
        raise map_error(e) from e


# === SUPPLIER REVIEWS ===

from app.domain.schemas import SupplierReviewCreate, SupplierReview, SupplierReviewModerate  # noqa: E402, F811


@router.post("/suppliers/{supplier_id}/reviews", status_code=201,
             response_model=SupplierReview, tags=["suppliers"])
def create_supplier_review(
    supplier_id: int,
    body: SupplierReviewCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        row = service.create_supplier_review(
            supplier_id=supplier_id,
            rating=body.rating,
            comment=body.comment,
            reviewer_id=actor_ctx.actor_id,
        )
        return SupplierReview(**{k: str(v) if k == "created_at" else v for k, v in row.items()})
    except Exception as e:
        raise map_error(e) from e


@router.get("/suppliers/{supplier_id}/reviews",
            response_model=list[SupplierReview], tags=["suppliers"])
def list_supplier_reviews(
    supplier_id: int,
    status: str | None = None,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission_or_supplier(actor_ctx, Permission.STOCK_READ)
        require_supplier_scope(actor_ctx, supplier_id)
        rows = service.list_supplier_reviews(supplier_id=supplier_id, status=status)
        return [SupplierReview(**{k: str(v) if k == "created_at" else v for k, v in r.items()}) for r in rows]
    except Exception as e:
        raise map_error(e) from e


@router.patch("/supplier-reviews/{review_id}",
              response_model=SupplierReview, tags=["suppliers"])
def moderate_supplier_review(
    review_id: int,
    body: SupplierReviewModerate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        row = service.moderate_supplier_review(review_id=review_id, action=body.action)
        return SupplierReview(**{k: str(v) if k == "created_at" else v for k, v in row.items()})
    except Exception as e:
        raise map_error(e) from e


@router.get("/supplier-reviews", response_model=list[SupplierReview], tags=["suppliers"])
def list_all_supplier_reviews(
    status: str | None = None,
    actor_ctx: ActorContext = Depends(get_actor_context),
    service: WarehouseService = Depends(get_warehouse_service),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        rows = service.list_all_supplier_reviews(status=status)
        return [SupplierReview(**{k: str(v) if k == "created_at" else v for k, v in r.items()}) for r in rows]
    except Exception as e:
        raise map_error(e) from e


# === INVENTORY SESSION PDF ===

@router.get("/inventory-sessions/{session_id}/pdf", tags=["inventory"])
def inventory_session_pdf(
    session_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Response:
    """Export inventory session as printable PDF sheet."""
    try:
        form = service.get_inventory_print_form(session_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, form["warehouse_id"])

        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        import io

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=1.5*cm, rightMargin=1.5*cm,
                                topMargin=2*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("inv_title", parent=styles["Normal"],
                                     fontSize=13, fontName="Helvetica-Bold", spaceAfter=4)
        sub_style = ParagraphStyle("inv_sub", parent=styles["Normal"],
                                   fontSize=9, fontName="Helvetica", spaceAfter=10)
        story = []
        story.append(Paragraph("ИНВЕНТАРИЗАЦИОННАЯ ВЕДОМОСТЬ", title_style))
        wh = form.get("warehouse_name") or f"Склад #{form.get('warehouse_id', '')}"
        created = str(form.get("created_at", ""))[:10]
        story.append(Paragraph(
            f"Склад: {wh} | Сессия #{session_id} | Начата: {created} | "
            f"Статус: {form.get('status', '')} | Категория: {form.get('category_name') or 'Все'}",
            sub_style
        ))

        headers = ["№", "Товар", "SKU", "Ед.", "Учётный остаток", "Факт", "Излишек/Недостача", "Примечание"]
        col_widths = [1*cm, 6.5*cm, 2.8*cm, 1.5*cm, 2.5*cm, 2.5*cm, 3*cm, 2.5*cm]

        lines = form.get("lines") or []
        table_data = [headers]
        for i, line in enumerate(lines, 1):
            book = float(line.get("book_quantity") or 0)
            fact = line.get("actual_quantity")
            if fact is not None:
                fact_val = float(fact)
                diff = fact_val - book
                diff_str = (f"+{diff:.3f}" if diff > 0 else f"{diff:.3f}") if diff != 0 else "0"
            else:
                fact_val = ""
                diff_str = ""
            table_data.append([
                str(i),
                str(line.get("product_name") or "")[:50],
                str(line.get("sku") or "")[:20],
                str(line.get("unit") or ""),
                f"{book:.3f}",
                str(fact_val) if fact_val != "" else "___________",
                diff_str or "___________",
                "",
            ])

        tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 7.5),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 7.5),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (4, 0), (6, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 1 * cm))
        story.append(Paragraph(
            f"Товарных позиций: {len(lines)}. "
            "Зав. складом: ___________________ Дата: ___________",
            sub_style
        ))
        story.append(Paragraph(
            "Комиссия: ___________________ ___________________ ___________________",
            sub_style
        ))
        doc.build(story)
        buf.seek(0)
        filename = f"inventory-{session_id}-{date.today()}.pdf"
        return Response(
            content=buf.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"code": "internal_error", "message": str(exc), "details": {}}) from exc


# === PURCHASE REQUESTS PDF ===

@router.get("/purchase-requests/pdf", tags=["purchase-requests"])
def purchase_requests_pdf(
    warehouse_id: int | None = None,
    status: str | None = None,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Response:
    """Export purchase requests as PDF."""
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        requests_list = service.list_purchase_requests(
            warehouse_id=warehouse_id, status=status or "draft", limit=500, offset=0
        )

        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        import io

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=1.5*cm, rightMargin=1.5*cm,
                                topMargin=2*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("pr_title", parent=styles["Normal"],
                                     fontSize=13, fontName="Helvetica-Bold", spaceAfter=4)
        sub_style = ParagraphStyle("pr_sub", parent=styles["Normal"],
                                   fontSize=9, fontName="Helvetica", spaceAfter=10)
        story = []
        story.append(Paragraph("ЗАЯВКИ НА ЗАКУПКУ", title_style))
        story.append(Paragraph(
            f"Дата: {date.today().strftime('%d.%m.%Y')} | Статус: {status or 'draft'} | "
            f"Склад: {'Склад #' + str(warehouse_id) if warehouse_id else 'Все'}",
            sub_style
        ))

        headers = ["№", "Товар", "SKU", "Склад", "Кол-во", "Статус", "Причина", "Дата"]
        col_widths = [1*cm, 5.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm, 3.5*cm, 2*cm]

        table_data = [headers]
        for i, req in enumerate(requests_list, 1):
            table_data.append([
                str(i),
                str(req.get("product_name") or req.get("product_id", ""))[:40],
                str(req.get("sku") or "")[:20],
                str(req.get("warehouse_id") or ""),
                str(req.get("recommended_quantity") or req.get("quantity") or ""),
                str(req.get("status") or ""),
                str(req.get("reason") or "")[:35],
                str(req.get("created_at", ""))[:10],
            ])

        tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 7.5),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 7.5),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph(
            f"Всего заявок: {len(requests_list)}. Зав. складом: ___________________ Дата: ___________",
            sub_style
        ))
        doc.build(story)
        buf.seek(0)
        filename = f"purchase-requests-{date.today()}.pdf"
        return Response(
            content=buf.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"code": "internal_error", "message": str(exc), "details": {}}) from exc


# === CERTIFICATE FILE UPLOAD ===

@router.post(
    "/products/{product_id}/certificate/upload",
    tags=["catalog"],
    summary="Upload certificate file for a product",
)
async def upload_product_certificate(
    product_id: int,
    file: UploadFile,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    """Upload a certificate file (PDF, JPG, PNG) and link it to the product."""
    import uuid, aiofiles
    from pathlib import Path

    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)

        MAX_SIZE = 10 * 1024 * 1024  # 10 MB
        ALLOWED = {".pdf", ".jpg", ".jpeg", ".png", ".webp"}

        ext = Path(file.filename or "").suffix.lower()
        if ext not in ALLOWED:
            raise HTTPException(
                status_code=422,
                detail={"code": "invalid_file_type", "message": f"Разрешены: PDF, JPG, PNG. Получен: {ext}", "details": {}},
            )

        content = await file.read()
        if len(content) > MAX_SIZE:
            raise HTTPException(
                status_code=422,
                detail={"code": "file_too_large", "message": "Файл больше 10 МБ", "details": {}},
            )

        uploads_dir = Path(__file__).resolve().parents[2] / "uploads" / "certificates"
        uploads_dir.mkdir(parents=True, exist_ok=True)

        safe_name = f"{product_id}_{uuid.uuid4().hex[:8]}{ext}"
        dest = uploads_dir / safe_name

        async with aiofiles.open(dest, "wb") as f_out:
            await f_out.write(content)

        # Build the public URL served by nginx -> /sklad/uploads/certificates/<file>
        cert_url = f"/uploads/certificates/{safe_name}"

        updated = service.update_product_certificate_ref(product_id, cert_url, actor_id)
        return {"product_id": product_id, "certificate_url": cert_url, "product": updated}

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"code": "internal_error", "message": str(exc), "details": {}},
        ) from exc


@router.post(
    "/products/{product_id}/image/upload",
    tags=["catalog"],
    summary="Upload product photo",
)
async def upload_product_image(
    product_id: int,
    file: UploadFile,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    """Upload a product photo (JPG, PNG, WEBP) and link it to the product."""
    import uuid, aiofiles
    from pathlib import Path

    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)

        MAX_SIZE = 8 * 1024 * 1024  # 8 MB
        ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}

        ext = Path(file.filename or "").suffix.lower()
        if ext not in ALLOWED:
            raise HTTPException(
                status_code=422,
                detail={"code": "invalid_file_type", "message": f"Разрешены: JPG, PNG, WEBP. Получен: {ext}", "details": {}},
            )

        content = await file.read()
        if len(content) > MAX_SIZE:
            raise HTTPException(
                status_code=422,
                detail={"code": "file_too_large", "message": "Файл больше 8 МБ", "details": {}},
            )

        uploads_dir = Path(__file__).resolve().parents[2] / "uploads" / "products"
        uploads_dir.mkdir(parents=True, exist_ok=True)

        safe_name = f"{product_id}_{uuid.uuid4().hex[:8]}{ext}"
        dest = uploads_dir / safe_name

        async with aiofiles.open(dest, "wb") as f_out:
            await f_out.write(content)

        image_url = f"/uploads/products/{safe_name}"

        updated = service.update_product_image_ref(product_id, image_url, actor_id)
        return {"product_id": product_id, "image_url": image_url, "product": updated}

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"code": "internal_error", "message": str(exc), "details": {}},
        ) from exc


@router.delete(
    "/products/{product_id}/image",
    tags=["catalog"],
    summary="Remove product photo",
)
async def delete_product_image(
    product_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    """Unlink the product photo."""
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        updated = service.update_product_image_ref(product_id, None, actor_id)
        return {"product_id": product_id, "image_url": None, "product": updated}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"code": "internal_error", "message": str(exc), "details": {}},
        ) from exc


@router.delete(
    "/products/{product_id}/certificate",
    tags=["catalog"],
    summary="Remove certificate file from a product",
)
async def delete_product_certificate(
    product_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    """Unlink (and optionally delete) the certificate file."""
    import aiofiles.os
    from pathlib import Path

    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)

        # Clear the certificate reference in the database
        updated = service.update_product_certificate_ref(product_id, None, actor_id)
        return {"product_id": product_id, "certificate_url": None, "product": updated}

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"code": "internal_error", "message": str(exc), "details": {}},
        ) from exc


# === INVENTORY COMPARISON (СЛИЧИТЕЛЬНАЯ ВЕДОМОСТЬ) PDF ===

@router.get("/inventory-sessions/{session_id}/comparison-pdf", tags=["inventory"])
def inventory_comparison_pdf(
    session_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Response:
    """
    Generate сличительная ведомость (comparison sheet) PDF.
    Only lines with actual_quantity != book_quantity are included.
    """
    try:
        form = service.get_inventory_print_form(session_id)
        require_stock_access(actor_ctx, Permission.STOCK_READ, form["warehouse_id"])

        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        import io

        lines = form.get("lines") or []
        # Only discrepant lines
        discrepant = [
            line for line in lines
            if line.get("actual_quantity") is not None
            and float(line["actual_quantity"]) != float(line.get("book_quantity") or 0)
        ]

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=1.5*cm, rightMargin=1.5*cm,
                                topMargin=2*cm, bottomMargin=1.5*cm)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("cmp_title", parent=styles["Normal"],
                                     fontSize=13, fontName="Helvetica-Bold", spaceAfter=4)
        sub_style = ParagraphStyle("cmp_sub", parent=styles["Normal"],
                                   fontSize=9, fontName="Helvetica", spaceAfter=10)
        sign_style = ParagraphStyle("cmp_sign", parent=styles["Normal"],
                                    fontSize=9, fontName="Helvetica", spaceAfter=6)
        story = []

        # Title
        story.append(Paragraph("СЛИЧИТЕЛЬНАЯ ВЕДОМОСТЬ", title_style))
        wh = form.get("warehouse_name") or f"Склад #{form.get('warehouse_id', '')}"
        created = str(form.get("created_at", ""))[:10]
        story.append(Paragraph(
            f"Склад: {wh}  |  Инвентаризация #{session_id}  |  Дата: {created}  |  Статус: {form.get('status', '')}",
            sub_style
        ))

        if not discrepant:
            story.append(Paragraph(
                "Расхождений не обнаружено. Все позиции соответствуют учётным данным.",
                sub_style
            ))
        else:
            headers = ["№", "Товар", "SKU", "Ед.", "По учёту", "Фактически", "Излишек (+)", "Недостача (−)"]
            col_widths = [1*cm, 6*cm, 2.5*cm, 1.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]

            surplus_total = 0.0
            shortage_total = 0.0

            table_data = [headers]
            for i, line in enumerate(discrepant, 1):
                book = float(line.get("book_quantity") or 0)
                fact = float(line["actual_quantity"])
                diff = fact - book
                surplus = f"{diff:.3f}" if diff > 0 else "—"
                shortage = f"{abs(diff):.3f}" if diff < 0 else "—"
                if diff > 0:
                    surplus_total += diff
                else:
                    shortage_total += abs(diff)
                table_data.append([
                    str(i),
                    str(line.get("product_name") or "")[:50],
                    str(line.get("sku") or "")[:20],
                    str(line.get("unit") or ""),
                    f"{book:.3f}",
                    f"{fact:.3f}",
                    surplus,
                    shortage,
                ])

            # Totals row
            table_data.append([
                "", "ИТОГО", "", "", "", "",
                f"{surplus_total:.3f}" if surplus_total else "—",
                f"{shortage_total:.3f}" if shortage_total else "—",
            ])

            tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 7.5),
                ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 7.5),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f1f5f9")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#f8fafc")]),
                # Highlight surplus in green
                ("TEXTCOLOR", (6, 1), (6, -2), colors.HexColor("#16a34a")),
                # Highlight shortage in red
                ("TEXTCOLOR", (7, 1), (7, -2), colors.HexColor("#dc2626")),
                ("FONTNAME", (6, 1), (7, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (4, 0), (7, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 0.5 * cm))
            story.append(Paragraph(
                f"Позиций с расхождением: {len(discrepant)}  |  "
                f"Излишки: {surplus_total:.3f}  |  Недостачи: {shortage_total:.3f}",
                sub_style
            ))

        story.append(Spacer(1, 1 * cm))
        story.append(Paragraph("Подписи комиссии:", sign_style))
        for role in [
            "Председатель комиссии (зав. склада): _____________________ Дата: ___________",
            "Член комиссии: _____________________ Дата: ___________",
            "Материально ответственное лицо: _____________________ Дата: ___________",
        ]:
            story.append(Paragraph(role, sign_style))

        doc.build(story)
        buf.seek(0)
        filename = f"comparison-{session_id}-{date.today()}.pdf"
        return Response(
            content=buf.read(),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"code": "internal_error", "message": str(exc), "details": {}},
        ) from exc


# === ПКУ PENDING CONTROLLED WRITE-OFFS (двойная подпись) ===

class PendingControlledWriteoffCreate(BaseModel):
    batch_id: int
    warehouse_id: int
    quantity: float
    reason: str | None = None
    patient_id: str
    doctor_id: str
    medical_record_no: str


class PendingControlledWriteoffConfirm(BaseModel):
    second_approver_id: str
    note: str | None = None


class PendingControlledWriteoffReject(BaseModel):
    rejected_reason: str


@router.post(
    "/controlled-writeoffs/pending",
    status_code=201,
    tags=["controlled-substances"],
    summary="Создать заявку на списание ПКУ (шаг 1: врач/медсестра)",
)
async def create_pending_controlled_writeoff(
    data: PendingControlledWriteoffCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_stock_access(actor_ctx, Permission.STOCK_WRITEOFF, data.warehouse_id)
        from decimal import Decimal as _D
        result = service.create_pending_controlled_writeoff(
            batch_id=data.batch_id,
            warehouse_id=data.warehouse_id,
            quantity=_D(str(data.quantity)),
            reason=data.reason,
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            medical_record_no=data.medical_record_no,
            requested_by=actor_id,
        )
        await publish_event(
            "controlled.writeoff.pending",
            {"pending_id": result["id"], "warehouse_id": data.warehouse_id, "batch_id": data.batch_id},
        )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.get(
    "/controlled-writeoffs/pending",
    tags=["controlled-substances"],
    summary="Список заявок на списание ПКУ",
)
def list_pending_controlled_writeoffs(
    warehouse_id: int | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        if warehouse_id is not None:
            require_warehouse_filter(actor_ctx, warehouse_id)
        return service.list_pending_controlled_writeoffs(
            warehouse_id=warehouse_id,
            status=status,
            limit=min(limit, 200),
            offset=offset,
        )
    except Exception as error:
        raise map_error(error) from error


@router.get(
    "/controlled-writeoffs/pending/{pending_id}",
    tags=["controlled-substances"],
    summary="Получить заявку на списание ПКУ по ID",
)
def get_pending_controlled_writeoff(
    pending_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        result = service.get_pending_controlled_writeoff(pending_id)
        require_warehouse_filter(actor_ctx, result["warehouse_id"])
        return result
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/controlled-writeoffs/pending/{pending_id}/confirm",
    tags=["controlled-substances"],
    summary="Подтвердить заявку на списание ПКУ (шаг 2: старшая медсестра/зав. склада)",
)
async def confirm_pending_controlled_writeoff(
    pending_id: int,
    data: PendingControlledWriteoffConfirm,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_WRITEOFF)
        result = service.confirm_pending_controlled_writeoff(
            pending_id=pending_id,
            second_approver_id=data.second_approver_id,
            note=data.note,
            actor_id=actor_id,
        )
        await publish_event(
            "controlled.writeoff.confirmed",
            {"pending_id": pending_id, "warehouse_id": result["warehouse_id"]},
        )
        await publish_event(
            "stock.balance.updated",
            {"batch_id": result["batch_id"], "warehouse_id": result["warehouse_id"]},
        )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/controlled-writeoffs/pending/{pending_id}/reject",
    tags=["controlled-substances"],
    summary="Отклонить заявку на списание ПКУ",
)
async def reject_pending_controlled_writeoff(
    pending_id: int,
    data: PendingControlledWriteoffReject,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
    actor_id: str = Depends(actor),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_WRITEOFF)
        result = service.reject_pending_controlled_writeoff(
            pending_id=pending_id,
            rejected_reason=data.rejected_reason,
            actor_id=actor_id,
        )
        await publish_event(
            "controlled.writeoff.rejected",
            {"pending_id": pending_id, "warehouse_id": result["warehouse_id"]},
        )
        return result
    except Exception as error:
        raise map_error(error) from error


# ── МИС-интеграция ────────────────────────────────────────────────────────────

@router.get("/mis/status", tags=["mis"])
def mis_status(
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    """Check MIS integration configuration (outbound webhook + inbound procedure events)."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        settings = get_settings()
        mapped_warehouses = service.count_mis_mapped_warehouses()
        templates = service.list_procedure_consumption_templates()
        return {
            "configured": bool(settings.mis_webhook_url),
            "webhook_url": settings.mis_webhook_url or None,
            "inbound_configured": bool(settings.mis_inbound_webhook_token),
            "inbound_endpoint": "/api/v1/mis/procedure-event",
            "mapped_warehouses": mapped_warehouses,
            "procedure_templates": len(templates),
        }
    except Exception as error:
        raise map_error(error) from error

@router.post("/mis/test", status_code=200, tags=["mis"])
def mis_test_connection(actor_ctx: ActorContext = Depends(get_actor_context)):
    """Send a test event to MIS webhook."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        from app.services.mis_client import MISClient
        settings = get_settings()
        if not settings.mis_webhook_url:
            raise ValidationError("МИС не настроена: укажите SKLAD_MIS_WEBHOOK_URL")
        client = MISClient(settings.mis_webhook_url, settings.mis_api_key)
        import datetime as _dt
        ok = client._send({"event": "test", "timestamp": _dt.datetime.now(_dt.UTC).isoformat(), "data": {"message": "Test from sklad"}})
        if not ok:
            raise ValidationError("МИС вернула ошибку. Проверьте URL и доступность системы.")
        return {"status": "ok", "message": "Тестовое событие отправлено в МИС"}
    except Exception as error:
        raise map_error(error) from error


class ProcedureConsumptionItemIn(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0)


class ProcedureConsumptionItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str | None = None
    quantity: str


class ProcedureConsumptionTemplateCreate(BaseModel):
    mis_clinic_id: str
    service_code: str
    name: str
    items: list[ProcedureConsumptionItemIn]


class ProcedureConsumptionTemplateOut(BaseModel):
    id: int
    mis_clinic_id: str
    service_code: str
    name: str
    created_by: str
    created_at: str
    items: list[ProcedureConsumptionItemOut]


@router.get(
    "/procedure-consumption-templates",
    response_model=list[ProcedureConsumptionTemplateOut],
    tags=["mis"],
)
def list_procedure_consumption_templates(
    mis_clinic_id: str | None = None,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.STOCK_READ)
        return service.list_procedure_consumption_templates(mis_clinic_id=mis_clinic_id)
    except Exception as error:
        raise map_error(error) from error


@router.post(
    "/procedure-consumption-templates",
    status_code=201,
    response_model=ProcedureConsumptionTemplateOut,
    tags=["mis"],
)
def create_procedure_consumption_template(
    body: ProcedureConsumptionTemplateCreate,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        return service.create_procedure_consumption_template(
            body.model_dump(), actor_id=actor_ctx.actor_id
        )
    except Exception as error:
        raise map_error(error) from error


@router.delete("/procedure-consumption-templates/{template_id}", status_code=204, tags=["mis"])
def delete_procedure_consumption_template(
    template_id: int,
    service: WarehouseService = Depends(get_warehouse_service),
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    try:
        require_permission(actor_ctx, Permission.CATALOG_WRITE)
        service.delete_procedure_consumption_template(template_id, actor_id=actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error


class MisProcedureEventIn(BaseModel):
    mis_clinic_id: str
    mis_room_id: str
    service_code: str
    mis_event_id: str
    patient_id: str | None = None
    doctor_id: str | None = None
    medical_record_no: str | None = None


class SupplierSelfUpdate(BaseModel):
    email: str | None = None
    phone: str | None = None
    contact_person: str | None = None
    city: str | None = None
    address: str | None = None
    delivery_days: int | None = None
    notes: str | None = None
    bank_details: str | None = None
    website: str | None = None
    inn: str | None = None


class ApplicationResubmitBody(BaseModel):
    name: str | None = None
    bin: str | None = None
    email: str | None = None
    phone: str | None = None
    contact_person: str | None = None
    city: str | None = None
    address: str | None = None
    delivery_days: int | None = None
    notes: str | None = None


class CatalogItemCreate(BaseModel):
    product_name: str
    sku: str | None = None
    unit: str = "шт"
    unit_price: float
    min_order_qty: float = 1
    stock_qty: float | None = None
    delivery_days: int | None = None
    category: str | None = None
    description: str | None = None
    product_id: int | None = None
    is_active: bool = True
    valid_until: str | None = None
    condition: str = "new"
    delivery_type: str = "buyer_arranges"
    delivery_price: float | None = None
    delivery_included: bool = False
    delivery_regions: str | None = None


class CatalogItemUpdate(BaseModel):
    product_name: str | None = None
    sku: str | None = None
    unit: str | None = None
    unit_price: float | None = None
    min_order_qty: float | None = None
    stock_qty: float | None = None
    delivery_days: int | None = None
    category: str | None = None
    description: str | None = None
    product_id: int | None = None
    is_active: bool | None = None
    valid_until: str | None = None
    condition: str | None = None
    delivery_type: str | None = None
    delivery_price: float | None = None
    delivery_included: bool | None = None
    delivery_regions: str | None = None


@router.post("/mis/procedure-event", tags=["mis"])
def mis_procedure_event(
    body: MisProcedureEventIn,
    authorization: str | None = Header(default=None, alias="Authorization"),
    service: WarehouseService = Depends(get_warehouse_service),
):
    """Inbound webhook: MIS notifies sklad that a procedure was completed.

    Sklad resolves the cabinet + procedure recipe and performs the FEFO
    write-off itself, so it keeps working even if MIS is briefly unreachable
    afterwards.
    """
    import secrets

    settings = get_settings()
    if not settings.mis_inbound_webhook_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "not_configured", "message": "МИС inbound webhook не настроен", "details": {}},
        )
    expected = f"Bearer {settings.mis_inbound_webhook_token}"
    if not authorization or not secrets.compare_digest(authorization, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "unauthorized", "message": "Invalid or missing webhook token", "details": {}},
        )
    try:
        return service.process_mis_procedure_event(
            mis_clinic_id=body.mis_clinic_id,
            mis_room_id=body.mis_room_id,
            service_code=body.service_code,
            mis_event_id=body.mis_event_id,
            patient_id=body.patient_id,
            doctor_id=body.doctor_id,
            medical_record_no=body.medical_record_no,
            actor_id="mis-integration",
        )
    except Exception as error:
        raise map_error(error) from error


# ── Бухгалтерская интеграция ──────────────────────────────────────────────────

@router.get("/accounting/status", tags=["accounting"])
def accounting_status(actor_ctx: ActorContext = Depends(get_actor_context)):
    """Check accounting integration status."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        settings = get_settings()
        return {
            "configured": bool(settings.accounting_webhook_url),
            "webhook_url": settings.accounting_webhook_url or None,
        }
    except Exception as error:
        raise map_error(error) from error

@router.post("/accounting/test", status_code=200, tags=["accounting"])
def accounting_test(actor_ctx: ActorContext = Depends(get_actor_context)):
    """Send a test event to accounting webhook."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        from app.services.accounting_client import AccountingClient
        settings = get_settings()
        if not settings.accounting_webhook_url:
            raise ValidationError("Бухгалтерия не настроена: укажите SKLAD_ACCOUNTING_WEBHOOK_URL")
        client = AccountingClient(settings.accounting_webhook_url, settings.accounting_webhook_secret)
        import datetime as _dt
        ok = client._send({"type": "test", "message": "Test from sklad", "date": _dt.datetime.now(_dt.UTC).strftime("%Y-%m-%d")})
        if not ok:
            raise ValidationError("Бухсистема вернула ошибку. Проверьте URL.")
        return {"status": "ok", "message": "Тестовое событие отправлено в бухсистему"}
    except Exception as error:
        raise map_error(error) from error


# ── Redis статус ──────────────────────────────────────────────────────────────

@router.get("/admin/redis-status", tags=["admin"])
def redis_status(actor_ctx: ActorContext = Depends(get_actor_context)):
    """Check Redis Pub/Sub availability."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.services.pubsub import is_available
        return {"redis_available": is_available()}
    except Exception as error:
        raise map_error(error) from error


# -- EDO/ECP (IS-ESF Kazakhstan) ----------------------------------------------

@router.get("/esf/status", tags=["esf"])
def esf_status(actor_ctx: ActorContext = Depends(get_actor_context)):
    """Check ESF integration configuration status."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        settings = get_settings()
        return {
            "configured": bool(settings.esf_username and settings.esf_password and settings.esf_seller_bin),
            "base_url": settings.esf_base_url,
            "seller_bin": settings.esf_seller_bin or None,
        }
    except Exception as error:
        raise map_error(error) from error


@router.post("/esf/connect", status_code=200, tags=["esf"])
def esf_connect(actor_ctx: ActorContext = Depends(get_actor_context)):
    """Test ESF connection and authenticate."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        from app.services.esf_client import ESFClient
        settings = get_settings()
        if not settings.esf_username or not settings.esf_password:
            raise ValidationError("ESF not configured: set SKLAD_ESF_USERNAME and SKLAD_ESF_PASSWORD")
        client = ESFClient(settings.esf_base_url)
        session_id = client.authenticate(settings.esf_username, settings.esf_password)
        return {"status": "connected", "session_id": session_id[:8] + "***"}
    except Exception as error:
        raise map_error(error) from error


@router.get("/esf/invoices", tags=["esf"])
def esf_list_invoices(
    date_from: str,
    date_to: str,
    actor_ctx: ActorContext = Depends(get_actor_context),
):
    """List ESF invoices in date range."""
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        from app.core.config import get_settings
        from app.services.esf_client import ESFClient
        settings = get_settings()
        if not settings.esf_username:
            raise ValidationError("ESF not configured")
        client = ESFClient(settings.esf_base_url)
        client.authenticate(settings.esf_username, settings.esf_password)
        return client.get_invoices(date_from, date_to)
    except Exception as error:
        raise map_error(error) from error


# ── Supplier self-service ────────────────────────────────────────────────────

@router.get("/supplier/me", tags=["supplier-self"])
def get_my_supplier_profile(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "No supplier linked to your account", "details": {}})
    try:
        svc = get_warehouse_service()
        return svc.get_supplier_by_id(actor_ctx.supplier_id)
    except Exception as error:
        raise map_error(error) from error

@router.patch("/supplier/me", tags=["supplier-self"])
def update_my_supplier_profile(
    body: SupplierSelfUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked to your account", "details": {}})
    try:
        svc = get_warehouse_service()
        return svc.update_supplier_self(actor_ctx.supplier_id, body.model_dump(exclude_none=True), actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error

@router.get("/supplier/verification-docs", tags=["supplier-self"])
def get_my_verification_docs(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().list_supplier_verification_docs(actor_ctx.supplier_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/supplier/verification-docs/upload", tags=["supplier-self"])
async def upload_verification_doc(
    doc_type: str = "other",
    file: UploadFile = File(...),
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    allowed_types = {"registration", "license", "certificate", "bank", "other"}
    if doc_type not in allowed_types:
        raise HTTPException(status_code=422, detail={"code": "validation_error", "message": f"doc_type must be one of {allowed_types}", "details": {}})
    import os, uuid
    from pathlib import Path
    uploads_dir = Path(os.getenv("SKLAD_UPLOADS_DIR", "/opt/sklad/uploads")) / "verification"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(file.filename or "doc").suffix or ".bin"
    fname = f"{uuid.uuid4().hex}{suffix}"
    fpath = uploads_dir / fname
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail={"code": "file_too_large", "message": "Max file size is 10MB", "details": {}})
    with open(fpath, "wb") as fp:
        fp.write(content)
    file_url = f"/sklad/uploads/verification/{fname}"
    try:
        return get_warehouse_service().add_supplier_verification_doc(
            actor_ctx.supplier_id, doc_type, file_url, file.filename, actor_ctx.actor_id
        )
    except Exception as error:
        raise map_error(error) from error


@router.delete("/supplier/verification-docs/{doc_id}", status_code=204, tags=["supplier-self"])
def delete_verification_doc(
    doc_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> None:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        get_warehouse_service().delete_supplier_verification_doc(doc_id, actor_ctx.supplier_id)
    except Exception as error:
        raise map_error(error) from error


class SupplierVerifyBody(BaseModel):
    is_verified: bool
    comment: str | None = None


@router.post("/admin/suppliers/{supplier_id}/verify", tags=["admin"])
def set_supplier_verified(
    supplier_id: int,
    body: SupplierVerifyBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    require_permission(actor_ctx, Permission.ADMIN_USERS)
    try:
        return get_warehouse_service().set_supplier_verified(
            supplier_id, body.is_verified, body.comment, actor_ctx.actor_id
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/my-applications", tags=["supplier-self"])
def get_my_supplier_applications(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    """Return supplier applications submitted by the current actor. Works for all authenticated users."""
    try:
        svc = get_warehouse_service()
        return svc.get_my_supplier_applications(actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error

@router.post("/supplier/my-applications/{application_id}/resubmit", tags=["supplier-self"])
def resubmit_supplier_application_endpoint(
    application_id: int,
    body: ApplicationResubmitBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        svc = get_warehouse_service()
        return svc.resubmit_supplier_application(
            application_id,
            body.model_dump(exclude_none=True),
            actor_ctx.actor_id,
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail={"code": "bad_request", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


# ── Supplier Catalog / Marketplace ───────────────────────────────────────────

@router.get("/marketplace/catalog", tags=["marketplace"])
def browse_catalog(
    supplier_id: int | None = None,
    category: str | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: str | None = None,
    limit: int = 100,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Browse all active supplier catalog items. Available to all authenticated users."""
    try:
        svc = get_warehouse_service()
        return svc.list_supplier_catalog(
            supplier_id=supplier_id, category=category, search=search,
            min_price=min_price, max_price=max_price,
            active_only=True, sort=sort, limit=limit, offset=offset,
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/catalog/categories", tags=["marketplace"])
def list_catalog_categories(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return get_warehouse_service().list_catalog_categories()
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/catalog/{item_id}", tags=["marketplace"])
def get_catalog_item(
    item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        svc = get_warehouse_service()
        item = svc.get_catalog_item(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found", "details": {}})
        return item
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


class CatalogItemReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


@router.post("/marketplace/catalog/{item_id}/reviews", status_code=201, tags=["marketplace"])
def create_catalog_item_review_endpoint(
    item_id: int,
    body: CatalogItemReviewCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        svc = get_warehouse_service()
        return svc.create_catalog_item_review(item_id, body.rating, body.comment, actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/catalog/{item_id}/reviews", tags=["marketplace"])
def list_catalog_item_reviews_endpoint(
    item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().list_catalog_item_reviews(item_id)
    except Exception as error:
        raise map_error(error) from error


class CatalogItemReviewModerate(BaseModel):
    action: str = Field(pattern="^(approve|reject)$")


@router.patch("/catalog-item-reviews/{review_id}", tags=["admin"])
def moderate_catalog_item_review_endpoint(
    review_id: int,
    body: CatalogItemReviewModerate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        require_permission(actor_ctx, Permission.ADMIN_USERS)
        return get_warehouse_service().moderate_catalog_item_review(review_id, body.action)
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/catalog", tags=["supplier-self"])
def get_my_catalog(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    """Return all catalog items (incl. inactive) for the current supplier."""
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        return svc.list_supplier_catalog(supplier_id=actor_ctx.supplier_id, active_only=False, limit=500)
    except Exception as error:
        raise map_error(error) from error


@router.post("/supplier/catalog", status_code=201, tags=["supplier-self"])
def create_catalog_item_endpoint(
    body: CatalogItemCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        return svc.create_catalog_item(actor_ctx.supplier_id, body.model_dump())
    except Exception as error:
        raise map_error(error) from error


@router.patch("/supplier/catalog/{item_id}", tags=["supplier-self"])
def update_catalog_item_endpoint(
    item_id: int,
    body: CatalogItemUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        result = svc.update_catalog_item(item_id, actor_ctx.supplier_id, body.model_dump(exclude_none=True))
        if result is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found or not yours", "details": {}})
        return result
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.delete("/supplier/catalog/{item_id}", status_code=204, tags=["supplier-self"])
def delete_catalog_item_endpoint(
    item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> None:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        ok = svc.delete_catalog_item(item_id, actor_ctx.supplier_id)
        if not ok:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found or not yours", "details": {}})
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


class MarketplaceInquiryCreate(BaseModel):
    quantity: float = Field(gt=0, default=1)
    notes: str | None = None
    warehouse_id: int | None = None
    purchase_request_id: int | None = None
    source: str = Field(default="marqet", pattern="^(marqet|qpartner|api)$")


class InquiryResponseBody(BaseModel):
    response_text: str = Field(min_length=1)


# ── Marketplace Directory ────────────────────────────────────────────────────

@router.get("/marketplace/suppliers", tags=["marketplace"])
def list_supplier_directory(
    city: str | None = None,
    category: str | None = None,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().list_suppliers_directory(
            city=city, category=category, search=search, limit=limit, offset=offset
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/suppliers/{supplier_id}", tags=["marketplace"])
def get_supplier_profile_endpoint(
    supplier_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Public seller storefront: profile, rating, catalog and reviews."""
    try:
        profile = get_warehouse_service().get_supplier_profile(supplier_id)
        if profile is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Supplier not found", "details": {}})
        return profile
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/stats", tags=["supplier-self"])
def get_supplier_dashboard_stats(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().get_supplier_stats(actor_ctx.supplier_id)
    except Exception as error:
        raise map_error(error) from error


# ── Marketplace Inquiries ────────────────────────────────────────────────────

@router.post("/marketplace/inquire/{item_id}", status_code=201, tags=["marketplace"])
def create_inquiry(
    item_id: int,
    body: MarketplaceInquiryCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        svc = get_warehouse_service()
        warehouse_id = body.warehouse_id
        if warehouse_id is None and actor_ctx.warehouse_ids:
            warehouse_id = list(actor_ctx.warehouse_ids)[0]
        return svc.create_marketplace_inquiry(
            catalog_item_id=item_id,
            actor_id=actor_ctx.actor_id,
            quantity=body.quantity,
            notes=body.notes,
            warehouse_id=warehouse_id,
            purchase_request_id=body.purchase_request_id,
            source=body.source,
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/my-inquiries", tags=["marketplace"])
def list_my_inquiries(
    status: str | None = None,
    source: str | None = None,
    limit: int = 50,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().list_marketplace_inquiries(
            actor_id=actor_ctx.actor_id, status=status, source=source, limit=limit
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/inquiries", tags=["supplier-self"])
def list_supplier_inquiries(
    status: str | None = None,
    source: str | None = None,
    limit: int = 50,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().list_marketplace_inquiries(
            supplier_id=actor_ctx.supplier_id, status=status, source=source, limit=limit
        )
    except Exception as error:
        raise map_error(error) from error


@router.post("/supplier/inquiries/{inquiry_id}/respond", tags=["supplier-self"])
def respond_to_inquiry_endpoint(
    inquiry_id: int,
    body: InquiryResponseBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().respond_to_inquiry(inquiry_id, actor_ctx.supplier_id, body.response_text)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


class InquiryMessageBody(BaseModel):
    body: str = Field(min_length=1, max_length=4000)


@router.get("/marketplace/my-inquiries/{inquiry_id}/messages", tags=["marketplace"])
def get_inquiry_messages_buyer(
    inquiry_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Buyer fetches full chat thread for their inquiry."""
    try:
        return get_warehouse_service().list_inquiry_messages(inquiry_id, actor_ctx.actor_id)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


@router.post("/marketplace/my-inquiries/{inquiry_id}/messages", tags=["marketplace"])
def add_inquiry_message_buyer(
    inquiry_id: int,
    body: InquiryMessageBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Buyer sends a follow-up message on an inquiry."""
    try:
        return get_warehouse_service().add_inquiry_message(inquiry_id, actor_ctx.actor_id, body.body)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/inquiries/{inquiry_id}/messages", tags=["supplier-self"])
def get_inquiry_messages_supplier(
    inquiry_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Supplier fetches full chat thread for an inquiry."""
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        supplier_actor = f"supplier-actor:{actor_ctx.supplier_id}"
        return get_warehouse_service().list_inquiry_messages(inquiry_id, supplier_actor)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


@router.post("/supplier/inquiries/{inquiry_id}/messages", tags=["supplier-self"])
def add_inquiry_message_supplier(
    inquiry_id: int,
    body: InquiryMessageBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Supplier sends a follow-up message (alternative to respond endpoint)."""
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        supplier_actor = f"supplier-actor:{actor_ctx.supplier_id}"
        return get_warehouse_service().add_inquiry_message(inquiry_id, supplier_actor, body.body)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


class InquiryStatusUpdate(BaseModel):
    status: str = Field(pattern="^(ordered|closed)$")


@router.patch("/marketplace/my-inquiries/{inquiry_id}", tags=["marketplace"])
def update_my_inquiry_status(
    inquiry_id: int,
    body: InquiryStatusUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().update_inquiry_status(
            inquiry_id, actor_ctx.actor_id, body.status
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail={"code": "validation_error", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


# ── Supplier: create shipment from inquiry ───────────────────────────────────

class InquiryShipmentCreate(BaseModel):
    estimated_arrival: date | None = None
    origin_city: str | None = None
    destination_warehouse_id: int | None = None
    reference: str | None = None
    notes: str | None = None


@router.post("/supplier/inquiries/{inquiry_id}/create-shipment", status_code=201, tags=["supplier-self"])
def create_shipment_from_inquiry(
    inquiry_id: int,
    body: InquiryShipmentCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().create_shipment_from_inquiry(
            inquiry_id, actor_ctx.supplier_id, body.model_dump(exclude_none=True)
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


# ── Marketplace cart (Kaspi/Amazon-style checkout) ──────────────────────────

class CartItemAdd(BaseModel):
    catalog_item_id: int
    quantity: float = Field(gt=0, default=1)


class CartItemQuantityUpdate(BaseModel):
    quantity: float = Field(gt=0)


class CartCheckout(BaseModel):
    warehouse_id: int | None = None
    notes: str | None = None
    source: str = Field(default="qpartner", pattern="^(marqet|qpartner|api)$")


class MarketplaceOrderCheckout(BaseModel):
    warehouse_id: int | None = None
    source: str = Field(default="marqet", pattern="^(marqet|qpartner|api)$")
    buyer_name: str | None = Field(default=None, max_length=255)
    buyer_phone: str | None = Field(default=None, max_length=64)
    buyer_email: str | None = Field(default=None, max_length=255)
    delivery_address: str | None = Field(default=None, max_length=1000)
    notes: str | None = Field(default=None, max_length=1000)


class PaymentMethodBind(BaseModel):
    provider: str = Field(min_length=1, max_length=64)
    provider_token: str = Field(min_length=8, max_length=512)
    brand: str = Field(default="unknown", max_length=32)
    last4: str = Field(min_length=4, max_length=32)
    expiry_month: int | None = Field(default=None, ge=1, le=12)
    expiry_year: int | None = Field(default=None, ge=2024, le=2100)
    holder_name: str | None = Field(default=None, max_length=255)
    is_default: bool = False


class MarketplacePaymentCreate(BaseModel):
    provider: str = Field(default="manual", max_length=64)
    payment_method_id: int | None = None


class MarketplacePaymentWebhook(BaseModel):
    payment_id: int
    status: str = Field(pattern="^(paid|failed|cancelled|refunded|authorized)$")
    provider_event_id: str = Field(min_length=1, max_length=255)
    provider_payment_id: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="KZT", pattern="^[A-Z]{3}$")
    payload: dict[str, Any] = Field(default_factory=dict)


@router.get("/marketplace/cart", tags=["marketplace"])
def get_cart_endpoint(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return get_warehouse_service().get_cart(actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/marketplace/cart/items", status_code=201, tags=["marketplace"])
def add_cart_item_endpoint(
    body: CartItemAdd,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().add_to_cart(actor_ctx.actor_id, body.catalog_item_id, body.quantity)
    except Exception as error:
        raise map_error(error) from error


@router.patch("/marketplace/cart/items/{cart_item_id}", tags=["marketplace"])
def update_cart_item_endpoint(
    cart_item_id: int,
    body: CartItemQuantityUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().update_cart_item(actor_ctx.actor_id, cart_item_id, body.quantity)
    except Exception as error:
        raise map_error(error) from error


@router.delete("/marketplace/cart/items/{cart_item_id}", tags=["marketplace"])
def remove_cart_item_endpoint(
    cart_item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().remove_from_cart(actor_ctx.actor_id, cart_item_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/marketplace/cart/checkout", status_code=201, tags=["marketplace"])
def checkout_cart_endpoint(
    body: CartCheckout,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        svc = get_warehouse_service()
        warehouse_id = body.warehouse_id
        if warehouse_id is None and actor_ctx.warehouse_ids:
            warehouse_id = list(actor_ctx.warehouse_ids)[0]
        return svc.checkout_cart(actor_ctx.actor_id, warehouse_id, body.notes, body.source)
    except Exception as error:
        raise map_error(error) from error


@router.post("/marketplace/orders/checkout", status_code=201, tags=["marketplace"])
def checkout_marketplace_order_endpoint(
    body: MarketplaceOrderCheckout,
    actor_ctx: ActorContext = Depends(get_actor_context),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> Any:
    try:
        svc = get_warehouse_service()
        warehouse_id = body.warehouse_id
        if warehouse_id is None and actor_ctx.warehouse_ids:
            warehouse_id = list(actor_ctx.warehouse_ids)[0]
        result, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_ctx.actor_id,
            method="POST",
            path="/api/v1/marketplace/orders/checkout",
            payload=body,
            response_status=status.HTTP_201_CREATED,
            resource_type="marketplace_order_checkout",
            operation=lambda: {
                "items": svc.create_marketplace_orders_from_cart(
                    actor_ctx.actor_id,
                    warehouse_id=warehouse_id,
                    source=body.source,
                    buyer_name=body.buyer_name,
                    buyer_phone=body.buyer_phone,
                    buyer_email=body.buyer_email,
                    delivery_address=body.delivery_address,
                    notes=body.notes,
                )
            },
        )
        return result
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/account/summary", tags=["marketplace"])
def marketplace_account_summary(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return get_warehouse_service().get_marketplace_account_summary(actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/orders", tags=["marketplace"])
def list_marketplace_orders_endpoint(
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = 50,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return get_warehouse_service().list_marketplace_orders(
            actor_ctx.actor_id, status=status_filter, limit=safe_limit, offset=safe_offset
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/orders/{order_id}", tags=["marketplace"])
def get_marketplace_order_endpoint(
    order_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().get_marketplace_order(actor_ctx.actor_id, order_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/marketplace/orders/{order_id}/payments", status_code=201, tags=["marketplace"])
def create_marketplace_payment_endpoint(
    order_id: int,
    body: MarketplacePaymentCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> Any:
    try:
        svc = get_warehouse_service()
        payment, _ = run_idempotent(
            idempotency_key=idempotency_key,
            store=idempotency_store,
            actor_id=actor_ctx.actor_id,
            method="POST",
            path=f"/api/v1/marketplace/orders/{order_id}/payments",
            payload={"order_id": order_id, "body": body},
            response_status=status.HTTP_201_CREATED,
            resource_type="marketplace_payment",
            operation=lambda: svc.create_marketplace_payment(
                actor_ctx.actor_id,
                order_id,
                provider=body.provider,
                payment_method_id=body.payment_method_id,
                idempotency_key=idempotency_key,
            ),
        )
        return payment
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/payment-methods", tags=["marketplace"])
def list_marketplace_payment_methods_endpoint(
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().list_marketplace_payment_methods(actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/marketplace/payment-methods", status_code=201, tags=["marketplace"])
def bind_marketplace_payment_method_endpoint(
    body: PaymentMethodBind,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().bind_marketplace_payment_method(
            actor_ctx.actor_id,
            provider=body.provider,
            provider_token=body.provider_token,
            brand=body.brand,
            last4=body.last4,
            expiry_month=body.expiry_month,
            expiry_year=body.expiry_year,
            holder_name=body.holder_name,
            is_default=body.is_default,
        )
    except Exception as error:
        raise map_error(error) from error


@router.patch("/marketplace/payment-methods/{method_id}/default", tags=["marketplace"])
def set_default_marketplace_payment_method_endpoint(
    method_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return get_warehouse_service().set_default_marketplace_payment_method(actor_ctx.actor_id, method_id)
    except Exception as error:
        raise map_error(error) from error


@router.delete("/marketplace/payment-methods/{method_id}", status_code=204, tags=["marketplace"])
def delete_marketplace_payment_method_endpoint(
    method_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Response:
    try:
        get_warehouse_service().delete_marketplace_payment_method(actor_ctx.actor_id, method_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as error:
        raise map_error(error) from error


@router.post("/marketplace/payments/webhook/{provider}", tags=["marketplace"])
async def marketplace_payment_webhook_endpoint(
    request: Request,
    provider: str,
    body: MarketplacePaymentWebhook,
    webhook_secret: str | None = Header(default=None, alias="X-Payment-Webhook-Secret"),
    webhook_signature: str | None = Header(default=None, alias="X-Payment-Signature"),
) -> Any:
    settings = get_settings()
    if not settings.marketplace_payment_webhook_secret or webhook_secret != settings.marketplace_payment_webhook_secret:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "Invalid payment webhook secret", "details": {}})
    raw_body = await request.body()
    expected_signature = hmac.new(
        settings.marketplace_payment_webhook_secret.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    provided_signature = (webhook_signature or "").removeprefix("sha256=").strip()
    if not provided_signature or not hmac.compare_digest(provided_signature, expected_signature):
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "Invalid payment webhook signature", "details": {}})
    try:
        return get_warehouse_service().apply_marketplace_payment_event(
            provider=provider,
            provider_event_id=body.provider_event_id,
            provider_payment_id=body.provider_payment_id,
            payment_id=body.payment_id,
            status=body.status,
            amount=body.amount,
            currency=body.currency,
            payload=body.payload,
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/loyalty", tags=["marketplace"])
def marketplace_loyalty_endpoint() -> Any:
    return {
        "tier": "bronze",
        "points_balance": 0,
        "points_pending": 0,
        "next_tier_points": 5000,
        "lifetime_spend": 0,
        "currency": "KZT",
        "history": [],
    }


@router.get("/supplier/marketplace-orders", tags=["supplier-self"])
def list_supplier_marketplace_orders_endpoint(
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = 50,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return get_warehouse_service().list_supplier_marketplace_orders(
            actor_ctx.supplier_id, status=status_filter, limit=safe_limit, offset=safe_offset
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/marketplace-orders/{order_id}", tags=["supplier-self"])
def get_supplier_marketplace_order_endpoint(
    order_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().get_supplier_marketplace_order(actor_ctx.supplier_id, order_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/marketplace-wallet", tags=["supplier-self"])
def get_supplier_marketplace_wallet_endpoint(
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().get_supplier_marketplace_wallet(actor_ctx.supplier_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/marketplace-wallet/ledger", tags=["supplier-self"])
def list_supplier_marketplace_ledger_endpoint(
    limit: int = 50,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        safe_limit, safe_offset = pagination_meta(limit, offset)
        return get_warehouse_service().list_supplier_marketplace_ledger(
            actor_ctx.supplier_id, limit=safe_limit, offset=safe_offset
        )
    except Exception as error:
        raise map_error(error) from error


# ── Bulk inquiry ─────────────────────────────────────────────────────────────

class BulkInquiryCreate(BaseModel):
    product_name: str = Field(min_length=1)
    quantity: float = Field(gt=0, default=1)
    notes: str | None = None
    warehouse_id: int | None = None
    source: str = Field(default="qpartner", pattern="^(marqet|qpartner|api)$")


@router.post("/marketplace/bulk-inquire", status_code=201, tags=["marketplace"])
def create_bulk_inquiry(
    body: BulkInquiryCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        svc = get_warehouse_service()
        warehouse_id = body.warehouse_id
        if warehouse_id is None and actor_ctx.warehouse_ids:
            warehouse_id = list(actor_ctx.warehouse_ids)[0]
        return svc.create_bulk_inquiry(
            product_name=body.product_name,
            actor_id=actor_ctx.actor_id,
            quantity=body.quantity,
            notes=body.notes,
            warehouse_id=warehouse_id,
            source=body.source,
        )
    except Exception as error:
        raise map_error(error) from error


# ── Supplier catalog CSV import ───────────────────────────────────────────────

@router.post("/supplier/catalog/import-csv", status_code=201, tags=["supplier-self"])
async def import_catalog_csv(
    file: UploadFile,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        import csv, io
        content = await file.read()
        text = content.decode("utf-8-sig")  # handle BOM
        reader = csv.DictReader(io.StringIO(text))
        rows = list(reader)
        if not rows:
            raise HTTPException(status_code=422, detail={"code": "validation_error", "message": "CSV файл пуст или неверный формат", "details": {}})
        return get_warehouse_service().import_catalog_csv(actor_ctx.supplier_id, rows)
    except HTTPException:
        raise
    except UnicodeDecodeError as error:
        raise HTTPException(status_code=422, detail={"code": "validation_error", "message": "Файл должен быть в кодировке UTF-8", "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


# ── Supplier catalog analytics ────────────────────────────────────────────────

@router.get("/supplier/catalog/analytics", tags=["supplier-self"])
def get_catalog_analytics(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().get_catalog_item_inquiry_stats(actor_ctx.supplier_id)
    except Exception as error:
        raise map_error(error) from error


class ReviewReplyBody(BaseModel):
    reply_text: str = Field(min_length=1, max_length=2000)


class BulkPriceUpdate(BaseModel):
    percent_change: float = Field(description="Percentage change, e.g. 10 means +10%, -5 means -5%")
    item_ids: list[int] | None = Field(default=None, description="Specific item IDs; omit to update all")


@router.post("/supplier/reviews/{review_id}/reply", tags=["supplier-self"])
def reply_to_review(
    review_id: int,
    body: ReviewReplyBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().reply_to_review(
            review_id=review_id,
            supplier_id=actor_ctx.supplier_id,
            reply_text=body.reply_text,
        )
    except Exception as error:
        raise map_error(error) from error


@router.get("/supplier/orders", tags=["supplier-self"])
def list_supplier_orders(
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().list_supplier_orders(
            supplier_id=actor_ctx.supplier_id,
            status=status,
            limit=min(limit, 200),
            offset=offset,
        )
    except Exception as error:
        raise map_error(error) from error


@router.post("/supplier/catalog/bulk-price", tags=["supplier-self"])
def bulk_update_catalog_prices(
    body: BulkPriceUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().bulk_update_catalog_prices(
            supplier_id=actor_ctx.supplier_id,
            item_ids=body.item_ids,
            percent_change=body.percent_change,
        )
    except Exception as error:
        raise map_error(error) from error




# ── Supplier catalog item image ───────────────────────────────────────────────

@router.post("/supplier/catalog/{item_id}/image/upload", tags=["supplier-self"], summary="Upload catalog item photo")
async def upload_catalog_item_image(
    item_id: int,
    file: UploadFile,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    import uuid, aiofiles
    from pathlib import Path
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    MAX_SIZE = 8 * 1024 * 1024
    ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED:
        raise HTTPException(status_code=422, detail={"code": "invalid_file_type", "message": f"Разрешены JPG PNG WEBP. Получен: {ext}", "details": {}})
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=422, detail={"code": "file_too_large", "message": "Файл больше 8 МБ", "details": {}})
    try:
        uploads_dir = Path(__file__).resolve().parents[2] / "uploads" / "catalog"
        uploads_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{item_id}_{uuid.uuid4().hex[:8]}{ext}"
        dest = uploads_dir / safe_name
        async with aiofiles.open(dest, "wb") as f_out:
            await f_out.write(content)
        image_url = f"/uploads/catalog/{safe_name}"
        svc = get_warehouse_service()
        result = svc.update_catalog_item(item_id, actor_ctx.supplier_id, {"image_url": image_url})
        if result is None:
            dest.unlink(missing_ok=True)
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found or not yours", "details": {}})
        return {"item_id": item_id, "image_url": image_url, "item": result}
    except HTTPException:
        raise
    except Exception as exc:
        raise map_error(exc) from exc


@router.delete("/supplier/catalog/{item_id}/image", status_code=204, tags=["supplier-self"], summary="Remove catalog item photo")
def delete_catalog_item_image(
    item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> None:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        result = svc.update_catalog_item(item_id, actor_ctx.supplier_id, {"image_url": None})
        if result is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found or not yours", "details": {}})
    except HTTPException:
        raise
    except Exception as exc:
        raise map_error(exc) from exc


@router.post("/admin/test-email", status_code=200, tags=["admin"])
def test_email(
    to_email: str,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Send a test email to verify SMTP configuration."""
    require_permission(actor_ctx, Permission.ADMIN_USERS)
    try:
        from app.services.email_notifier import _send
        from app.core.config import get_settings as _gs; _settings = _gs()
        _send(_settings, to_email, "Тест: Sklad email работает",
              "<h2>Тест успешен!</h2><p>SMTP настроен корректно.</p>")
        return {"sent": True, "to": to_email}
    except Exception as exc:
        raise HTTPException(status_code=422, detail={"code": "smtp_error", "message": str(exc), "details": {}}) from exc
class PurchaseOrderCreate(BaseModel):
    buyer_name: str | None = None
    buyer_bin: str | None = None
    buyer_address: str | None = None
    buyer_contact: str | None = None
    delivery_address: str | None = None
    payment_terms: str | None = None
    notes: str | None = None
    delivery_type: str | None = Field(default=None, pattern="^(pickup|courier|freight|postal|buyer_arranges)$")
    delivery_price: float | None = Field(default=None, ge=0)
    delivery_included: bool = False
    escrow_amount: float | None = Field(default=None, ge=0)


class EscrowActionBody(BaseModel):
    action: str = Field(pattern="^(reserve|release|refund)$")


class DeliveryUpdateBody(BaseModel):
    delivery_status: str | None = Field(default=None, pattern="^(pending|preparing|shipped|in_transit|delivered|returned)$")
    delivery_tracking_number: str | None = None
    delivery_type: str | None = Field(default=None, pattern="^(pickup|courier|freight|postal|buyer_arranges)$")
    delivery_price: float | None = Field(default=None, ge=0)
    delivery_included: bool | None = None


class GovAdvanceBody(BaseModel):
    pass


class GovFeedbackBody(BaseModel):
    feedback_text: str
    rating: int = Field(ge=1, le=5)


@router.post("/marketplace/my-inquiries/{inquiry_id}/purchase-order", tags=["marketplace"])
def create_po(
    inquiry_id: int,
    body: PurchaseOrderCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Create (or return existing) Purchase Order for an inquiry."""
    try:
        return get_warehouse_service().create_purchase_order(
            inquiry_id, actor_ctx.actor_id, body.model_dump(exclude_none=True)
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/my-inquiries/{inquiry_id}/purchase-order/html", tags=["marketplace"],
            response_class=HTMLResponse)
def get_po_html(
    inquiry_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Return printable HTML for a Purchase Order."""
    from fastapi.responses import HTMLResponse as _HR
    try:
        data = get_warehouse_service().get_purchase_order(inquiry_id, actor_ctx.actor_id)
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error

    inq = data["inquiry"]
    po = data["po"]

    def esc(v):
        if v is None: return "—"
        return str(v).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def row(label, val):
        v = esc(val)
        return f'<div style="margin-bottom:4px"><span style="color:#666;font-size:11px">{label}</span><div>{v}</div></div>' if val else ""

    STATUS_LABELS = {"draft": "Черновик", "sent": "Отправлен", "accepted": "Принят", "completed": "Завершён", "cancelled": "Отменён"}
    status_label = STATUS_LABELS.get(po["status"] if po else "draft", "—") if po else "Без PO"
    po_number = po["po_number"] if po else f"INQ-{inquiry_id}"
    created_date = (str(po["created_at"])[:10] if po else str(inq["created_at"])[:10])
    verified_badge = '<div style="font-size:12px;margin-top:4px"><span style="background:#16a34a;color:#fff;padding:2px 8px;border-radius:10px;font-size:11px">✅ Верифицирован</span></div>' if inq.get("supplier_verified") else ""

    buyer_rows = (
        row("Организация", po["buyer_name"] if po else None) +
        row("БИН", po["buyer_bin"] if po else None) +
        row("Адрес", po["buyer_address"] if po else None) +
        row("Контактное лицо", po["buyer_contact"] if po else None)
    ) or "<div style='color:#999'>Данные не указаны</div>"

    supplier_rows = (
        row("Организация", inq["supplier_name"]) +
        row("БИН/ИНН", inq.get("supplier_bin") or inq.get("supplier_inn")) +
        row("Адрес", inq.get("supplier_address")) +
        row("Город", inq.get("supplier_city")) +
        row("Телефон", inq.get("supplier_phone")) +
        row("Email", inq.get("supplier_email"))
    ) or "<div style='color:#999'>—</div>"

    unit_price_str = f'{float(inq["unit_price"]):,.2f} тг' if inq.get("unit_price") else "—"
    qty = float(inq["quantity"])
    total = float(inq["unit_price"]) * qty if inq.get("unit_price") else None
    total_price_str = f'{total:,.2f} тг' if total else "—"

    delivery_address_row = f'<strong>Адрес доставки:</strong> {esc(po["delivery_address"])}<br>' if po and po.get("delivery_address") else ""
    delivery_type_row = f'<strong>Тип доставки:</strong> {esc(po["delivery_type"])}<br>' if po and po.get("delivery_type") else ""
    delivery_price_row = f'<strong>Стоимость доставки:</strong> {float(po["delivery_price"]):,.2f} тг<br>' if po and po.get("delivery_price") is not None else ""
    delivery_included_row = f'<strong>Доставка включена:</strong> {"Да" if po.get("delivery_included") else "Нет"}<br>' if po else ""
    escrow_amount_row = f'<strong>Эскроу:</strong> {float(po["escrow_amount"]):,.2f} тг<br>' if po and po.get("escrow_amount") is not None else ""
    notes_row = f'<strong>Примечания:</strong> {esc(po["notes"] if po else inq.get("notes"))}<br>' if (po and po.get("notes")) or inq.get("notes") else ""
    sup_verified = ' <span style="background:#16a34a;color:#fff;padding:1px 6px;border-radius:8px;font-size:10px">✅</span>' if inq.get("supplier_verified") else ""
    payment_terms = esc(po["payment_terms"] if po else None) if po else "По договорённости"

    _PO_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Заказ {po_number}</title>
<style>
  body{{font-family:Arial,sans-serif;font-size:13px;margin:0;padding:20px;color:#111}}
  h1{{font-size:20px;margin:0 0 4px}}
  .header{{display:flex;justify-content:space-between;margin-bottom:20px;border-bottom:2px solid #000;padding-bottom:14px}}
  .parties{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}}
  .party{{border:1px solid #ddd;padding:12px;border-radius:4px}}
  .party h3{{margin:0 0 8px;font-size:14px;border-bottom:1px solid #eee;padding-bottom:6px}}
  table{{width:100%;border-collapse:collapse;margin-bottom:20px}}
  th{{background:#f5f5f5;text-align:left;padding:8px;font-size:12px;border:1px solid #ddd}}
  td{{padding:8px;border:1px solid #ddd;font-size:12px}}
  .total{{text-align:right;font-size:15px;font-weight:bold;margin-bottom:20px}}
  .terms{{background:#f9f9f9;padding:12px;border-radius:4px;font-size:12px;margin-bottom:20px}}
  .sign{{display:grid;grid-template-columns:1fr 1fr;gap:40px;margin-top:40px}}
  .sign-block{{border-top:1px solid #000;padding-top:8px;font-size:12px;color:#555}}
  @media print{{button{{display:none}}}}
</style>
</head>
<body>
<button onclick="window.print()" style="position:fixed;top:16px;right:16px;padding:8px 16px;background:#2563eb;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:13px">&#x1F5A8; Печать</button>
<div class="header">
  <div>
    <h1>ЗАКАЗ НА ПОСТАВКУ</h1>
    <div style="font-size:16px;font-weight:bold;color:#2563eb">{po_number}</div>
    <div style="font-size:12px;color:#555;margin-top:4px">Дата: {created_date}</div>
  </div>
  <div style="text-align:right">
    <div style="font-size:12px;color:#555">Статус: <strong>{status_label}</strong></div>
    {verified_badge}
  </div>
</div>
<div class="parties">
  <div class="party"><h3>ПОКУПАТЕЛЬ</h3>{buyer_rows}</div>
  <div class="party"><h3>ПОСТАВЩИК{sup_verified}</h3>{supplier_rows}</div>
</div>
<table>
  <tr><th style="width:40%">Наименование товара</th><th>Кол-во</th><th>Ед. изм.</th><th>Цена за ед.</th><th>Сумма</th></tr>
  <tr><td>{product_name}</td><td>{quantity}</td><td>{unit}</td><td>{unit_price}</td><td>{total_price}</td></tr>
</table>
<div class="total">ИТОГО: {total_price}</div>
<div class="terms"><strong>Условия оплаты:</strong> {payment_terms}<br>{delivery_address_row}{delivery_type_row}{delivery_price_row}{delivery_included_row}{escrow_amount_row}{notes_row}</div>
<div class="sign">
  <div class="sign-block">Покупатель: __________________ / ____________________</div>
  <div class="sign-block">Поставщик: __________________ / ____________________</div>
</div>
</body>
</html>"""

    html = _PO_HTML_TEMPLATE.format(
        po_number=esc(po_number),
        created_date=esc(created_date),
        status_label=esc(status_label),
        verified_badge=verified_badge,
        buyer_rows=buyer_rows,
        supplier_rows=supplier_rows,
        sup_verified=sup_verified,
        product_name=esc(inq["product_name"]),
        quantity=esc(str(qty)),
        unit=esc(inq.get("unit", "")),
        unit_price=unit_price_str,
        total_price=total_price_str,
        payment_terms=payment_terms,
        delivery_address_row=delivery_address_row,
        delivery_type_row=delivery_type_row,
        delivery_price_row=delivery_price_row,
        delivery_included_row=delivery_included_row,
        escrow_amount_row=escrow_amount_row,
        notes_row=notes_row,
    )
    return _HR(content=html)


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slug: str | None = None
    parent_id: int | None = None
    icon: str | None = None
    sort_order: int = 0


@router.get("/catalog-categories", tags=["marketplace"])
def list_categories(
    parent_id: int | None = None,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """List all categories or children of a specific category."""
    try:
        return get_warehouse_service().list_catalog_categories(parent_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/catalog-categories", status_code=201, response_model=dict, tags=["admin"])
def create_catalog_category_endpoint(
    body: CategoryCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Create a new catalog category (admin only)."""
    require_permission(actor_ctx, Permission.CATALOG_WRITE)
    try:
        return get_warehouse_service().create_catalog_category(
            body.model_dump(exclude_none=True), actor_ctx.actor_id
        )
    except Exception as error:
        raise map_error(error) from error


class PriceTierItem(BaseModel):
    min_quantity: float = Field(gt=0)
    unit_price: float = Field(gt=0)
    label: str | None = None


class PriceTiersBody(BaseModel):
    tiers: list[PriceTierItem]


@router.get("/supplier/catalog/{item_id}/price-tiers", tags=["supplier-self"])
def get_price_tiers(
    item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().get_price_tiers(item_id)
    except Exception as error:
        raise map_error(error) from error


@router.put("/supplier/catalog/{item_id}/price-tiers", tags=["supplier-self"])
def set_price_tiers(
    item_id: int,
    body: PriceTiersBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Replace all price tiers for a catalog item. Send empty list to clear tiers."""
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        return get_warehouse_service().set_price_tiers(
            item_id, actor_ctx.supplier_id,
            [t.model_dump() for t in body.tiers]
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/catalog/{item_id}/price-tiers", tags=["marketplace"])
def get_public_price_tiers(
    item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Public endpoint: price tiers for a catalog item (visible to buyers)."""
    try:
        return get_warehouse_service().get_price_tiers(item_id)
    except Exception as error:
        raise map_error(error) from error


@router.get("/marketplace/compare", tags=["marketplace"])
def compare_catalog_items(
    ids: str,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Compare up to 6 catalog items side-by-side. Pass ids as comma-separated: ?ids=1,2,3"""
    try:
        id_list = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]
        if not id_list:
            raise HTTPException(status_code=422, detail={"code": "validation_error", "message": "ids must be comma-separated integers", "details": {}})
        return get_warehouse_service().compare_catalog_items(id_list)
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


# ── Service marketplace (repair/cleaning/logistics/consulting) ─────────────────

class ServiceCatalogCreate(BaseModel):
    type: str = Field(default="service", pattern="^(product|service)$")
    title: str = Field(min_length=1, max_length=240)
    description: str | None = Field(default=None, max_length=4000)
    price: Decimal | None = Field(default=None, ge=0)
    price_type: str = Field(default="negotiable", pattern="^(fixed|hourly|negotiable)$")
    unit: str | None = Field(default=None, max_length=64)
    service_category: str | None = Field(default=None, pattern="^(repair|cleaning|logistics|consulting|)$")


class ServiceCatalogUpdate(ServiceCatalogCreate):
    pass


@router.get("/supplier/services", tags=["supplier-self"])
def list_my_services(
    type: str | None = None,
    limit: int = 100,
    offset: int = 0,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        safe_limit = max(1, min(limit, 500))
        safe_offset = max(0, offset)
        return {
            "items": svc.list_service_catalog(actor_ctx.supplier_id, type, safe_limit, safe_offset),
            "total": svc.count_service_catalog(actor_ctx.supplier_id, type),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


@router.post("/supplier/services", status_code=201, tags=["supplier-self"])
def create_service_item(
    body: ServiceCatalogCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        return svc.create_service_catalog_item(actor_ctx.supplier_id, actor_ctx.actor_id, body.model_dump())
    except Exception as error:
        raise map_error(error) from error


@router.patch("/supplier/services/{item_id}", tags=["supplier-self"])
def update_service_item(
    item_id: int,
    body: ServiceCatalogUpdate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        result = svc.update_service_catalog_item(item_id, actor_ctx.supplier_id, body.model_dump())
        if result is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found or not yours", "details": {}})
        return result
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.delete("/supplier/services/{item_id}", status_code=204, tags=["supplier-self"])
def delete_service_item(
    item_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> None:
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    try:
        svc = get_warehouse_service()
        ok = svc.delete_service_catalog_item(item_id, actor_ctx.supplier_id)
        if not ok:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found or not yours", "details": {}})
    except HTTPException:
        raise
    except Exception as error:
        raise map_error(error) from error


@router.post("/supplier/services/{item_id}/image", tags=["supplier-self"])
async def upload_service_item_image(
    item_id: int,
    file: UploadFile,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    import urllib.request as _urllib, json as _json
    if actor_ctx.supplier_id is None:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": "No supplier linked", "details": {}})
    settings = get_settings()
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        raise HTTPException(
            status_code=503,
            detail={"code": "not_configured", "message": "Image upload not configured", "details": {}},
        )
    try:
        content = await file.read()
        filename = file.filename or "photo.jpg"
        boundary = b"----FormBoundary"
        body = (
            b"--" + boundary + b"\r\n"
            b'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
            + settings.telegram_chat_id.encode() + b"\r\n"
            b"--" + boundary + b"\r\n"
            b'Content-Disposition: form-data; name="photo"; filename="' + filename.encode() + b'"\r\n'
            b"Content-Type: " + (file.content_type or "image/jpeg").encode() + b"\r\n\r\n"
            + content + b"\r\n"
            b"--" + boundary + b"--\r\n"
        )
        req = _urllib.Request(
            f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendPhoto",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode()}"},
            method="POST",
        )
        with _urllib.urlopen(req, timeout=30) as resp:
            tg_data = _json.loads(resp.read())
        if not tg_data.get("ok"):
            raise HTTPException(
                status_code=502,
                detail={"code": "upload_failed", "message": "Telegram upload failed", "details": tg_data},
            )
        photos = tg_data["result"]["photo"]
        file_id = max(photos, key=lambda p: p.get("file_size", 0))["file_id"]
        svc = get_warehouse_service()
        result = svc.set_service_catalog_item_image(item_id, actor_ctx.supplier_id, file_id)
        if result is None:
            raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Item not found or not yours", "details": {}})
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise map_error(exc) from exc


@router.get("/services/{item_id}/image")
def get_service_item_image(item_id: int) -> Any:
    import urllib.request as _urllib, json as _json
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise HTTPException(status_code=404, detail="Not found")
    try:
        svc = get_warehouse_service()
        connection = svc.database.connect()
        try:
            row = connection.execute(
                "SELECT image_file_id FROM supplier_catalog WHERE id = ? AND is_active = 1",
                (item_id,),
            ).fetchone()
        finally:
            svc._close_connection(connection)
        if not row or not row["image_file_id"]:
            raise HTTPException(status_code=404, detail="No image")
        file_id = row["image_file_id"]
        req = _urllib.Request(
            f"https://api.telegram.org/bot{settings.telegram_bot_token}/getFile?file_id={file_id}"
        )
        with _urllib.urlopen(req, timeout=10) as resp:
            info = _json.loads(resp.read())
        file_path = info["result"]["file_path"]
        img_url = f"https://api.telegram.org/file/bot{settings.telegram_bot_token}/{file_path}"
        with _urllib.urlopen(img_url, timeout=30) as img_resp:
            content = img_resp.read()
            content_type = img_resp.headers.get("Content-Type", "image/jpeg")
        return Response(content=content, media_type=content_type, headers={"Cache-Control": "public, max-age=3600"})
    except HTTPException:
        raise
    except Exception as exc:
        raise map_error(exc) from exc


@router.get("/marketplace/services")
def list_service_marketplace_endpoint(
    type: str | None = None,
    service_category: str | None = None,
    supplier_id: int | None = None,
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> Any:
    try:
        svc = get_warehouse_service()
        safe_limit = max(1, min(limit, 200))
        safe_offset = max(0, offset)
        return {
            "items": svc.list_service_marketplace(type, service_category, supplier_id, q, safe_limit, safe_offset),
            "total": svc.count_service_marketplace(type, service_category, supplier_id, q),
            "limit": safe_limit,
            "offset": safe_offset,
        }
    except Exception as error:
        raise map_error(error) from error


# ── Gov procurement cycle ────────────────────────────────────────────────────

@router.post("/purchase-requests/{request_id}/gov-advance", tags=["purchase-requests"])
def advance_gov_status(
    request_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Advance gov procurement status: demand → accepting → closed."""
    try:
        return get_warehouse_service().advance_gov_status(request_id, actor_ctx.actor_id)
    except Exception as error:
        raise map_error(error) from error


@router.post("/purchase-requests/{request_id}/gov-feedback", tags=["purchase-requests"])
def add_gov_feedback(
    request_id: int,
    body: GovFeedbackBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Add gov procurement feedback (rating + text) — allowed when status is closed."""
    try:
        return get_warehouse_service().add_gov_feedback(
            request_id, body.feedback_text, body.rating, actor_ctx.actor_id
        )
    except Exception as error:
        raise map_error(error) from error


# ── Purchase Order escrow + delivery ─────────────────────────────────────────

@router.post("/marketplace/my-inquiries/{inquiry_id}/purchase-order/escrow", tags=["marketplace"])
def po_escrow_action(
    inquiry_id: int,
    body: EscrowActionBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Reserve / release / refund escrow for a Purchase Order."""
    try:
        return get_warehouse_service().update_po_escrow(
            inquiry_id, body.action, actor_ctx.actor_id
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


@router.patch("/marketplace/my-inquiries/{inquiry_id}/purchase-order/delivery", tags=["marketplace"])
def update_po_delivery(
    inquiry_id: int,
    body: DeliveryUpdateBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Update delivery status / tracking for a Purchase Order."""
    try:
        return get_warehouse_service().update_po_delivery(
            inquiry_id, body.model_dump(exclude_none=True), actor_ctx.actor_id
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error


# ── Auction escrow ────────────────────────────────────────────────────────────

@router.post("/marketplace/auctions/{auction_id}/escrow", tags=["marketplace"])
def auction_escrow_action(
    auction_id: int,
    body: EscrowActionBody,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    """Reserve / release / refund escrow for a Dutch auction win."""
    try:
        return get_warehouse_service().update_auction_escrow(
            auction_id, body.action, actor_ctx.actor_id
        )
    except PermissionError as error:
        raise HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}}) from error
    except Exception as error:
        raise map_error(error) from error
