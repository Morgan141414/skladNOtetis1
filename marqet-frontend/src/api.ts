import type { Product } from './components/ProductCard'

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

// ── Payments & installments (рассрочка) ─────────────────────────────────────

export interface InstallmentPlan {
  months: number
  markup_percent: number
  total: number
  monthly: number
  interest_free: boolean
}

export interface Payment {
  id: number
  amount: number
  total_amount: number
  markup_amount: number
  method: string
  installment_months: number
  currency: string
  provider: string
  status: 'pending' | 'processing' | 'paid' | 'failed' | 'refunded' | 'cancelled'
  redirect_url: string | null
  return_url: string | null
  failure_reason: string | null
  payment_method_id: number | null
}

export const apiInstallmentOptions = (amount: number): Promise<{ amount: number; plans: InstallmentPlan[] }> =>
  authReq(`/marketplace/payments/installment-options?amount=${encodeURIComponent(amount)}`)

export const apiCreatePayment = (body: {
  amount: number
  method: 'card' | 'installment' | 'wallet' | 'invoice'
  installment_months?: number
  inquiry_ids?: number[]
  return_url?: string
  description?: string
  payment_method_id?: number
}): Promise<Payment> =>
  authReq<Payment>('/marketplace/payments', { method: 'POST', body: JSON.stringify(body) })

export const apiGetPayment = (id: number): Promise<Payment> =>
  authReq<Payment>(`/marketplace/payments/${id}`)

// ── Saved cards (tokenized — no card data is stored by marqet.kz) ────────────

export interface SavedCard {
  id: number
  brand: string | null
  last4: string | null
  exp_month: number | null
  exp_year: number | null
  is_default: boolean
  status: 'pending' | 'active' | 'expired' | 'removed' | 'failed'
  created_at: string
}

export const apiGetCards = (): Promise<{ items: SavedCard[] }> =>
  authReq<{ items: SavedCard[] }>('/marketplace/cards')

export const apiBindCard = (return_url?: string): Promise<SavedCard & { redirect_url: string }> =>
  authReq('/marketplace/cards/bind', { method: 'POST', body: JSON.stringify({ return_url }) })

export const apiSetDefaultCard = (id: number): Promise<SavedCard> =>
  authReq(`/marketplace/cards/${id}/default`, { method: 'PATCH' })

export const apiRemoveCard = (id: number): Promise<{ removed: boolean }> =>
  authReq(`/marketplace/cards/${id}`, { method: 'DELETE' })

// ── Supplier payout accounts & payouts ──────────────────────────────────────

export interface PayoutAccount {
  id: number
  account_type: 'card' | 'bank'
  brand: string | null
  last4: string | null
  exp_month: number | null
  exp_year: number | null
  holder_name: string | null
  bank_name: string | null
  iban_last4: string | null
  is_default: boolean
  status: 'pending' | 'active' | 'rejected' | 'removed' | 'failed'
  created_at: string
}

export interface Payout {
  id: number
  payment_id: number | null
  amount: string
  commission_amount: string
  net_amount: string
  status: 'pending' | 'processing' | 'sent' | 'failed' | 'cancelled'
  failure_reason: string | null
  sent_at: string | null
  created_at: string
}

export const apiGetPayoutAccounts = (): Promise<{ items: PayoutAccount[] }> =>
  authReq<{ items: PayoutAccount[] }>('/supplier/payout-accounts')

export const apiBindPayoutAccount = (return_url?: string): Promise<PayoutAccount & { redirect_url: string }> =>
  authReq('/supplier/payout-accounts/bind', { method: 'POST', body: JSON.stringify({ return_url }) })

export const apiSetDefaultPayoutAccount = (id: number): Promise<PayoutAccount> =>
  authReq(`/supplier/payout-accounts/${id}/default`, { method: 'PATCH' })

export const apiRemovePayoutAccount = (id: number): Promise<{ removed: boolean }> =>
  authReq(`/supplier/payout-accounts/${id}`, { method: 'DELETE' })

export const apiGetPayouts = (): Promise<{ items: Payout[] }> =>
  authReq<{ items: Payout[] }>('/supplier/payouts')

export const apiCreatePayout = (payment_id: number): Promise<Payout> =>
  authReq('/supplier/payouts', { method: 'POST', body: JSON.stringify({ payment_id }) })

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
