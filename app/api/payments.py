"""Marketplace payments API — card payments and installment ("рассрочка").

Mounted alongside the main router under /api/v1. The sandbox endpoints render a
minimal gateway page so the redirect + return flow works without a real acquirer.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field

from app.api.dependencies import get_actor_context, get_warehouse_service
from app.domain.errors import NotFoundError, ValidationError
from app.security.rbac import ActorContext
from app.services.payments import PaymentService, installment_options

payment_router = APIRouter(prefix="/api/v1", tags=["payments"])


def _service() -> PaymentService:
    return PaymentService(get_warehouse_service().database)


def _map(error: Exception) -> HTTPException:
    if isinstance(error, ValidationError):
        return HTTPException(status_code=422, detail={"code": "validation_error", "message": str(error), "details": {}})
    if isinstance(error, NotFoundError):
        return HTTPException(status_code=404, detail={"code": "not_found", "message": str(error), "details": {}})
    if isinstance(error, PermissionError):
        return HTTPException(status_code=403, detail={"code": "forbidden", "message": str(error), "details": {}})
    return HTTPException(status_code=500, detail={"code": "internal_error", "message": str(error), "details": {}})


class PaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    method: str = Field(default="card", pattern="^(card|installment|wallet|invoice)$")
    installment_months: int = Field(default=0, ge=0)
    inquiry_ids: list[int] | None = None
    return_url: str | None = None
    description: str | None = None


@payment_router.get("/marketplace/payments/installment-options", tags=["payments"])
def get_installment_options(amount: float = Query(gt=0)) -> Any:
    """Public: available installment plans with monthly figures for an amount."""
    return {"amount": amount, "plans": installment_options(amount)}


@payment_router.post("/marketplace/payments", status_code=201, tags=["payments"])
def create_payment(
    body: PaymentCreate,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        payment = _service().create_payment(
            actor_id=actor_ctx.actor_id,
            amount=body.amount,
            method=body.method,
            installment_months=body.installment_months,
            inquiry_ids=body.inquiry_ids,
            return_url=body.return_url,
            description=body.description or "Оплата заказа marqet.kz",
        )
        return payment
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.get("/marketplace/payments", tags=["payments"])
def list_my_payments(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return {"items": _service().list_payments(actor_ctx.actor_id)}
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.get("/marketplace/payments/{payment_id}", tags=["payments"])
def get_payment(
    payment_id: int,
    actor_ctx: ActorContext = Depends(get_actor_context),
) -> Any:
    try:
        return _service().get_payment(payment_id, actor_id=actor_ctx.actor_id)
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


# ── Sandbox gateway (emulated redirect flow) ─────────────────────────────────
@payment_router.get("/marketplace/payments/sandbox/{payment_id}", include_in_schema=False)
def sandbox_page(payment_id: int) -> Any:
    try:
        payment = _service().get_payment(payment_id)
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error
    total = payment["total_amount"]
    months = payment["installment_months"]
    term = f"<p>Рассрочка на {months} мес.</p>" if months else ""
    already = payment["status"] in ("paid", "refunded")
    body = "<p style='color:#16a34a;font-weight:700'>Платёж уже оплачен ✓</p>" if already else f"""
      <form method="post" action="/api/v1/marketplace/payments/sandbox/{payment_id}/confirm?result=success">
        <button type="submit" style="background:#5B4FE8;color:#fff;border:0;border-radius:12px;padding:14px 22px;font-size:15px;font-weight:800;cursor:pointer;width:100%">Оплатить {total} ₸</button>
      </form>
      <form method="post" action="/api/v1/marketplace/payments/sandbox/{payment_id}/confirm?result=fail" style="margin-top:10px">
        <button type="submit" style="background:#F1F5F9;color:#475569;border:0;border-radius:12px;padding:12px 22px;font-size:14px;font-weight:700;cursor:pointer;width:100%">Отменить</button>
      </form>"""
    html = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Оплата marqet.kz (sandbox)</title></head>
    <body style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#F5F5FA;margin:0;padding:40px 16px">
      <div style="max-width:420px;margin:0 auto;background:#fff;border:1px solid #E2E8F0;border-radius:16px;padding:26px">
        <div style="font-weight:900;font-size:18px;color:#1E1B4B;margin-bottom:4px">marqet.kz · тестовая оплата</div>
        <div style="display:inline-block;background:#FEF3C7;color:#92400E;font-size:11px;font-weight:800;padding:3px 8px;border-radius:6px;margin-bottom:16px">SANDBOX — деньги не списываются</div>
        <p style="color:#64748B;font-size:14px;margin:0 0 4px">Платёж #{payment_id}</p>
        <p style="font-size:26px;font-weight:900;color:#1E1B4B;margin:0 0 4px">{total} ₸</p>
        {term}
        <div style="margin-top:18px">{body}</div>
      </div>
    </body></html>"""
    return HTMLResponse(content=html)


@payment_router.post("/marketplace/payments/sandbox/{payment_id}/confirm", include_in_schema=False)
def sandbox_confirm(payment_id: int, result: str = Query(default="success")) -> Any:
    svc = _service()
    try:
        payment = svc.confirm_sandbox(payment_id, success=(result == "success"))
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error
    return_url = payment.get("return_url")
    if return_url:
        sep = "&" if "?" in return_url else "?"
        target = f"{return_url}{sep}paid={'1' if payment['status'] == 'paid' else '0'}&payment_id={payment_id}"
        return RedirectResponse(url=target, status_code=303)
    return payment


@payment_router.post("/marketplace/payments/webhook/{provider}", include_in_schema=False)
async def payment_webhook(provider: str, request: Request) -> Any:
    raw = await request.body()
    headers = {k.lower(): v for k, v in request.headers.items()}
    try:
        return _service().handle_webhook(headers, raw)
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error
