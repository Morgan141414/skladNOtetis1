# Marketplace Production AI Handoff

This document coordinates parallel AI work on `marqet.kz` and `qpartner.kz`.
It is intentionally strict: production marketplace work must not be done by
multiple agents in the same files without an explicit handoff.

## Current Production Shape

- `marqet.kz` is the public marketplace storefront.
- `qpartner.kz` is the warehouse/qpartner application.
- The current public storefront supports catalog, product detail, seller page,
  cart, inquiry checkout, messages, favorites, listing post flow, and account.
- The current checkout creates marketplace inquiries. It is not a full paid
  order system yet.
- The next production milestone is to add a real order/payment/loyalty layer
  while keeping the inquiry/RFQ flow working.

## Main Rule

Do not build payments, saved cards, loyalty, returns, or seller payouts on top
of `marketplace_inquiries` as if inquiries were final orders.

The correct direction is:

1. Keep inquiries as RFQ/pre-order communication.
2. Add `orders` as the purchase contract.
3. Add `payments` as the money state machine.
4. Add ledgers for bonus/wallet/commission/payout movements.
5. Connect qpartner fulfillment after the order is created and stock is reserved.

## Work Ownership

### Codex / Current Agent Owns

- Marketplace production coordination docs.
- Backend-first architecture plan.
- Migration/API contract review.
- Integration safety and release gates.

Preferred files:

- `docs/marketplace-production-ai-handoff.md`
- `docs/marketplace-production-implementation-plan.md`
- future backend migration files only after explicit start

### Other AI Should Own

Frontend-only scaffolding that can be built without changing backend behavior:

- buyer account hub pages;
- orders UI placeholders;
- payment methods UI placeholders;
- loyalty UI placeholders;
- frontend API types that fail gracefully when backend returns 404;
- shared layout improvements for account/seller/admin navigation.

Preferred files for the other AI:

- `marqet-frontend/src/App.tsx`
- `marqet-frontend/src/api.ts`
- new files under `marqet-frontend/src/pages/account/`
- new files under `marqet-frontend/src/components/`

Important: keep the existing `/account` page intact. It currently behaves like
seller/listing tooling, so buyer marketplace account pages must live on new
routes under `/account/*`.

The other AI must not edit:

- `app/api/routes.py`
- `app/services/warehouse.py`
- `app/db/migrations/versions/*`
- production deploy scripts or server state

until backend contracts are agreed.

## First Backend Milestone

Goal: introduce the production order/payment/loyalty foundation without breaking
the existing inquiry checkout.

Additive only:

- new tables;
- new read/write endpoints behind `/marketplace/orders`;
- no deletion or reinterpretation of existing inquiry tables;
- no destructive migrations;
- no change to current `/marketplace/cart/checkout` behavior until a new
  endpoint is ready.

Initial concepts:

- `marketplace_orders`
- `marketplace_order_items`
- `marketplace_payments`
- `marketplace_payment_events`
- `loyalty_accounts`
- `loyalty_ledger`

The first migration should be `0048_production_marketplace_orders_payments_loyalty.py`
with `down_revision = "0046_merge_supplier_offers_marketplace_inquiry_source"`
unless the Alembic head changes before implementation starts. Re-check heads
immediately before writing the migration.

Money fields must use integer minor units, not float.

Saved cards must store only PSP tokens and masked display data. Never store PAN,
CVV, 3DS OTP, raw card form data, or sensitive PSP payloads.

If the existing backend convention for marketplace monetary fields is still
`NUMERIC(18,2)` at implementation time, keep the migration consistent with the
current schema and convert API/domain calculations carefully. Do not introduce
floats in Python or JavaScript.

## First Frontend Milestone For Other AI

Build UI routes that are useful now and safe before backend is complete:

- `/account/hub`
- `/account/orders`
- `/account/orders/:id`
- `/account/payment-methods`
- `/account/loyalty`

These pages should:

- show loading, empty, error, and unavailable states;
- call API methods that safely handle 404/501 as "feature is being prepared";
- not hardcode real card entry fields for PAN/CVV;
- use "Add card" as a PSP-tokenization flow placeholder;
- show only masked card examples in placeholder data;
- not send card data to our backend.

Do not create fake payment success flows. Payments must be wired only after the
backend payment provider abstraction exists.

## Instructions For Other AI

Use this exact scope:

1. Work only in `marqet-frontend`.
2. Do not edit `src/pages/AccountPage.tsx`; leave old `/account` behavior as-is.
3. Create account marketplace hub navigation:
   - profile;
   - orders;
   - addresses;
   - payment methods;
   - loyalty;
   - security;
   - support.
