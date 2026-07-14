import type { Product } from './components/ProductCard'
import {
  mockAccountSummary,
  mockLoyaltyAccount,
  mockOrderDetail,
  mockOrders,
} from './pages/account/accountMocks'

const BASE = '/api/v1'

function getToken(): string | null {
  try {
    const raw = localStorage.getItem('marqet-auth')
    if (!raw) return null
    return JSON.parse(raw)?.state?.token ?? null
  } catch { return null }
}

async function req<T>(path: string, opts: RequestInit = {}, token?: string): Promise<T> {
  const tok = token ?? getToken()
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(opts.headers as any ?? {}) }
  if (tok) headers['Authorization'] = `Bearer ${tok}`
  const res = await fetch(`${BASE}${path}`, { ...opts, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err?.detail?.message ?? err?.detail ?? `HTTP ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

function toProduct(item: any): Product {
  return {
    id: item.id,
    supplier_id: item.supplier_id ?? null,
    name: item.product_name ?? item.name ?? '',
    description: item.description ?? null,
    price: item.unit_price != null ? parseFloat(item.unit_price) : null,
    unit: item.unit ?? null,
    supplier_name: item.supplier_name ?? null,
    supplier_phone: item.supplier_phone ?? null,
    image_url: item.image_url ?? null,
    category: item.category ?? null,
    view_count: item.view_count ?? 0,
    avg_rating: item.avg_rating ?? null,
    review_count: item.review_count ?? null,
    likes_count: item.likes_count ?? null,
    promoted_until: item.promoted_until ?? null,
    supplier_city: item.supplier_city ?? null,
  }
}

export async function apiBrowseCatalog(params: {
  search?: string; category?: string; sort?: string;
  min_price?: number; max_price?: number;
  limit?: number; offset?: number
} = {}): Promise<{ items: Product[]; total: number }> {
  const q = new URLSearchParams()
  if (params.search)     q.set('search', params.search)
  if (params.category)   q.set('category', params.category)
  if (params.sort)       q.set('sort', params.sort)
  if (params.min_price != null) q.set('min_price', String(params.min_price))
  if (params.max_price != null) q.set('max_price', String(params.max_price))
  if (params.limit != null)  q.set('limit', String(params.limit))
  if (params.offset != null) q.set('offset', String(params.offset))
  const suffix = q.toString() ? `?${q}` : ''
  const data = await req<any>(`/marketplace/catalog${suffix}`)
  const raw = Array.isArray(data) ? data : (data.items ?? [])
  const total = Array.isArray(data) ? raw.length : (data.total ?? raw.length)
  return { items: raw.map(toProduct), total }
}

export async function apiGetCategories(): Promise<string[]> {
  const data = await req<any>('/marketplace/catalog/categories')
  if (!Array.isArray(data)) return []; return data.map((x: any) => typeof x === "string" ? x : (x.name ?? x)).filter(Boolean)
}

export async function apiGetProduct(id: number): Promise<Product> {
  const data = await req<any>(`/marketplace/catalog/${id}`)
  return toProduct(data)
}

export async function apiRegister(body: { name: string; email: string; phone?: string; password: string }) {
  return req<{ access_token: string }>('/marketplace/auth/register', { method: 'POST', body: JSON.stringify(body) })
}

export async function apiLogin(body: { email: string; password: string }) {
  return req<{ access_token: string }>('/marketplace/auth/login', { method: 'POST', body: JSON.stringify(body) })
}

export async function apiMe(token: string) {
  return req<{ id: number; name: string; email: string; phone?: string; roles: string[]; is_nca_verified?: boolean }>('/marketplace/auth/me', {}, token)
}

export async function apiCreateListing(body: {
  title: string; description?: string; price?: number; unit?: string;
  category?: string; phone?: string; image_url?: string; city?: string
}) {
  return req<{ id: number; message: string }>('/marketplace/listings', { method: 'POST', body: JSON.stringify(body) })
}

export async function apiGetMyListings() {
  return req<{ items: any[]; total: number }>('/marketplace/my-listings')
}

export async function apiUpdateListing(id: number, body: Partial<{
  title: string; description: string; price: number; unit: string;
  category: string; phone: string; image_url: string; is_active: boolean
}>) {
  return req<{ message: string }>(`/marketplace/listings/${id}`, { method: 'PATCH', body: JSON.stringify(body) })
}

export async function apiDeleteListing(id: number) {
  return req<void>(`/marketplace/listings/${id}`, { method: 'DELETE' })
}


// ── Messaging / Inquiries ──────────────────────────────────────────────────

export async function apiContactSeller(itemId: number, message: string) {
  return req<{ id: number; status: string }>(`/marketplace/inquire/${itemId}`, {
    method: 'POST',
    body: JSON.stringify({ quantity: 1, notes: message }),
  })
}

export async function apiGetMyInquiries(status?: string) {
  const q = status ? `?status=${status}` : ''
  return req<{ items: any[]; total: number }>(`/marketplace/my-inquiries${q}`)
}

export async function apiGetInquiryMessages(inquiryId: number) {
  return req<any[]>(`/marketplace/my-inquiries/${inquiryId}/messages`)
}

export async function apiSendInquiryMessage(inquiryId: number, body: string) {
  return req<any>(`/marketplace/my-inquiries/${inquiryId}/messages`, {
    method: 'POST',
    body: JSON.stringify({ body }),
  })
}

export async function apiTrackView(itemId: number) {
  try {
    await fetch(`/api/v1/marketplace/catalog/${itemId}/view`, { method: 'POST' })
  } catch {}
}

// ── NCA / ЭЦП ──────────────────────────────────────────────────────────────

export async function apiNcaChallenge() {
  return req<{ challenge_id: string; challenge: string; expires_in: number }>(
    '/marketplace/auth/nca-challenge', { method: 'POST' }
  )
}

export async function apiNcaAuth(body: { challenge_id: string; cms_signature: string }) {
  return req<{ access_token: string; iin: string; full_name: string; is_nca_verified: boolean }>(
    '/marketplace/auth/nca-auth', { method: 'POST', body: JSON.stringify(body) }
  )
}

export async function apiGetOferta() {
  return req<{ version: string; text: string; hash: string }>('/marketplace/oferta')
}

export async function apiSignOferta(body: { cms_signature: string; oferta_version: string }) {
  return req<{ signed: boolean; signed_at: string; iin: string; full_name: string; message: string }>(
    '/marketplace/oferta/sign', { method: 'POST', body: JSON.stringify(body) }
  )
}

export async function apiOfertaStatus() {
  return req<{ oferta_signed: boolean; signed_at?: string; oferta_version?: string; is_nca_verified: boolean; iin?: string; full_name?: string }>(
    '/marketplace/oferta/status'
  )
}

// ── Cart ──────────────────────────────────────────────────────────────────────

export interface CartItem {
  id: number
  catalog_item_id: number
  quantity: number
  product_name: string
  unit: string
  unit_price: number | null
  image_url: string | null
  supplier_name: string | null
  supplier_id?: number | null
}

export interface Cart {
  items: CartItem[]
  total_items: number
  total_amount: number
}

function getToken2(): string | null {
  try { return JSON.parse(localStorage.getItem('marqet-auth') || '{}')?.state?.token ?? null } catch { return null }
}

async function authReq<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const tok = getToken2()
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(opts.headers as Record<string, string> ?? {}) }
  if (tok) headers['Authorization'] = `Bearer ${tok}`
  const res = await fetch(`/api/v1${path}`, { ...opts, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err?.detail?.message ?? err?.detail ?? `HTTP ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export const apiGetCart = (): Promise<Cart> => authReq<Cart>('/marketplace/cart')

export const apiAddToCart = (catalogItemId: number, quantity = 1): Promise<Cart> =>
  authReq<Cart>('/marketplace/cart/items', {
    method: 'POST', body: JSON.stringify({ catalog_item_id: catalogItemId, quantity })
  })

export const apiUpdateCartItem = (cartItemId: number, quantity: number): Promise<Cart> =>
  authReq<Cart>(`/marketplace/cart/items/${cartItemId}`, {
    method: 'PATCH', body: JSON.stringify({ quantity })
  })

export const apiRemoveCartItem = (cartItemId: number): Promise<Cart> =>
  authReq<Cart>(`/marketplace/cart/items/${cartItemId}`, { method: 'DELETE' })

export interface CheckoutInquiry {
  id: number
  catalog_item_id?: number
  product_name?: string
  quantity?: number
  status?: string
  supplier_id?: number | null
  supplier_name?: string | null
}

export const apiCheckoutCart = (body: { notes?: string; warehouse_id?: number | null; source?: 'marqet' | 'qpartner' | 'api' }): Promise<CheckoutInquiry[]> =>
  authReq<CheckoutInquiry[]>('/marketplace/cart/checkout', {
    method: 'POST',
    body: JSON.stringify({
      source: 'marqet',
      warehouse_id: body.warehouse_id ?? null,
      notes: body.notes ?? null,
      ...body,
    }),
  })

// ── Favorites ────────────────────────────────────────────────────────────────

export const apiToggleFavorite = (itemId: number): Promise<{ favorited: boolean; likes_count: number }> =>
  authReq<{ favorited: boolean; likes_count: number }>(`/marketplace/catalog/${itemId}/favorite`, { method: 'POST' })

export const apiCheckFavorite = (itemId: number): Promise<{ favorited: boolean; likes_count: number }> =>
  authReq<{ favorited: boolean; likes_count: number }>(`/marketplace/catalog/${itemId}/favorite`)

export const apiGetMyFavorites = (): Promise<{ items: any[]; total: number }> =>
  authReq<{ items: any[]; total: number }>('/marketplace/my-favorites')

// ── WhatsApp OTP ──────────────────────────────────────────────────────────────

export const apiSendPhoneOtp = (phone: string): Promise<{ sent: boolean; expires_in: number }> =>
  authReq<{ sent: boolean; expires_in: number }>('/marketplace/auth/send-phone-otp', {
    method: 'POST', body: JSON.stringify({ phone })
  })

export const apiVerifyPhoneOtp = (phone: string, otp: string): Promise<{ verified: boolean; phone: string }> =>
  authReq<{ verified: boolean; phone: string }>('/marketplace/auth/verify-phone-otp', {
    method: 'POST', body: JSON.stringify({ phone, otp })
  })

// ── Seller profile & listing management ──────────────────────────────────────

export interface SellerProfile {
  id: number
  name: string
  city?: string | null
  phone?: string | null
  email?: string | null
  is_verified: boolean
  created_at: string
  total_listings: number
  active_listings: number
  seller_rating: number
  total_reviews: number
  listings: any[]
}

export const apiGetSellerProfile = (supplierId: number): Promise<SellerProfile> =>
  authReq<SellerProfile>(`/marketplace/seller/${supplierId}`)

export const apiExtendListing = (itemId: number, days: number): Promise<{ expires_at: string; listing_plan: string; message: string }> =>
  authReq(`/marketplace/listings/${itemId}/extend`, { method: 'PATCH', body: JSON.stringify({ days }) })

export const apiPromoteListing = (itemId: number, days: number): Promise<{ promoted_until: string; message: string }> =>
  authReq(`/marketplace/listings/${itemId}/promote`, { method: 'PATCH', body: JSON.stringify({ days }) })

export interface AdminStats {
  total_users: number
  new_users_7d: number
  total_posts: number
  active_posts: number
  archived_posts: number
  promoted_posts: number
  new_posts_7d: number
  total_reviews: number
  open_tickets: number
  top_categories: { category: string; count: number }[]
}

export const apiGetAdminStats = (): Promise<AdminStats> =>
  authReq<AdminStats>('/marketplace/admin/stats')

// ── Buyer account hub / orders / payments / loyalty ────────────────────────

export type MarketplaceOrderStatus =
  | 'draft'
  | 'pending'
  | 'pending_payment'
  | 'paid'
  | 'accepted'
  | 'preparing'
  | 'shipped'
  | 'delivered'
  | 'completed'
  | 'cancelled'
  | 'refund_requested'
  | 'refunded'

export interface MockableResponse {
  is_mock?: boolean
  unavailable?: boolean
}

export interface AccountSummary extends MockableResponse {
  active_orders: number
  delivered_orders: number
  bonus_points: number
  saved_payment_methods: number
  open_messages: number
  seller_listings: number
}

export interface MarketplaceOrderListItem extends MockableResponse {
  id: number
  number: string
  status: MarketplaceOrderStatus
  created_at: string
  updated_at?: string | null
  total_amount: number | null
  currency: 'KZT'
  items_count: number
  supplier_id?: number | null
  supplier_name?: string | null
  product_name?: string | null
  source_inquiry_id?: number | null
  payment_status?: 'unpaid' | MarketplacePayment['status']
  delivery_status?: 'not_started' | 'preparing' | 'in_transit' | 'delivered'
}

export interface MarketplaceOrderItem {
  id: number
  catalog_item_id?: number | null
  product_name: string
  quantity: number
  unit?: string | null
  unit_price: number | null
  image_url?: string | null
}

export interface MarketplaceOrderTimelineEvent {
  id: string
  title: string
  description?: string | null
  created_at: string
  status?: MarketplaceOrderStatus
}

export interface MarketplaceOrderDetail extends MarketplaceOrderListItem {
  buyer_name?: string | null
  buyer_phone?: string | null
  delivery_address?: string | null
  notes?: string | null
  items: MarketplaceOrderItem[]
  latest_payment?: MarketplacePayment | null
  timeline: MarketplaceOrderTimelineEvent[]
}

export interface PaymentMethod extends MockableResponse {
  id: string
  provider?: string | null
  brand: 'visa' | 'mastercard' | 'kaspi' | 'halyk' | 'unknown'
  last4: string
  expiry_month?: number | null
  expiry_year?: number | null
  holder_name?: string | null
  is_default: boolean
  status: 'active' | 'expired' | 'disabled'
}

export interface LoyaltyEvent {
  id: string
  type: 'earn' | 'redeem' | 'adjust' | 'reversal' | 'expire'
  title: string
  points_delta: number
  created_at: string
  order_number?: string | null
}

export interface LoyaltyAccount extends MockableResponse {
  tier: 'bronze' | 'silver' | 'gold' | 'platinum'
  points_balance: number
  points_pending: number
  next_tier_points: number
  lifetime_spend: number
  currency: 'KZT'
  history: LoyaltyEvent[]
}

export interface AccountOrdersResponse extends MockableResponse {
  items: MarketplaceOrderListItem[]
  total: number
}

export interface PaymentMethodsResponse extends MockableResponse {
  items: PaymentMethod[]
}

export interface MarketplacePayment {
  id: number
  order_id: number
  provider: string
  status: 'pending' | 'requires_action' | 'authorized' | 'paid' | 'failed' | 'cancelled' | 'refunded'
  amount: number | null
  currency: 'KZT'
  payment_url?: string | null
  created_at: string
  paid_at?: string | null
}

export type SupplierMarketplaceOrderNextStatus =
  | 'accepted'
  | 'preparing'
  | 'shipped'
  | 'delivered'
  | 'completed'
  | 'cancelled'

export interface SupplierMarketplaceOrdersResponse extends MockableResponse {
  items: MarketplaceOrderListItem[]
  total: number
}

export interface SupplierMarketplaceWallet extends MockableResponse {
  supplier_id: number
  currency: 'KZT'
  available_amount: number
  pending_amount: number
  posted_credit: number
  posted_debit: number
  pending_ledger: number
  ledger_entries: number
  created_at?: string | null
  updated_at?: string | null
}

export interface SupplierMarketplaceLedgerEntry {
  id: number
  order_id?: number | null
  order_number?: string | null
  payment_id?: number | null
  provider?: string | null
  provider_payment_id?: string | null
  entry_type: 'credit' | 'debit' | 'hold' | 'release' | 'refund' | 'adjust'
  status: 'pending' | 'posted' | 'cancelled'
  amount: number
  currency: 'KZT'
  description?: string | null
  source_type?: string | null
  source_id?: string | null
  created_at: string
}

export interface SupplierMarketplaceLedgerResponse extends MockableResponse {
  items: SupplierMarketplaceLedgerEntry[]
  total: number
}

class AccountApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function accountReq<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const tok = getToken2()
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(opts.headers as Record<string, string> ?? {}) }
  if (tok) headers['Authorization'] = `Bearer ${tok}`
  const res = await fetch(`/api/v1${path}`, { ...opts, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new AccountApiError(res.status, err?.detail?.message ?? err?.detail ?? `HTTP ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

const accountEnv = (import.meta as ImportMeta & { env?: Record<string, string | boolean | undefined> }).env ?? {}
const USE_ACCOUNT_MOCKS =
  accountEnv.VITE_MARQET_ACCOUNT_MOCKS === '1' ||
  accountEnv.DEV === true

function markMock<T extends MockableResponse>(value: T, unavailable = false): T {
  return { ...value, is_mock: true, unavailable }
}

async function withAccountFallback<T extends MockableResponse>(
  real: () => Promise<T>,
  mock: T,
): Promise<T> {
  if (USE_ACCOUNT_MOCKS) return markMock(mock)
  try {
    return await real()
  } catch (error) {
    if (error instanceof AccountApiError && (error.status === 404 || error.status === 501)) {
      return markMock(mock, true)
    }
    throw error
  }
}

export const apiGetAccountSummary = (): Promise<AccountSummary> =>
  withAccountFallback(
    () => accountReq<AccountSummary>('/marketplace/account/summary'),
    mockAccountSummary,
  )

export const apiGetMyOrders = (params: { status?: string; limit?: number; offset?: number } = {}): Promise<AccountOrdersResponse> => {
  const q = new URLSearchParams()
  if (params.status) q.set('status', params.status)
  if (params.limit != null) q.set('limit', String(params.limit))
  if (params.offset != null) q.set('offset', String(params.offset))
  const suffix = q.toString() ? `?${q}` : ''
  return withAccountFallback(
    () => accountReq<AccountOrdersResponse>(`/marketplace/orders${suffix}`),
    mockOrders,
  )
}

export const apiGetOrder = (id: number): Promise<MarketplaceOrderDetail> =>
  withAccountFallback(
    () => accountReq<MarketplaceOrderDetail>(`/marketplace/orders/${id}`),
    mockOrderDetail(id),
  )

function makeIdempotencyKey(prefix: string): string {
  const cryptoValue = globalThis.crypto?.randomUUID?.()
  return cryptoValue ? `${prefix}-${cryptoValue}` : `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

export const apiCheckoutMarketplaceOrders = (body: {
  warehouse_id?: number | null
  source?: 'marqet' | 'qpartner' | 'api'
  buyer_name?: string | null
  buyer_phone?: string | null
  buyer_email?: string | null
  delivery_address?: string | null
  notes?: string | null
}): Promise<{ items: MarketplaceOrderDetail[] }> =>
  accountReq<{ items: MarketplaceOrderDetail[] }>('/marketplace/orders/checkout', {
    method: 'POST',
    headers: { 'Idempotency-Key': makeIdempotencyKey('checkout') },
    body: JSON.stringify({ source: 'marqet', warehouse_id: null, ...body }),
  })

export const apiCreateMarketplacePayment = (
  orderId: number,
  body: { provider?: string; payment_method_id?: number | null } = {},
): Promise<MarketplacePayment> =>
  accountReq<MarketplacePayment>(`/marketplace/orders/${orderId}/payments`, {
    method: 'POST',
    headers: { 'Idempotency-Key': makeIdempotencyKey(`payment-${orderId}`) },
    body: JSON.stringify({
      provider: body.provider ?? 'manual',
      payment_method_id: body.payment_method_id ?? null,
    }),
  })

export const apiCancelMarketplaceOrder = (
  orderId: number,
  reason: string,
): Promise<MarketplaceOrderDetail> =>
  accountReq<MarketplaceOrderDetail>(`/marketplace/orders/${orderId}/cancel`, {
    method: 'POST',
    headers: { 'Idempotency-Key': makeIdempotencyKey(`cancel-${orderId}`) },
    body: JSON.stringify({ reason }),
  })

export const apiRequestMarketplaceRefund = (
  orderId: number,
  reason: string,
): Promise<MarketplaceOrderDetail> =>
  accountReq<MarketplaceOrderDetail>(`/marketplace/orders/${orderId}/refund-request`, {
    method: 'POST',
    headers: { 'Idempotency-Key': makeIdempotencyKey(`refund-${orderId}`) },
    body: JSON.stringify({ reason }),
  })

export const apiGetSupplierMarketplaceOrders = (params: { status?: string; limit?: number; offset?: number } = {}): Promise<SupplierMarketplaceOrdersResponse> => {
  const q = new URLSearchParams()
  if (params.status) q.set('status', params.status)
  if (params.limit != null) q.set('limit', String(params.limit))
  if (params.offset != null) q.set('offset', String(params.offset))
  const suffix = q.toString() ? `?${q}` : ''
  return accountReq<SupplierMarketplaceOrdersResponse>(`/supplier/marketplace-orders${suffix}`)
}

export const apiGetSupplierMarketplaceOrder = (id: number): Promise<MarketplaceOrderDetail> =>
  accountReq<MarketplaceOrderDetail>(`/supplier/marketplace-orders/${id}`)

export const apiUpdateSupplierMarketplaceOrderStatus = (
  orderId: number,
  body: { status: SupplierMarketplaceOrderNextStatus; cancel_reason?: string | null },
): Promise<MarketplaceOrderDetail> =>
  accountReq<MarketplaceOrderDetail>(`/supplier/marketplace-orders/${orderId}/status`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  })

export const apiGetSupplierMarketplaceWallet = (): Promise<SupplierMarketplaceWallet> =>
  accountReq<SupplierMarketplaceWallet>('/supplier/marketplace-wallet')

export const apiGetSupplierMarketplaceLedger = (params: { limit?: number; offset?: number } = {}): Promise<SupplierMarketplaceLedgerResponse> => {
  const q = new URLSearchParams()
  if (params.limit != null) q.set('limit', String(params.limit))
  if (params.offset != null) q.set('offset', String(params.offset))
  const suffix = q.toString() ? `?${q}` : ''
  return accountReq<SupplierMarketplaceLedgerResponse>(`/supplier/marketplace-wallet/ledger${suffix}`)
}

export const apiBindPaymentMethod = (body: {
  provider: string
  provider_token: string
  brand?: PaymentMethod['brand']
  last4: string
  expiry_month?: number | null
  expiry_year?: number | null
  holder_name?: string | null
  is_default?: boolean
}): Promise<PaymentMethod> =>
  accountReq<PaymentMethod>('/marketplace/payment-methods', {
    method: 'POST',
    headers: { 'Idempotency-Key': makeIdempotencyKey('payment-method') },
    body: JSON.stringify(body),
  })

export const apiGetPaymentMethods = (): Promise<PaymentMethodsResponse> =>
  accountReq<PaymentMethodsResponse>('/marketplace/payment-methods')

export const apiSetDefaultPaymentMethod = (id: string): Promise<PaymentMethod> =>
  accountReq<PaymentMethod>(`/marketplace/payment-methods/${id}/default`, { method: 'PATCH' })

export const apiDeletePaymentMethod = (id: string): Promise<void> =>
  accountReq<void>(`/marketplace/payment-methods/${id}`, { method: 'DELETE' })

export const apiGetLoyaltyAccount = (): Promise<LoyaltyAccount> =>
  withAccountFallback(
    () => accountReq<LoyaltyAccount>('/marketplace/loyalty'),
    mockLoyaltyAccount,
  )
