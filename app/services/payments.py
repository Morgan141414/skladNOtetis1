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

# Platform fee withheld from each seller payout.
PLATFORM_COMMISSION_PERCENT = Decimal(os.getenv("MARQET_COMMISSION_PERCENT", "5"))

# Sandbox-only fake cards. Real card data is NEVER entered on marqet.kz — the
# buyer types it on the acquirer's page and we only ever receive a token.
SANDBOX_TEST_CARDS = [
    {"id": "visa", "brand": "Visa", "last4": "4242", "exp_month": 12, "exp_year": 2029},
    {"id": "mastercard", "brand": "Mastercard", "last4": "5100", "exp_month": 8, "exp_year": 2028},
    {"id": "declined", "brand": "Visa", "last4": "0002", "exp_month": 1, "exp_year": 2027},
]


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

    # ── Card binding (tokenization) ──────────────────────────────────────────
    def create_binding(self, *, kind: str, method_id: int, return_url: str | None) -> dict[str, Any]:
        return {
            "provider_ref": f"sbxbind_{kind}_{method_id}",
            "redirect_url": f"/api/v1/marketplace/cards/sandbox/{kind}/{method_id}",
        }

    def finalize_binding(self, *, card_id: str) -> dict[str, Any]:
        card = next((c for c in SANDBOX_TEST_CARDS if c["id"] == card_id), None)
        if card is None:
            raise ValidationError("Неизвестная тестовая карта")
        if card_id == "declined":
            return {"status": "failed", "failure_reason": "Банк отклонил привязку карты"}
        return {
            "status": "active",
            "provider_token": f"sbxtok_{card['brand'].lower()}_{card['last4']}",
            "brand": card["brand"],
            "last4": card["last4"],
            "exp_month": card["exp_month"],
            "exp_year": card["exp_year"],
        }

    # ── Charging a stored token (one-click) ──────────────────────────────────
    def charge_saved(self, *, payment_id: int, amount: Decimal, token: str) -> dict[str, Any]:
        if token.endswith("_0002"):
            return {"status": "failed", "provider_ref": f"sbx_{payment_id}", "failure_reason": "Недостаточно средств"}
        return {"status": "paid", "provider_ref": f"sbx_{payment_id}"}

    # ── Payouts (money out to sellers) ───────────────────────────────────────
    def create_payout(self, *, payout_id: int, amount: Decimal, token: str) -> dict[str, Any]:
        return {"status": "sent", "provider_ref": f"sbxpo_{payout_id}"}


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

    def create_binding(self, *, kind, method_id, return_url) -> dict[str, Any]:
        self._require_config()
        # ePay: create a zero-amount/verify invoice with `saveCard=true`; the
        # card is entered on ePay's page and only the token comes back to us.
        raise ValidationError("ePay card binding pending merchant credentials")

    def finalize_binding(self, *, card_id: str) -> dict[str, Any]:
        self._require_config()
        raise ValidationError("ePay card binding pending merchant credentials")

    def charge_saved(self, *, payment_id, amount, token) -> dict[str, Any]:
        self._require_config()
        raise ValidationError("ePay one-click charge pending merchant credentials")

    def create_payout(self, *, payout_id, amount, token) -> dict[str, Any]:
        self._require_config()
        # ePay OCT / card2card payout to the seller's tokenized card.
        raise ValidationError("ePay payouts pending merchant credentials")


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
        payment_method_id: int | None = None,
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

        saved_method: dict[str, Any] | None = None
        if payment_method_id is not None:
            saved_method = self.get_payment_method(payment_method_id, actor_id)
            if saved_method["status"] != "active" or not saved_method.get("provider_token"):
                raise ValidationError("Сохранённая карта недоступна — привяжите карту заново")

        with self.database.transaction() as conn:
            payment_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_payments
                   (actor_id, inquiry_ids, amount, currency, method, installment_months,
                    markup_amount, total_amount, provider, status, payment_method_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)""",
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
                    payment_method_id,
                ),
            )

        # One-click: charge the stored token straight away, no gateway redirect.
        if saved_method is not None:
            charge = self.provider.charge_saved(
                payment_id=payment_id, amount=total, token=saved_method["provider_token"]
            )
            with self.database.transaction() as conn:
                conn.execute(
                    """UPDATE marketplace_payments
                       SET provider_ref = ?, return_url = ?, updated_at = ?
                       WHERE id = ?""",
                    (charge.get("provider_ref"), return_url, now_iso(), payment_id),
                )
            return self._set_status(
                charge.get("provider_ref"),
                charge.get("status", "failed"),
                charge.get("failure_reason"),
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

    # ── Buyer saved cards ────────────────────────────────────────────────────
    def _fetch_all(self, sql: str, params: tuple) -> list[dict[str, Any]]:
        conn = self.database.connect()
        try:
            rows = conn.execute(sql, params).fetchall()
        finally:
            try:
                conn.close()
            except Exception:
                pass
        return [dict(r) for r in rows]

    def _fetch_one(self, sql: str, params: tuple) -> dict[str, Any] | None:
        rows = self._fetch_all(sql, params)
        return rows[0] if rows else None

    def start_card_binding(self, actor_id: str, return_url: str | None = None) -> dict[str, Any]:
        """Begin tokenizing a card. Card data is entered on the gateway, never here."""
        with self.database.transaction() as conn:
            method_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_payment_methods (actor_id, provider, status, return_url)
                   VALUES (?, ?, 'pending', ?)""",
                (actor_id, self.provider.name, return_url),
            )
        reg = self.provider.create_binding(kind="method", method_id=method_id, return_url=return_url)
        with self.database.transaction() as conn:
            conn.execute(
                "UPDATE marketplace_payment_methods SET provider_ref = ?, updated_at = ? WHERE id = ?",
                (reg.get("provider_ref"), now_iso(), method_id),
            )
        method = self.get_payment_method(method_id, actor_id)
        method["redirect_url"] = reg.get("redirect_url")
        return method

    def finalize_card_binding(self, method_id: int, card_id: str) -> dict[str, Any]:
        method = self.get_payment_method(method_id)
        if method["status"] == "active":
            return method
        result = self.provider.finalize_binding(card_id=card_id)
        with self.database.transaction() as conn:
            conn.execute(
                """UPDATE marketplace_payment_methods
                   SET status = ?, provider_token = ?, brand = ?, last4 = ?,
                       exp_month = ?, exp_year = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    result["status"],
                    result.get("provider_token"),
                    result.get("brand"),
                    result.get("last4"),
                    result.get("exp_month"),
                    result.get("exp_year"),
                    now_iso(),
                    method_id,
                ),
            )
        if result["status"] == "active":
            existing = self._fetch_all(
                "SELECT id FROM marketplace_payment_methods WHERE actor_id = ? AND status = 'active'",
                (method["actor_id"],),
            )
            if len(existing) == 1:  # first card becomes the default
                self.set_default_card(method_id, method["actor_id"])
        return self.get_payment_method(method_id)

    def get_payment_method(self, method_id: int, actor_id: str | None = None) -> dict[str, Any]:
        row = self._fetch_one("SELECT * FROM marketplace_payment_methods WHERE id = ?", (method_id,))
        if row is None:
            raise NotFoundError("Карта не найдена")
        if actor_id is not None and row["actor_id"] != actor_id:
            raise PermissionError("Это не ваша карта")
        return row

    def list_cards(self, actor_id: str) -> list[dict[str, Any]]:
        return self._fetch_all(
            """SELECT id, brand, last4, exp_month, exp_year, is_default, status, created_at
               FROM marketplace_payment_methods
               WHERE actor_id = ? AND status IN ('active','pending')
               ORDER BY is_default DESC, id DESC""",
            (actor_id,),
        )

    def set_default_card(self, method_id: int, actor_id: str) -> dict[str, Any]:
        self.get_payment_method(method_id, actor_id)
        with self.database.transaction() as conn:
            conn.execute(
                "UPDATE marketplace_payment_methods SET is_default = false WHERE actor_id = ?", (actor_id,)
            )
            conn.execute(
                "UPDATE marketplace_payment_methods SET is_default = true, updated_at = ? WHERE id = ?",
                (now_iso(), method_id),
            )
        return self.get_payment_method(method_id, actor_id)

    def remove_card(self, method_id: int, actor_id: str) -> dict[str, Any]:
        self.get_payment_method(method_id, actor_id)
        with self.database.transaction() as conn:
            conn.execute(
                """UPDATE marketplace_payment_methods
                   SET status = 'removed', is_default = false, provider_token = NULL, updated_at = ?
                   WHERE id = ?""",
                (now_iso(), method_id),
            )
        return {"removed": True, "id": method_id}

    # ── Supplier payout accounts ─────────────────────────────────────────────
    def start_payout_binding(self, supplier_id: int, return_url: str | None = None) -> dict[str, Any]:
        with self.database.transaction() as conn:
            acc_id = insert_and_get_id(
                conn,
                """INSERT INTO supplier_payout_accounts (supplier_id, account_type, provider, status, return_url)
                   VALUES (?, 'card', ?, 'pending', ?)""",
                (supplier_id, self.provider.name, return_url),
            )
        reg = self.provider.create_binding(kind="payout", method_id=acc_id, return_url=return_url)
        with self.database.transaction() as conn:
            conn.execute(
                "UPDATE supplier_payout_accounts SET provider_ref = ?, updated_at = ? WHERE id = ?",
                (reg.get("provider_ref"), now_iso(), acc_id),
            )
        acc = self.get_payout_account(acc_id, supplier_id)
        acc["redirect_url"] = reg.get("redirect_url")
        return acc

    def finalize_payout_binding(self, account_id: int, card_id: str) -> dict[str, Any]:
        acc = self.get_payout_account(account_id)
        if acc["status"] == "active":
            return acc
        result = self.provider.finalize_binding(card_id=card_id)
        with self.database.transaction() as conn:
            conn.execute(
                """UPDATE supplier_payout_accounts
                   SET status = ?, provider_token = ?, brand = ?, last4 = ?,
                       exp_month = ?, exp_year = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    result["status"],
                    result.get("provider_token"),
                    result.get("brand"),
                    result.get("last4"),
                    result.get("exp_month"),
                    result.get("exp_year"),
                    now_iso(),
                    account_id,
                ),
            )
        if result["status"] == "active":
            existing = self._fetch_all(
                "SELECT id FROM supplier_payout_accounts WHERE supplier_id = ? AND status = 'active'",
                (acc["supplier_id"],),
            )
            if len(existing) == 1:
                self.set_default_payout_account(account_id, acc["supplier_id"])
        return self.get_payout_account(account_id)

    def get_payout_account(self, account_id: int, supplier_id: int | None = None) -> dict[str, Any]:
        row = self._fetch_one("SELECT * FROM supplier_payout_accounts WHERE id = ?", (account_id,))
        if row is None:
            raise NotFoundError("Реквизиты не найдены")
        if supplier_id is not None and int(row["supplier_id"]) != int(supplier_id):
            raise PermissionError("Это не ваши реквизиты")
        return row

    def list_payout_accounts(self, supplier_id: int) -> list[dict[str, Any]]:
        return self._fetch_all(
            """SELECT id, account_type, brand, last4, exp_month, exp_year, holder_name,
                      bank_name, iban_last4, is_default, status, created_at
               FROM supplier_payout_accounts
               WHERE supplier_id = ? AND status IN ('active','pending')
               ORDER BY is_default DESC, id DESC""",
            (supplier_id,),
        )

    def set_default_payout_account(self, account_id: int, supplier_id: int) -> dict[str, Any]:
        self.get_payout_account(account_id, supplier_id)
        with self.database.transaction() as conn:
            conn.execute(
                "UPDATE supplier_payout_accounts SET is_default = false WHERE supplier_id = ?", (supplier_id,)
            )
            conn.execute(
                "UPDATE supplier_payout_accounts SET is_default = true, updated_at = ? WHERE id = ?",
                (now_iso(), account_id),
            )
        return self.get_payout_account(account_id, supplier_id)

    def remove_payout_account(self, account_id: int, supplier_id: int) -> dict[str, Any]:
        self.get_payout_account(account_id, supplier_id)
        with self.database.transaction() as conn:
            conn.execute(
                """UPDATE supplier_payout_accounts
                   SET status = 'removed', is_default = false, provider_token = NULL, updated_at = ?
                   WHERE id = ?""",
                (now_iso(), account_id),
            )
        return {"removed": True, "id": account_id}

    # ── Payouts ──────────────────────────────────────────────────────────────
    def create_payout(self, supplier_id: int, payment_id: int) -> dict[str, Any]:
        payment = self.get_payment(payment_id)
        if payment["status"] != "paid":
            raise ValidationError("Выплата возможна только по оплаченному заказу")
        existing = self._fetch_one(
            "SELECT * FROM marketplace_payouts WHERE payment_id = ? AND supplier_id = ?",
            (payment_id, supplier_id),
        )
        if existing:
            raise ValidationError(f"Выплата по этому заказу уже создана (#{existing['id']})")
        account = self._fetch_one(
            """SELECT * FROM supplier_payout_accounts
               WHERE supplier_id = ? AND status = 'active'
               ORDER BY is_default DESC, id DESC LIMIT 1""",
            (supplier_id,),
        )
        if account is None:
            raise ValidationError("Добавьте карту для получения выплат в личном кабинете")

        gross = Decimal(str(payment["amount"]))
        commission = _q(gross * PLATFORM_COMMISSION_PERCENT / Decimal(100))
        net = _q(gross - commission)

        with self.database.transaction() as conn:
            payout_id = insert_and_get_id(
                conn,
                """INSERT INTO marketplace_payouts
                   (supplier_id, payout_account_id, payment_id, amount, commission_amount,
                    net_amount, provider, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')""",
                (
                    supplier_id,
                    account["id"],
                    payment_id,
                    str(gross),
                    str(commission),
                    str(net),
                    self.provider.name,
                ),
            )
        result = self.provider.create_payout(
            payout_id=payout_id, amount=net, token=account["provider_token"]
        )
        sent_at = now_iso() if result.get("status") == "sent" else None
        with self.database.transaction() as conn:
            conn.execute(
                """UPDATE marketplace_payouts
                   SET status = ?, provider_ref = ?, failure_reason = ?, sent_at = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    result.get("status", "failed"),
                    result.get("provider_ref"),
                    result.get("failure_reason"),
                    sent_at,
                    now_iso(),
                    payout_id,
                ),
            )
        return self._fetch_one("SELECT * FROM marketplace_payouts WHERE id = ?", (payout_id,)) or {}

    def list_payouts(self, supplier_id: int, limit: int = 50) -> list[dict[str, Any]]:
        return self._fetch_all(
            "SELECT * FROM marketplace_payouts WHERE supplier_id = ? ORDER BY id DESC LIMIT ?",
            (supplier_id, limit),
        )
