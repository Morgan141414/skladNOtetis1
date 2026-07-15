"""Marketplace payments & installment ("рассрочка") service.

Provider-agnostic payment layer for marqet.kz. The default provider is a
built-in ``sandbox`` gateway that emulates the full redirect + webhook flow so
the checkout works end-to-end without any external acquirer. A real Kazakhstan
acquirer (Halyk ePay / Kaspi) plugs in by implementing :class:`PaymentProvider`
and setting ``MARQET_PAYMENT_PROVIDER`` + credentials in the environment.

Money handling stays on the platform only as a *ledger*: the actual card data
never touches this service — the buyer enters it on the gateway's own page.
"""

from __future__ import annotations

import json
import math
import os
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Protocol

from app.domain.errors import NotFoundError, ValidationError
from app.storage.sqlite import insert_and_get_id, now_iso


# ── Installment plans ────────────────────────────────────────────────────────
# markup = share added to the price for that term (buyer-facing overpayment).
# 3 and 6 months are interest-free (merchant absorbs the commission, Kaspi-Red
# style); 12 months carries a markup. Tune here without touching the flow.
INSTALLMENT_PLANS: dict[int, float] = {3: 0.0, 6: 0.0, 12: 0.10}
MIN_INSTALLMENT_AMOUNT = Decimal("6000")  # ₸ — below this installments make no sense


