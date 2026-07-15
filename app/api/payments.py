"""Marketplace payments API — card payments and installment ("рассрочка").

Mounted alongside the main router under /api/v1. The sandbox endpoints render a
minimal gateway page so the redirect + return flow works without a real acquirer.
"""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
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
    payment_method_id: int | None = None


class BindCard(BaseModel):
    return_url: str | None = None


class PayoutCreate(BaseModel):
    payment_id: int


def _supplier_id(actor_ctx: ActorContext) -> int:
    if actor_ctx.supplier_id is None:
        raise HTTPException(
            status_code=403,
            detail={"code": "forbidden", "message": "Профиль продавца не привязан", "details": {}},
        )
    return int(actor_ctx.supplier_id)


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
            payment_method_id=body.payment_method_id,
        )
        return payment
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


# ── Buyer saved cards ────────────────────────────────────────────────────────
@payment_router.get("/marketplace/cards", tags=["payments"])
def list_cards(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return {"items": _service().list_cards(actor_ctx.actor_id)}
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.post("/marketplace/cards/bind", status_code=201, tags=["payments"])
def bind_card(body: BindCard, actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    """Start card tokenization. Returns a redirect_url to the acquirer's secure page."""
    try:
        return _service().start_card_binding(actor_ctx.actor_id, body.return_url)
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.patch("/marketplace/cards/{method_id}/default", tags=["payments"])
def set_default_card(method_id: int, actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return _service().set_default_card(method_id, actor_ctx.actor_id)
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.delete("/marketplace/cards/{method_id}", tags=["payments"])
def remove_card(method_id: int, actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return _service().remove_card(method_id, actor_ctx.actor_id)
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


# ── Supplier payout accounts ─────────────────────────────────────────────────
@payment_router.get("/supplier/payout-accounts", tags=["payments"])
def list_payout_accounts(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return {"items": _service().list_payout_accounts(_supplier_id(actor_ctx))}
    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.post("/supplier/payout-accounts/bind", status_code=201, tags=["payments"])
def bind_payout_account(body: BindCard, actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    """Start tokenizing the seller's card for receiving payouts."""
    try:
        return _service().start_payout_binding(_supplier_id(actor_ctx), body.return_url)
    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.patch("/supplier/payout-accounts/{account_id}/default", tags=["payments"])
def set_default_payout_account(account_id: int, actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return _service().set_default_payout_account(account_id, _supplier_id(actor_ctx))
    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.delete("/supplier/payout-accounts/{account_id}", tags=["payments"])
def remove_payout_account(account_id: int, actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return _service().remove_payout_account(account_id, _supplier_id(actor_ctx))
    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


# ── Payouts ──────────────────────────────────────────────────────────────────
@payment_router.get("/supplier/payouts", tags=["payments"])
def list_payouts(actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    try:
        return {"items": _service().list_payouts(_supplier_id(actor_ctx))}
    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error


@payment_router.post("/supplier/payouts", status_code=201, tags=["payments"])
def create_payout(body: PayoutCreate, actor_ctx: ActorContext = Depends(get_actor_context)) -> Any:
    """Send the seller's proceeds for a paid order to their default payout card."""
    try:
        return _service().create_payout(_supplier_id(actor_ctx), body.payment_id)
    except HTTPException:
        raise
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


# ── Sandbox card-binding form ────────────────────────────────────────────────
# Stand-in for the acquirer's hosted widget (ePay / Stripe Elements): served from
# the gateway route and embedded as an iframe, so the PAN never enters the SPA.
_BIND_FORM_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:transparent;color:#1E293B;padding:2px}
.f{display:flex;flex-direction:column;gap:10px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.inp{width:100%;border:1.5px solid #E2E8F0;border-radius:12px;padding:14px 13px;font-size:15px;font-family:inherit;color:#1E293B;background:#fff;outline:none;transition:border-color .16s,box-shadow .16s}
.inp:focus{border-color:#5B4FE8;box-shadow:0 0 0 3px rgba(91,79,232,.12)}
.inp::placeholder{color:#94A3B8}
.lbl{font-size:12px;font-weight:800;color:#475569;margin:8px 0 -2px}
.pan-wrap{position:relative}
.brands{position:absolute;right:12px;top:50%;transform:translateY(-50%);display:flex;gap:4px;font-size:10px;font-weight:900;color:#94A3B8;letter-spacing:.02em}
.btn{width:100%;min-height:50px;border:0;border-radius:12px;color:#fff;background:linear-gradient(135deg,#5B4FE8 0%,#3B82F6 100%);font-size:15px;font-weight:900;font-family:inherit;cursor:pointer;margin-top:6px}
.btn:disabled{opacity:.55;cursor:not-allowed}
.err{background:#FEF2F2;border:1px solid #FECACA;color:#DC2626;border-radius:10px;padding:11px 13px;font-size:13px;line-height:1.45}
.note{display:flex;gap:7px;align-items:flex-start;color:#64748B;font-size:11px;line-height:1.5;margin-top:4px}
.sbx{background:#FEF3C7;color:#92400E;font-size:11px;font-weight:800;padding:6px 10px;border-radius:8px;line-height:1.45}
"""


def _bind_form_html(kind: str, record_id: int, error: str | None = None) -> str:
    cta = "Сохранить карту" if kind == "method" else "Сохранить реквизиты"
    err = f'<div class="err">{error}</div>' if error else ""
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Добавить способ оплаты</title><style>{_BIND_FORM_CSS}</style></head><body>
<form class="f" method="post" action="/api/v1/marketplace/cards/sandbox/{kind}/{record_id}/confirm" autocomplete="off">
  <div class="sbx">🔒 Тестовый шлюз. Введите <b>4242 4242 4242 4242</b>, любой будущий срок и любой CVC. Настоящую карту вводить не нужно — она будет отклонена.</div>
  {err}
  <div class="lbl">Номер карты</div>
  <div class="pan-wrap">
    <input class="inp" name="pan" inputmode="numeric" placeholder="1234 1234 1234 1234" maxlength="23" required
           oninput="this.value=this.value.replace(/\\D/g,'').replace(/(.{{4}})/g,'$1 ').trim()">
    <div class="brands"><span>VISA</span><span>MC</span></div>
  </div>
  <div class="row">
    <div>
      <div class="lbl">Срок действия</div>
      <input class="inp" name="exp" inputmode="numeric" placeholder="ММ / ГГ" maxlength="7" required
             oninput="let v=this.value.replace(/\\D/g,'').slice(0,4);this.value=v.length>2?v.slice(0,2)+' / '+v.slice(2):v">
    </div>
    <div>
      <div class="lbl">Код безопасности</div>
      <input class="inp" name="cvc" inputmode="numeric" placeholder="CVC" maxlength="4" required
             oninput="this.value=this.value.replace(/\\D/g,'')">
    </div>
  </div>
  <div class="lbl">Имя владельца</div>
  <input class="inp" name="holder_name" placeholder="IVAN IVANOV" autocomplete="off">
  <button class="btn" type="submit">{cta}</button>
  <div class="note">
    <span>🔒</span>
    <span>Данные карты обрабатывает платёжный шлюз. marqet.kz сохраняет только тип карты и последние 4 цифры — номер и CVC к нам не попадают.</span>
  </div>
</form></body></html>"""


@payment_router.get("/marketplace/cards/sandbox/{kind}/{record_id}", include_in_schema=False)
def sandbox_bind_page(kind: str, record_id: int) -> Any:
    if kind not in ("method", "payout"):
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Unknown binding kind", "details": {}})
    return HTMLResponse(content=_bind_form_html(kind, record_id))


@payment_router.post("/marketplace/cards/sandbox/{kind}/{record_id}/confirm", include_in_schema=False)
def sandbox_bind_confirm(
    kind: str,
    record_id: int,
    pan: str = Form(default=""),
    exp: str = Form(default=""),
    cvc: str = Form(default=""),
    holder_name: str = Form(default=""),
) -> Any:
    if kind not in ("method", "payout"):
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Unknown binding kind", "details": {}})
    digits = "".join(c for c in exp if c.isdigit())
    exp_month = int(digits[:2]) if len(digits) >= 2 else 0
    exp_year = 2000 + int(digits[2:4]) if len(digits) >= 4 else 0
    card = {
        "pan": pan,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvc": cvc,
        "holder_name": holder_name.strip() or None,
    }
    svc = _service()
    try:
        if kind == "method":
            record = svc.finalize_card_binding(record_id, **card)
        else:
            record = svc.finalize_payout_binding(record_id, **card)
    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error

    if record.get("status") != "active":
        # Re-render the form with the gateway's reason; the row stays retryable.
        reason = record.get("failure_reason") or "Не удалось привязать карту"
        return HTMLResponse(content=_bind_form_html(kind, record_id, error=reason), status_code=200)

    # Notify the embedding SPA (iframe), or fall back to a redirect.
    return_url = record.get("return_url")
    fallback = ""
    if return_url:
        sep = "&" if "?" in return_url else "?"
        fallback = f"if(window.top===window.self){{location.href={json.dumps(f'{return_url}{sep}card_added=1')}}}"
    html = f"""<!doctype html><html><head><meta charset="utf-8"></head><body>
<script>
  try {{ window.parent.postMessage({{type:'marqet:card-bound', status:'active', kind:{json.dumps(kind)}}}, '*'); }} catch(e) {{}}
  {fallback}
</script></body></html>"""
    return HTMLResponse(content=html)


@payment_router.post("/marketplace/payments/webhook/{provider}", include_in_schema=False)
async def payment_webhook(provider: str, request: Request) -> Any:
    raw = await request.body()
    headers = {k.lower(): v for k, v in request.headers.items()}
    try:
        return _service().handle_webhook(headers, raw)
    except Exception as error:  # noqa: BLE001
        raise _map(error) from error