4. Add these files:
   - `src/pages/account/AccountHubPage.tsx`;
   - `src/pages/account/OrdersPage.tsx`;
   - `src/pages/account/OrderDetailPage.tsx`;
   - `src/pages/account/PaymentMethodsPage.tsx`;
   - `src/pages/account/LoyaltyPage.tsx`;
   - `src/pages/account/account.css`;
   - `src/pages/account/accountMocks.ts`;
   - `src/pages/account/accountUi.tsx`.
5. Add safe placeholder pages:
   - Orders list/detail with empty state;
   - Payment methods page with masked saved-card rows and "Add card" CTA;
   - Loyalty page with bonus balance, tier progress, and ledger empty state;
   - Address book page if time allows.
6. Add API client methods in `src/api.ts`, but make them resilient:
   - if backend returns 404, show planned-feature empty state;
   - do not block current catalog/cart/checkout.
7. Add only minimal route/header integration:
   - `src/App.tsx` for routes;
   - `src/components/Header.tsx` for menu links.
8. Run:
   - `cd marqet-frontend`
   - `npm run build`
   - `git diff --check`
9. Commit only frontend files.
10. Do not deploy to production.

Recommended frontend API contract:

- `GET /api/v1/marketplace/account/summary`
- `GET /api/v1/marketplace/orders`
- `GET /api/v1/marketplace/orders/{id}`
- `GET /api/v1/marketplace/payment-methods`
- `PATCH /api/v1/marketplace/payment-methods/{id}/default`
- `DELETE /api/v1/marketplace/payment-methods/{id}`
- `GET /api/v1/marketplace/loyalty`

Until backend is ready, frontend may use demo data only when
`VITE_MARQET_ACCOUNT_MOCKS=1` or in local dev mode. Any demo state must be
visibly marked as demo/unavailable and must not pretend that a real payment,
saved card, bonus accrual, or order has happened.

## Files To Avoid Conflicts

If another AI is active, avoid editing the same file in parallel:

- `marqet-frontend/src/api.ts`
- `marqet-frontend/src/App.tsx`
- `marqet-frontend/src/pages/AccountPage.tsx`

If those files must be edited, make small additive changes and commit quickly.

## Backend Contract For First Order Layer

The first backend implementation should add, not replace:

- `POST /api/v1/marketplace/orders/checkout`
- `GET /api/v1/marketplace/orders`
- `GET /api/v1/marketplace/orders/{order_id}`
- `POST /api/v1/marketplace/orders/{order_id}/payments`
- `POST /api/v1/marketplace/payments/{payment_id}/confirm`
- `POST /api/v1/marketplace/payments/webhook/{provider}`
- `GET /api/v1/marketplace/loyalty/me`
- `GET /api/v1/supplier/orders`
- `PATCH /api/v1/supplier/orders/{order_id}/status`

Use `Idempotency-Key` and the existing idempotency helper for checkout and
payment creation. The old `/api/v1/marketplace/cart/checkout` endpoint must
continue creating inquiries until the production order flow is fully wired and
released intentionally.

Do not touch these in the first backend increment:

- old marketplace inquiry checkout behavior;
- `marketplace_inquiries` status enum;
- purchase order document flow;
- auth/RBAC role model;
- supplier catalog price-tier structure;
- real PSP/acquiring, fiscalization, accounting, or warehouse posting.

## Parallel Work Rules

- One AI equals one branch and one isolated worktree/clone.
- One task equals one clearly named path scope.
- Do not let two agents edit the same router, migration chain, lockfile, or
  shared config at the same time.
- Do not use `git add .`.
- Do not edit `.env`, `*.session`, `*.log`, local DB files, production archives,
  or deploy state unless the task explicitly requires it.
- Migration work is serialized: only one agent may touch
  `app/db/migrations/versions/*` at a time.

## Minimum Gates

Docs-only:

- `git diff --check`

Frontend-only:

- `cd marqet-frontend && npm run build`
- `git diff --check`

Backend migration-only:

- `python -m py_compile app/api/routes.py app/services/warehouse.py`
- `python -m pytest tests/test_sqlite_migrations.py tests/test_postgresql_runtime_readiness.py -q --tb=short`
- `git diff --check`

Full backend:

- install missing dev dependencies first;
- force UTF-8 for tests on Windows;
- run targeted tests before full suite.

Known local issues:

- some tests fail on Windows with cp1251 `UnicodeDecodeError` unless UTF-8 is
  forced;
- API smoke currently needs `prometheus_fastapi_instrumentator` installed.

## Production Deploy Rule

Only deploy after:

- branch is clean;
- build passes;
- source is pushed;
- production backup is created;
- smoke checks pass on `marqet.kz`;
- no other AI is deploying at the same time.