def _q(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def installment_options(amount: float | Decimal | str) -> list[dict[str, Any]]:
    """Return the available installment plans with monthly figures for ``amount``."""
    base = Decimal(str(amount))
    out: list[dict[str, Any]] = []
    if base < MIN_INSTALLMENT_AMOUNT:
        return out
    for months, markup in sorted(INSTALLMENT_PLANS.items()):
        total = _q(base * (Decimal(1) + Decimal(str(markup))))
        monthly = _q(Decimal(math.ceil(total / months)))
        out.append(
            {
                "months": months,
                "markup_percent": round(markup * 100, 2),
                "total": float(total),
                "monthly": float(monthly),
                "interest_free": markup == 0.0,
            }
        )
    return out


def compute_total(amount: float | Decimal | str, method: str, installment_months: int) -> tuple[Decimal, Decimal]:
    """Return (total_amount, markup_amount) for a given method/term."""
    base = Decimal(str(amount))
    if method == "installment" and installment_months:
        if installment_months not in INSTALLMENT_PLANS:
            raise ValidationError(f"Недоступный срок рассрочки: {installment_months}")
        if base < MIN_INSTALLMENT_AMOUNT:
            raise ValidationError("Сумма слишком мала для рассрочки")
        markup = Decimal(str(INSTALLMENT_PLANS[installment_months]))
        total = _q(base * (Decimal(1) + markup))
        return total, _q(total - base)
    return _q(base), Decimal("0.00")


# ── Provider abstraction ─────────────────────────────────────────────────────
class PaymentProvider(Protocol):
    name: str

    def create(
        self, *, payment_id: int, amount: Decimal, currency: str, description: str, return_url: str | None
    ) -> dict[str, Any]:
        """Register the payment with the gateway. Returns provider_ref + redirect_url."""

    def verify_webhook(self, headers: dict[str, str], raw_body: bytes) -> dict[str, Any]:
        """Validate a gateway callback. Returns {provider_ref, status, failure_reason?}."""


class SandboxProvider:
    """Built-in gateway emulation. Redirects to an on-server confirmation page."""

    name = "sandbox"

    def create(self, *, payment_id, amount, currency, description, return_url) -> dict[str, Any]:
        return {
            "provider_ref": f"sbx_{payment_id}",
            "redirect_url": f"/api/v1/marketplace/payments/sandbox/{payment_id}",
            "status": "pending",
        }

    def verify_webhook(self, headers, raw_body) -> dict[str, Any]:
        data = json.loads(raw_body or b"{}")
        return {
            "provider_ref": data.get("provider_ref"),
            "status": data.get("status", "failed"),
            "failure_reason": data.get("failure_reason"),
        }


class HalykEpayProvider:
    """Adapter skeleton for Halyk Bank ePay (KZ card acquiring + installments).

    Configure via env: MARQET_EPAY_TERMINAL, MARQET_EPAY_CLIENT_ID,
    MARQET_EPAY_CLIENT_SECRET, MARQET_EPAY_BASE_URL. Left as a stub because the
    live terminal requires a signed merchant contract that cannot be
    self-provisioned; the create/verify contract matches ePay's OAuth + invoice
    API so wiring real keys is the only remaining step.
    """

    name = "epay"

    def __init__(self) -> None:
        self.terminal = os.getenv("MARQET_EPAY_TERMINAL")
        self.client_id = os.getenv("MARQET_EPAY_CLIENT_ID")
        self.client_secret = os.getenv("MARQET_EPAY_CLIENT_SECRET")
        self.base_url = os.getenv("MARQET_EPAY_BASE_URL", "https://epay-api.homebank.kz")

    def _require_config(self) -> None:
        if not (self.terminal and self.client_id and self.client_secret):
            raise ValidationError(
                "Платёжный провайдер ePay не настроен: задайте MARQET_EPAY_* в окружении"
            )

    def create(self, *, payment_id, amount, currency, description, return_url) -> dict[str, Any]:
        self._require_config()
        raise ValidationError("ePay live integration pending merchant credentials")

    def verify_webhook(self, headers, raw_body) -> dict[str, Any]:
        self._require_config()
        raise ValidationError("ePay live integration pending merchant credentials")


def get_provider() -> PaymentProvider:
    name = os.getenv("MARQET_PAYMENT_PROVIDER", "sandbox").strip().lower()
    if name == "epay":
        return HalykEpayProvider()
    return SandboxProvider()


# ── Service ──────────────────────────────────────────────────────────────────
class PaymentService:
    def __init__(self, database: Any) -> None:
        self.database = database
        self.provider = get_provider()

    def create_payment(
        self,
        *,
        actor_id: str,
        amount: float | str,
        method: str,
        installment_months: int = 0,
        inquiry_ids: list[int] | None = None,
        return_url: str | None = None,
        description: str = "Оплата заказа marqet.kz",
    ) -> dict[str, Any]:
        if method not in {"card", "installment", "wallet", "invoice"}:
            raise ValidationError(f"Неизвестный способ оплаты: {method}")
        base = Decimal(str(amount))
        if base <= 0:
            raise ValidationError("Сумма оплаты должна быть больше нуля")
        if method != "installment":
            installment_months = 0
        total, markup = compute_total(base, method, installment_months)
        ids_csv = ",".join(str(i) for i in (inquiry_ids or []))

        with self.database.transaction() as conn:
            payment_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_payments
                   (actor_id, inquiry_ids, amount, currency, method, installment_months,
                    markup_amount, total_amount, provider, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')""",
                (
                    actor_id,
                    ids_csv or None,
                    str(_q(base)),
                    "KZT",
                    method,
                    installment_months,
                    str(markup),
                    str(total),
                    self.provider.name,
                ),
            )

        reg = self.provider.create(
            payment_id=payment_id,
            amount=total,
            currency="KZT",
            description=description,
            return_url=return_url,
        )
        with self.database.transaction() as conn:
            conn.execute(
                """UPDATE marketplace_payments
                   SET provider_ref = ?, redirect_url = ?, return_url = ?,
                       status = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    reg.get("provider_ref"),
                    reg.get("redirect_url"),
                    return_url,
                    reg.get("status", "pending"),
                    now_iso(),
                    payment_id,
                ),
            )
        return self.get_payment(payment_id, actor_id=actor_id)

    def get_payment(self, payment_id: int, actor_id: str | None = None) -> dict[str, Any]:
        conn = self.database.connect()
        try:
            row = conn.execute(
                "SELECT * FROM marketplace_payments WHERE id = ?", (payment_id,)
            ).fetchone()
        finally:
            try:
                conn.close()
            except Exception:
                pass
        if row is None:
            raise NotFoundError("Платёж не найден")
        data = dict(row)
        if actor_id is not None and data.get("actor_id") != actor_id:
            raise PermissionError("Это не ваш платёж")
        return data

    def list_payments(self, actor_id: str, limit: int = 50) -> list[dict[str, Any]]:
        conn = self.database.connect()
        try:
            rows = conn.execute(
                "SELECT * FROM marketplace_payments WHERE actor_id = ? ORDER BY id DESC LIMIT ?",
                (actor_id, limit),
            ).fetchall()
        finally:
            try:
                conn.close()
            except Exception:
                pass
        return [dict(r) for r in rows]

    def _set_status(self, provider_ref: str, status: str, failure_reason: str | None = None) -> dict[str, Any]:
        with self.database.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM marketplace_payments WHERE provider_ref = ?", (provider_ref,)
            ).fetchone()
            if row is None:
                raise NotFoundError("Платёж не найден по provider_ref")
            payment = dict(row)
            if payment["status"] in {"paid", "refunded"}:
                return payment  # idempotent — do not re-process a settled payment
            paid_at = now_iso() if status == "paid" else None
            conn.execute(
                """UPDATE marketplace_payments
                   SET status = ?, failure_reason = ?, paid_at = COALESCE(?, paid_at), updated_at = ?
                   WHERE id = ?""",
                (status, failure_reason, paid_at, now_iso(), payment["id"]),
            )
        if status == "paid":
            self._on_paid(payment)
        return self.get_payment(payment["id"])

    def _on_paid(self, payment: dict[str, Any]) -> None:
        """Best-effort: mark escrow held on any purchase orders behind the paid inquiries."""
        ids_csv = payment.get("inquiry_ids")
        if not ids_csv:
            return
        try:
            inquiry_ids = [int(x) for x in str(ids_csv).split(",") if x.strip()]
        except ValueError:
            return
        for inq_id in inquiry_ids:
            try:
                with self.database.transaction() as conn:
                    conn.execute(
                        """UPDATE purchase_orders
                           SET escrow_status = 'held', escrow_reserved_at = ?
                           WHERE inquiry_id = ? AND escrow_status IN ('none', 'reserved')""",
                        (now_iso(), inq_id),
                    )
            except Exception:
                continue

    def confirm_sandbox(self, payment_id: int, success: bool) -> dict[str, Any]:
        payment = self.get_payment(payment_id)
        if payment["provider"] != "sandbox":
            raise ValidationError("Подтверждение доступно только для sandbox-платежа")
        status = "paid" if success else "failed"
        reason = None if success else "Отменено покупателем в sandbox"
        return self._set_status(payment["provider_ref"], status, reason)

    def handle_webhook(self, headers: dict[str, str], raw_body: bytes) -> dict[str, Any]:
        result = self.provider.verify_webhook(headers, raw_body)
        provider_ref = result.get("provider_ref")
        if not provider_ref:
            raise ValidationError("В callback отсутствует provider_ref")
        return self._set_status(provider_ref, result.get("status", "failed"), result.get("failure_reason"))
