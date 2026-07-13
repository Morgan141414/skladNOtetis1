# Marketplace Production Implementation Plan

This is the first implementation plan for moving `marqet.kz` from marketplace
MVP to production marketplace. It is scoped for safe incremental development.

## Phase 0: Coordination And Safety

Status: started.

Tasks:

- keep `marqet.kz` storefront and `qpartner.kz` warehouse concerns separated;
- avoid direct production edits except explicit deploy tasks;
- keep all AI workers on separate file scopes;
- document handoffs before coding shared contracts.

Deliverables:

- `docs/marketplace-production-ai-handoff.md`;
- this implementation plan;
- explicit instructions for the other AI.

Parallel work policy:

- one AI works in one isolated branch/worktree;
- each task has an explicit file scope before edits start;
- frontend, backend services, migrations, docs, and deploy work are committed
  separately;
- migration work is serialized, because Alembic heads are shared state;
- no one deploys while another agent is changing production-facing assets.

## Phase 1: Order Foundation

Goal: add a real order domain without removing current inquiry/RFQ flow.

Backend deliverables:

- migration `0048_production_marketplace_orders_payments_loyalty.py`;
- `marketplace_orders`;
- `marketplace_order_items`;
- `marketplace_payments`;
- `marketplace_payment_events`;
- `loyalty_accounts`;
- `loyalty_ledger`;
- service methods:
  - create production orders from cart;
  - list buyer orders;
  - get buyer order detail;
  - create payment attempt;
  - confirm manual/test payment;
  - write loyalty ledger entries;
  - list supplier orders;
  - update supplier operational status;
- API endpoints:
  - `POST /api/v1/marketplace/orders/checkout`;
  - `GET /api/v1/marketplace/orders`;
  - `GET /api/v1/marketplace/orders/{order_id}`;
  - `POST /api/v1/marketplace/orders/{order_id}/payments`;
  - `POST /api/v1/marketplace/payments/{payment_id}/confirm`;
  - `POST /api/v1/marketplace/payments/webhook/{provider}`;
  - `GET /api/v1/marketplace/loyalty/me`;
  - `GET /api/v1/supplier/orders`;
  - `PATCH /api/v1/supplier/orders/{order_id}/status`.

Compatibility:

- keep `/marketplace/cart/checkout` unchanged;
- new checkout UI can choose new order flow later;
- existing inquiry/messages flow remains available.

Statuses:

- `draft`
- `pending_payment`
- `paid`
- `accepted`
- `preparing`
- `shipped`
- `delivered`
- `completed`
- `cancelled`
- `refunded`

Money:

- prefer integer minor units in application contracts;
- if current database conventions require `NUMERIC(18,2)`, keep schema
  consistent and avoid floats in application code;
- keep currency as `KZT`;
- avoid floats for order/payment totals.

Idempotency:

- checkout and payment creation must require/use `Idempotency-Key`;
- repeated clicks must not create duplicate orders or duplicate payment attempts.

## Phase 2: Payment And Saved Cards

Goal: payment provider abstraction and safe saved-card tokenization.

Backend deliverables:

- `marketplace_payment_intents`;
- `marketplace_payment_attempts`;
- `marketplace_payment_transactions`;
- `marketplace_saved_payment_methods`;
- `marketplace_payment_webhook_events`;
- `marketplace_refunds`;
- provider interface:
  - create payment;
  - confirm 3DS;
  - capture;
  - cancel;
  - refund;
  - get status;
  - bind card;
  - charge token;
  - delete token;
  - handle webhook.

Rules:

- do not store PAN;
- do not store CVV;
- do not store 3DS OTP;
- store PSP token, masked PAN, brand, expiry, consent metadata only;
- final payment state must come from verified webhook or server-to-server status.

Frontend deliverables:

- `/account/payment-methods`;
- payment step in checkout;
- 3DS pending/failed/success states;
- saved-card list with masked cards only.

## Phase 3: Loyalty And Promotions

Goal: auditable bonus and promo system.

Backend deliverables:

- `marketplace_bonus_accounts`;
- `marketplace_bonus_transactions`;
- `marketplace_loyalty_rules`;
- `marketplace_promo_codes`;
- `marketplace_coupon_redemptions`;
- reserve/release/earn/burn bonus operations;
- bonus expiry job.

Frontend deliverables:

- `/account/loyalty`;
- checkout bonus redemption;
- promo code apply/remove;
- bonus transaction history.

Rules:

- bonus movements must be ledgered;
- refunds must reverse earned/spent bonuses correctly;
- promotions must have budget, period, eligibility, stacking rules.

## Phase 4: Delivery, Returns, Disputes

Backend deliverables:

- `marketplace_shipments`;
- `marketplace_tracking_events`;
- `marketplace_return_requests`;
- `marketplace_return_items`;
- `marketplace_disputes`;
- `marketplace_dispute_messages`;
- `marketplace_dispute_evidence`.

Frontend deliverables:

- `/account/orders/:id`;
- `/account/orders/:id/return`;
- tracking timeline;
- support/dispute escalation.

## Phase 5: Seller Cabinet And Admin

Seller cabinet:

- dashboard;
- products;
- orders;
- returns;
- payouts;
- reviews;
- promotions;
- documents;
- qpartner warehouse sync;
- staff roles.

Admin:

- users;
- sellers;
- listing moderation;
- orders;
- payments;
- refunds;
- disputes;
- support;
- categories;
- banners;
- audit log;
- risk flags.

## First Tasks To Start Now

Codex:

1. maintain this plan;
2. prepare backend order/payment/loyalty migration contract;
3. keep prod stable.

Other AI:

1. work only in `marqet-frontend`;
2. keep existing `/account` page unchanged;
3. add `/account/hub`, `/account/orders`, `/account/orders/:id`,
   `/account/payment-methods`, and `/account/loyalty`;
4. add new files under `marqet-frontend/src/pages/account/`;
5. add resilient API methods in `src/api.ts` that handle backend 404/501 as
   planned-feature empty states;
6. touch `src/App.tsx` and `src/components/Header.tsx` only for minimal route
   and navigation integration;
7. run frontend build and `git diff --check`;
8. commit only frontend files;
9. do not touch backend, migrations, production deploy scripts, or server state.
