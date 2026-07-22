import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useStore } from '../store'
import {
  apiGetMyListings, apiDeleteListing, apiUpdateListing, apiExtendListing, apiPromoteListing, apiGetAdminStats,
  apiGetCards, apiSetDefaultCard, apiRemoveCard,
  apiGetPayoutAccounts, apiSetDefaultPayoutAccount, apiRemovePayoutAccount,
  apiGetPayouts,
  type AdminStats, type SavedCard, type PayoutAccount, type Payout,
} from '../api'
import EditListingModal from '../components/EditListingModal'
import AddCardModal from '../components/AddCardModal'
import { useToast } from '../components/Toast'

const css = `
.acc-wrap { max-width:900px; margin:0 auto; padding:32px 20px 60px; }
.acc-header { display:flex; align-items:center; gap:16px; margin-bottom:32px; background:#fff; border-radius:16px; border:1px solid #E2E8F0; padding:24px; }
.acc-avatar { width:64px; height:64px; border-radius:50%; background:var(--brand-grad); color:#fff; font-size:26px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.acc-name { font-size:22px; font-weight:900; color:#1E1B4B; }
.acc-email { font-size:13px; color:#64748B; margin-top:2px; }
.acc-role { display:inline-flex; align-items:center; gap:4px; background:#EEF2FF; color:#5B4FE8; font-size:11px; font-weight:700; padding:3px 10px; border-radius:20px; margin-top:6px; }
.acc-role-admin { background:#1E1B4B; color:#fff; }
.nca-verified { display:inline-flex;align-items:center;gap:5px;background:#D1FAE5;color:#065F46;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:700;margin-top:6px; }
.nca-unverified { display:inline-flex;align-items:center;gap:5px;background:#FEF3C7;color:#92400E;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:700;margin-top:6px;cursor:pointer;border:none;font-family:inherit; }
.nca-unverified:hover { background:#FDE68A; }
.pay-section { background:#fff; border:1px solid #E2E8F0; border-radius:16px; padding:22px; margin-bottom:20px; }
.pay-head { display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }
.pay-title { font-size:16px; font-weight:900; color:#1E1B4B; }
.pay-subtitle { font-size:13px; font-weight:800; color:#475569; margin-bottom:8px; }
.pay-add { background:#EEF2FF; color:#5B4FE8; border:0; border-radius:10px; padding:8px 14px; font-size:13px; font-weight:800; cursor:pointer; font-family:inherit; }
.pay-add:disabled { opacity:.55; cursor:not-allowed; }
.pay-hint { color:#64748B; font-size:12px; line-height:1.5; margin:8px 0 14px; }
.pay-empty { color:#94A3B8; font-size:13px; background:#F8FAFC; border:1px dashed #E2E8F0; border-radius:12px; padding:16px; text-align:center; }
.pay-card { display:flex; align-items:center; gap:12px; border:1.5px solid #E2E8F0; border-radius:12px; padding:12px 14px; margin-bottom:8px; }
.pay-card-icon { font-size:20px; }
.pay-card-num { font-size:14px; font-weight:800; color:#1E1B4B; }
.pay-card-exp { font-size:12px; color:#94A3B8; margin-top:2px; }
.pay-badge { background:#D1FAE5; color:#065F46; font-size:11px; font-weight:800; padding:3px 9px; border-radius:20px; }
.pay-link { background:none; border:0; color:#5B4FE8; font-size:12px; font-weight:700; cursor:pointer; font-family:inherit; }
.pay-del { background:none; border:0; color:#CBD5E1; font-size:15px; cursor:pointer; padding:4px 6px; }
.pay-del:hover { color:#EF4444; }
.payout-row { display:flex; align-items:center; justify-content:space-between; gap:12px; border-top:1px solid #F1F5F9; padding:10px 2px; }
.payout-status { font-size:11px; font-weight:800; padding:3px 9px; border-radius:20px; }
.payout-sent { background:#D1FAE5; color:#065F46; }
.payout-failed { background:#FEE2E2; color:#991B1B; }
.payout-pending, .payout-processing { background:#FEF3C7; color:#92400E; }
.stats-row { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:28px; }
.stat-card { background:#fff; border-radius:14px; border:1px solid #E2E8F0; padding:18px; text-align:center; }
.stat-num { font-size:28px; font-weight:900; color:#5B4FE8; }
.stat-label { font-size:12px; color:#94A3B8; font-weight:600; margin-top:2px; }
.btn-post { display:inline-flex; align-items:center; gap:6px; padding:10px 22px; border-radius:12px; background:var(--brand-grad); color:#fff; font-size:14px; font-weight:700; border:none; cursor:pointer; margin-bottom:20px; }
.lcard { background:#fff; border:1px solid #E2E8F0; border-radius:14px; padding:16px; display:flex; gap:14px; margin-bottom:10px; align-items:flex-start; transition:all .18s; }
.lcard:hover { border-color:#C7D2FE; box-shadow:0 4px 16px rgba(91,79,232,.08); }
.lcard.expired { border-color:#FEE2E2; background:#FFFAFA; }
.lcard.promoted { border-color:#F59E0B; box-shadow:0 0 0 2px rgba(245,158,11,.15); }
.lthumb { width:88px; height:88px; border-radius:10px; object-fit:cover; flex-shrink:0; background:#F1F5F9; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.lthumb img { width:100%; height:100%; object-fit:cover; }
.lbody { flex:1; min-width:0; }
.ltitle { font-size:16px; font-weight:700; color:#1E1B4B; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:4px; }
.lprice { font-size:18px; font-weight:800; color:#5B4FE8; margin-bottom:6px; }
.lmeta { font-size:12px; color:#94A3B8; margin-bottom:6px; display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
.lactions { display:flex; gap:8px; flex-wrap:wrap; }
.btn-sm { padding:6px 14px; border-radius:8px; font-size:12px; font-weight:700; border:none; cursor:pointer; transition:all .15s; }
.btn-edit { background:#EEF2FF; color:#5B4FE8; }
.btn-edit:hover { background:#E0E7FF; }
.btn-toggle-on { background:#D1FAE5; color:#059669; }
.btn-toggle-off { background:#F3F4F6; color:#6B7280; }
.btn-del { background:#FEF2F2; color:#EF4444; }
.btn-extend { background:#FEF3C7; color:#92400E; }
.btn-extend:hover { background:#FDE68A; }
.btn-promote { background:linear-gradient(135deg,#F59E0B,#EF4444); color:#fff; }
.btn-promote:hover { opacity:.9; }
.badge-active { background:#D1FAE5; color:#059669; font-size:10px; font-weight:700; padding:2px 8px; border-radius:20px; }
.badge-inactive { background:#F3F4F6; color:#9CA3AF; font-size:10px; font-weight:700; padding:2px 8px; border-radius:20px; }
.badge-expired { background:#FEE2E2; color:#EF4444; font-size:10px; font-weight:700; padding:2px 8px; border-radius:20px; }
.badge-promoted { background:linear-gradient(135deg,#F59E0B,#EF4444); color:#fff; font-size:10px; font-weight:700; padding:2px 8px; border-radius:20px; }
.badge-expiry { font-size:11px; padding:2px 8px; border-radius:20px; font-weight:700; }
.badge-exp-ok { background:#EEF2FF; color:#5B4FE8; }
.badge-exp-warn { background:#FEF3C7; color:#92400E; }
.badge-exp-crit { background:#FEE2E2; color:#EF4444; }
.lstat { display:flex; align-items:center; gap:3px; font-size:11px; color:#94A3B8; }
.empty-state { text-align:center; padding:60px 20px; }
.empty-state h3 { font-size:18px; font-weight:700; color:#475569; margin-bottom:8px; }
.confirm-overlay { position:fixed; inset:0; background:rgba(15,15,35,.5); z-index:500; display:flex; align-items:center; justify-content:center; }
.confirm-box { background:#fff; border-radius:16px; padding:28px 24px; max-width:360px; width:100%; text-align:center; }
.confirm-box h3 { font-size:18px; font-weight:800; color:#1E1B4B; margin-bottom:8px; }
.confirm-box p { font-size:14px; color:#64748B; margin-bottom:24px; }
.confirm-btns { display:flex; gap:10px; justify-content:center; }
/* Admin */
.admin-panel { background:#fff; border:2px solid #1E1B4B; border-radius:16px; padding:24px; margin-bottom:28px; }
.admin-title { font-size:18px; font-weight:900; color:#1E1B4B; margin-bottom:16px; display:flex; align-items:center; gap:8px; }
.admin-stats-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(130px,1fr)); gap:10px; margin-bottom:20px; }
.admin-stat { background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:12px; text-align:center; }
.admin-stat-val { font-size:22px; font-weight:900; color:#1E1B4B; }
.admin-stat-lbl { font-size:11px; color:#94A3B8; font-weight:600; margin-top:2px; }
.admin-stat.highlight { background:#EEF2FF; border-color:#C7D2FE; }
.admin-stat.highlight .admin-stat-val { color:#5B4FE8; }
.admin-tabs { display:flex; gap:8px; margin-bottom:20px; flex-wrap:wrap; }
.admin-tab { padding:8px 18px; border-radius:20px; border:1.5px solid #E2E8F0; background:#fff; font-size:13px; font-weight:700; color:#475569; cursor:pointer; }
.admin-tab.active { background:#1E1B4B; border-color:#1E1B4B; color:#fff; }
.ticket-row { border:1px solid #E2E8F0; border-radius:12px; padding:14px; margin-bottom:8px; }
.ticket-subject { font-size:14px; font-weight:700; color:#1E1B4B; margin-bottom:4px; }
.ticket-meta { font-size:12px; color:#94A3B8; margin-bottom:8px; }
.ticket-msg { font-size:13px; color:#475569; line-height:1.5; white-space:pre-wrap; }
.ticket-status { display:inline-flex; align-items:center; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.ts-new { background:#DBEAFE; color:#1D4ED8; }
.ts-in_progress { background:#FEF3C7; color:#92400E; }
.ts-resolved { background:#D1FAE5; color:#059669; }
.ts-closed { background:#F3F4F6; color:#6B7280; }
.ticket-actions { display:flex; gap:6px; margin-top:10px; flex-wrap:wrap; }
.ta-btn { padding:4px 12px; border-radius:8px; font-size:11px; font-weight:700; border:none; cursor:pointer; }
.top-cats { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px; }
.top-cat { background:#EEF2FF; color:#5B4FE8; font-size:11px; font-weight:700; padding:3px 10px; border-radius:20px; }
@media(max-width:480px){.stats-row{grid-template-columns:1fr 1fr}.acc-header{flex-direction:column;text-align:center}}
`

interface Listing {
  id: number; product_name: string; unit_price: number | null; unit: string;
  category: string | null; description: string | null; image_url: string | null;
  is_active: boolean; created_at: string; supplier_phone: string | null; city: string | null;
  view_count?: number; likes_count?: number;
  expires_at?: string | null; listing_plan?: string; promoted_until?: string | null;
}

interface Ticket {
  id: number; name: string; email: string | null; phone: string | null;
  subject: string; message: string; status: string;
  actor_id: string | null; created_at: string;
}

const STATUS_LABELS: Record<string, string> = {
  new: 'Новый', in_progress: 'В работе', resolved: 'Решён', closed: 'Закрыт',
}
const STATUS_NEXT: Record<string, string[]> = {
  new: ['in_progress', 'closed'],
  in_progress: ['resolved', 'closed'],
  resolved: ['closed'],
  closed: [],
}

function getToken() {
  try { return JSON.parse(localStorage.getItem('marqet-auth') || '{}')?.state?.token ?? null } catch { return null }
}

function daysLeft(expiresAt: string | null | undefined): number | null {
  if (!expiresAt) return null
  const diff = new Date(expiresAt).getTime() - Date.now()
  return Math.floor(diff / 86400000)
}

function ExpiryBadge({ expiresAt, isActive }: { expiresAt?: string | null; isActive: boolean }) {
  if (!isActive) return null
  const days = daysLeft(expiresAt)
  if (days === null) return null
  if (days < 0) return <span className="badge-expiry badge-exp-crit">Истёк</span>
  if (days <= 2) return <span className="badge-expiry badge-exp-crit">Истекает через {days} дн.</span>
  if (days <= 5) return <span className="badge-expiry badge-exp-warn">Ещё {days} дн.</span>
  return <span className="badge-expiry badge-exp-ok">Ещё {days} дн.</span>
}

function AdminPanel() {
  const [tab, setTab] = useState<'new'|'in_progress'|'resolved'|'closed'>('new')
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState<AdminStats | null>(null)

  useEffect(() => {
    apiGetAdminStats().then(setStats).catch(() => {})
  }, [])

  async function load(status: string) {
    setLoading(true)
    try {
      const tok = getToken()
      const res = await fetch(`/api/v1/marketplace/admin/support-tickets?status=${status}&limit=50`, {
        headers: tok ? { Authorization: `Bearer ${tok}` } : {}
      })
      const d = await res.json()
      setTickets(d.items || [])
      setTotal(d.total || 0)
    } catch {} finally { setLoading(false) }
  }

  useEffect(() => { load(tab) }, [tab])

  async function changeStatus(id: number, status: string) {
    const tok = getToken()
    await fetch(`/api/v1/marketplace/admin/support-tickets/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', ...(tok ? { Authorization: `Bearer ${tok}` } : {}) },
      body: JSON.stringify({ status }),
    })
    setTickets(t => t.filter(x => x.id !== id))
    setTotal(n => Math.max(0, n - 1))
  }

  return (
    <div className="admin-panel">
      <div className="admin-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        Панель администратора
      </div>

      {stats && (
        <>
          <div className="admin-stats-grid">
            <div className="admin-stat highlight">
              <div className="admin-stat-val">{stats.total_users}</div>
              <div className="admin-stat-lbl">Пользователей</div>
            </div>
            <div className="admin-stat">
              <div className="admin-stat-val">+{stats.new_users_7d}</div>
              <div className="admin-stat-lbl">Новых за 7 дн.</div>
            </div>
            <div className="admin-stat highlight">
              <div className="admin-stat-val">{stats.active_posts}</div>
              <div className="admin-stat-lbl">Активных постов</div>
            </div>
            <div className="admin-stat">
              <div className="admin-stat-val">{stats.archived_posts}</div>
              <div className="admin-stat-lbl">В архиве</div>
            </div>
            <div className="admin-stat">
              <div className="admin-stat-val">{stats.promoted_posts}</div>
              <div className="admin-stat-lbl">Продвигается</div>
            </div>
            <div className="admin-stat">
              <div className="admin-stat-val">+{stats.new_posts_7d}</div>
              <div className="admin-stat-lbl">Новых постов 7д</div>
            </div>
            <div className="admin-stat">
              <div className="admin-stat-val">{stats.total_reviews}</div>
              <div className="admin-stat-lbl">Отзывов</div>
            </div>
            <div className="admin-stat" style={stats.open_tickets > 0 ? {background:'#FEF2F2',borderColor:'#FEE2E2'} : {}}>
              <div className="admin-stat-val" style={stats.open_tickets > 0 ? {color:'#EF4444'} : {}}>{stats.open_tickets}</div>
              <div className="admin-stat-lbl">Открытых тикетов</div>
            </div>
          </div>
          {stats.top_categories.length > 0 && (
            <div style={{marginBottom:20}}>
              <div style={{fontSize:12,fontWeight:700,color:'#94A3B8',marginBottom:6}}>ТОП КАТЕГОРИИ</div>
              <div className="top-cats">
                {stats.top_categories.map(c => (
                  <span key={c.category} className="top-cat">{c.category} ({c.count})</span>
                ))}
              </div>
            </div>
          )}
          <div style={{height:1,background:'#E2E8F0',marginBottom:20}}/>
        </>
      )}

      <div style={{fontWeight:700,color:'#475569',marginBottom:12,fontSize:14}}>Обращения в поддержку</div>
      <div className="admin-tabs">
        {(['new','in_progress','resolved','closed'] as const).map(s => (
          <button key={s} className={`admin-tab ${tab === s ? 'active' : ''}`} onClick={() => setTab(s)}>
            {STATUS_LABELS[s]}
          </button>
        ))}
      </div>
      {loading ? (
        <div style={{color:'#94A3B8',textAlign:'center',padding:'20px 0'}}>Загрузка...</div>
      ) : tickets.length === 0 ? (
        <div style={{color:'#94A3B8',textAlign:'center',padding:'20px 0'}}>Обращений нет</div>
      ) : (
        <>
          <div style={{fontSize:12,color:'#94A3B8',marginBottom:10}}>{total} обращений</div>
          {tickets.map(t => (
            <div key={t.id} className="ticket-row">
              <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:6}}>
                <div className="ticket-subject">{t.subject}</div>
                <span className={`ticket-status ts-${t.status}`}>{STATUS_LABELS[t.status]}</span>
              </div>
              <div className="ticket-meta">
                От: <b>{t.name}</b>
                {t.email && <> · <a href={`mailto:${t.email}`} style={{color:'#5B4FE8'}}>{t.email}</a></>}
                {t.phone && <> · {t.phone}</>}
                {' · '}{new Date(t.created_at).toLocaleString('ru-RU')}
              </div>
              <div className="ticket-msg">{t.message}</div>
              {STATUS_NEXT[t.status]?.length > 0 && (
                <div className="ticket-actions">
                  {STATUS_NEXT[t.status].map(ns => (
                    <button key={ns} className="ta-btn" onClick={() => changeStatus(t.id, ns)}
                      style={{background: ns === 'resolved' ? '#D1FAE5' : ns === 'in_progress' ? '#FEF3C7' : '#F3F4F6',
                              color: ns === 'resolved' ? '#059669' : ns === 'in_progress' ? '#92400E' : '#6B7280'}}>
                      → {STATUS_LABELS[ns]}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
        </>
      )}
    </div>
  )
}

const BRAND_ICON: Record<string, string> = { visa: '💳', mastercard: '💳' }

function cardLabel(c: { brand: string | null; last4: string | null }) {
  return `${c.brand ?? 'Карта'} •••• ${c.last4 ?? '····'}`
}

/** Buyer's saved cards. Card data lives at the acquirer — we only show the mask. */
function CardsSection() {
  const { show } = useToast()
  const [cards, setCards] = useState<SavedCard[]>([])
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)

  async function load() {
    try { setCards((await apiGetCards()).items.filter(c => c.status === 'active')) }
    catch { /* keep previous */ }
    finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  async function makeDefault(id: number) {
    await apiSetDefaultCard(id).catch(() => null)
    setCards(cs => cs.map(c => ({ ...c, is_default: c.id === id })))
    show('Карта выбрана основной')
  }

  async function remove(id: number) {
    await apiRemoveCard(id).catch(() => null)
    setCards(cs => cs.filter(c => c.id !== id))
    show('Карта удалена')
  }

  return (
    <div className="pay-section">
      {adding && (
        <AddCardModal kind="method" onClose={() => setAdding(false)} onBound={() => { load(); show('Карта успешно привязана') }} />
      )}
      <div className="pay-head">
        <h3 className="pay-title">💳 Мои карты</h3>
        <button className="pay-add" onClick={() => setAdding(true)}>+ Добавить карту</button>
      </div>
      <p className="pay-hint">
        Данные карты вводятся в защищённой форме платёжного шлюза. marqet.kz хранит только тип карты и последние 4 цифры — номер и CVC к нам не попадают.
      </p>
      {loading ? (
        <div className="pay-empty">Загрузка...</div>
      ) : cards.length === 0 ? (
        <div className="pay-empty">Нет привязанных карт. Добавьте карту, чтобы платить в один клик.</div>
      ) : (
        cards.map(c => (
          <div className="pay-card" key={c.id}>
            <div className="pay-card-icon">{BRAND_ICON[(c.brand ?? '').toLowerCase()] ?? '💳'}</div>
            <div style={{ flex: 1 }}>
              <div className="pay-card-num">{cardLabel(c)}</div>
              <div className="pay-card-exp">
                {c.exp_month && c.exp_year ? `до ${String(c.exp_month).padStart(2, '0')}/${c.exp_year}` : 'срок не указан'}
              </div>
            </div>
            {c.is_default
              ? <span className="pay-badge">основная</span>
              : <button className="pay-link" onClick={() => makeDefault(c.id)}>сделать основной</button>}
            <button className="pay-del" onClick={() => remove(c.id)} title="Удалить">✕</button>
          </div>
        ))
      )}
    </div>
  )
}

/** Seller's payout card — where marketplace proceeds are sent. */
function PayoutSection() {
  const { show } = useToast()
  const [accounts, setAccounts] = useState<PayoutAccount[]>([])
  const [payouts, setPayouts] = useState<Payout[]>([])
  const [loading, setLoading] = useState(true)
  const [adding, setAdding] = useState(false)

  async function load() {
    try {
      const [a, p] = await Promise.all([
        apiGetPayoutAccounts().catch(() => ({ items: [] as PayoutAccount[] })),
        apiGetPayouts().catch(() => ({ items: [] as Payout[] })),
      ])
      setAccounts(a.items.filter(x => x.status === 'active'))
      setPayouts(p.items)
    } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  async function makeDefault(id: number) {
    await apiSetDefaultPayoutAccount(id).catch(() => null)
    setAccounts(cs => cs.map(c => ({ ...c, is_default: c.id === id })))
    show('Карта выбрана основной для выплат')
  }

  async function remove(id: number) {
    await apiRemovePayoutAccount(id).catch(() => null)
    setAccounts(cs => cs.filter(c => c.id !== id))
    show('Реквизиты удалены')
  }

  const fmtMoney = (v: string) => Number(v).toLocaleString('ru-KZ') + ' ₸'

  return (
    <div className="pay-section">
      {adding && (
        <AddCardModal kind="payout" onClose={() => setAdding(false)} onBound={() => { load(); show('Карта для выплат привязана') }} />
      )}
      <div className="pay-head">
        <h3 className="pay-title">🏦 Карта для выплат</h3>
        <button className="pay-add" onClick={() => setAdding(true)}>+ Добавить карту</button>
      </div>
      <p className="pay-hint">
        Сюда marqet.kz перечисляет деньги за проданные товары после подтверждения сделки. Комиссия площадки удерживается автоматически.
      </p>
      {loading ? (
        <div className="pay-empty">Загрузка...</div>
      ) : accounts.length === 0 ? (
        <div className="pay-empty">Карта для выплат не добавлена — вы не сможете получить деньги за заказы.</div>
      ) : (
        accounts.map(c => (
          <div className="pay-card" key={c.id}>
            <div className="pay-card-icon">🏦</div>
            <div style={{ flex: 1 }}>
              <div className="pay-card-num">{cardLabel(c)}</div>
              <div className="pay-card-exp">
                {c.exp_month && c.exp_year ? `до ${String(c.exp_month).padStart(2, '0')}/${c.exp_year}` : 'срок не указан'}
              </div>
            </div>
            {c.is_default
              ? <span className="pay-badge">основная</span>
              : <button className="pay-link" onClick={() => makeDefault(c.id)}>сделать основной</button>}
            <button className="pay-del" onClick={() => remove(c.id)} title="Удалить">✕</button>
          </div>
        ))
      )}

      {payouts.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <div className="pay-subtitle">История выплат</div>
          {payouts.slice(0, 5).map(p => (
            <div className="payout-row" key={p.id}>
              <div>
                <div className="pay-card-num">{fmtMoney(p.net_amount)}</div>
                <div className="pay-card-exp">
                  из {fmtMoney(p.amount)} · комиссия {fmtMoney(p.commission_amount)}
                </div>
              </div>
              <span className={`payout-status payout-${p.status}`}>
                {p.status === 'sent' ? 'отправлено' : p.status === 'failed' ? 'ошибка' : 'в обработке'}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default function AccountPage() {
  const { user, logout, openNCA } = useStore()
  const nav = useNavigate()
  const { show } = useToast()
  const [listings, setListings] = useState<Listing[]>([])
  const [loading, setLoading] = useState(true)
  const [confirmId, setConfirmId] = useState<number | null>(null)
  const [editItem, setEditItem] = useState<Listing | null>(null)

  const isAdmin = user?.roles?.includes('admin') || user?.roles?.includes('warehouse_manager')
  const isSupplier = user?.roles?.includes('supplier')

  useEffect(() => {
    // Returning from the card-binding gateway (?card_added=1|0)
    const q = new URLSearchParams(window.location.search)
    if (q.has('card_added')) {
      show(q.get('card_added') === '1' ? 'Карта успешно привязана' : 'Не удалось привязать карту')
      window.history.replaceState({}, '', '/account')
    }
  }, [])

  useEffect(() => {
    if (!user) { nav('/'); return }
    apiGetMyListings()
      .then(d => setListings(d.items || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [user])

  async function handleDelete(id: number) {
    await apiDeleteListing(id).catch(() => {})
    setListings(l => l.filter(x => x.id !== id))
    setConfirmId(null)
    show('Объявление удалено')
  }

  async function toggleActive(item: Listing) {
    await apiUpdateListing(item.id, { is_active: !item.is_active }).catch(() => {})
    setListings(l => l.map(x => x.id === item.id ? { ...x, is_active: !x.is_active } : x))
    show(item.is_active ? 'Объявление скрыто' : 'Объявление активировано')
  }

  async function handleExtend(item: Listing) {
    const r = await apiExtendListing(item.id, 30).catch(() => null)
    if (r) {
      setListings(l => l.map(x => x.id === item.id ? { ...x, expires_at: r.expires_at, listing_plan: r.listing_plan } : x))
      show(r.message)
    }
  }

  async function handlePromote(item: Listing) {
    const r = await apiPromoteListing(item.id, 7).catch(() => null)
    if (r) {
      setListings(l => l.map(x => x.id === item.id ? { ...x, promoted_until: r.promoted_until, listing_plan: 'promoted' } : x))
      show(r.message)
    }
  }

  const fmt = (n: number | null) => n !== null ? n.toLocaleString('ru-KZ') + ' ₸' : 'Цена по запросу'
  const active = listings.filter(x => x.is_active && (daysLeft(x.expires_at) ?? 999) >= 0)
  const expired = listings.filter(x => x.is_active && (daysLeft(x.expires_at) ?? 999) < 0)
  const inactive = listings.filter(x => !x.is_active)

  if (!user) return null

  return (
    <>
      <style>{css}</style>
      <div className="acc-wrap">
        <div className="acc-header">
          <div className="acc-avatar">{user.name[0]?.toUpperCase()}</div>
          <div style={{flex:1}}>
            <div className="acc-name">{user.name}</div>
            <div className="acc-email">{user.email}</div>
            <div style={{display:'flex',gap:6,flexWrap:'wrap',marginTop:6}}>
              {isAdmin
                ? <span className="acc-role acc-role-admin">🛡 Администратор</span>
                : <span className="acc-role">{user.roles.includes('supplier') ? '🏪 Продавец' : '👤 Покупатель'}</span>
              }
            </div>
            {user.is_nca_verified
              ? <div className="nca-verified">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                  ИИН подтверждён
                </div>
              : <button className="nca-unverified" onClick={openNCA}>
                  ⚠ Подтвердить ИИН через ЭЦП
                </button>
            }
          </div>
          <button onClick={() => { logout(); nav('/') }} style={{padding:'8px 16px',borderRadius:10,border:'1.5px solid #E2E8F0',background:'#fff',color:'#EF4444',fontWeight:700,fontSize:13,cursor:'pointer',flexShrink:0}}>Выйти</button>
        </div>

        {isAdmin && <AdminPanel />}

        <CardsSection />
        {isSupplier && <PayoutSection />}

        <div className="stats-row">
          <div className="stat-card"><div className="stat-num">{active.length}</div><div className="stat-label">Активных</div></div>
          <div className="stat-card"><div className="stat-num" style={expired.length > 0 ? {color:'#EF4444'} : {}}>{expired.length}</div><div className="stat-label">Истекших</div></div>
          <div className="stat-card"><div className="stat-num">{inactive.length}</div><div className="stat-label">Скрытых</div></div>
        </div>

        <button className="btn-post" onClick={() => nav('/post')}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 5v14M5 12h14"/></svg>
          Подать объявление
        </button>

        {loading ? (
          <div style={{textAlign:'center',padding:'60px 0',color:'#94A3B8'}}>Загрузка...</div>
        ) : listings.length === 0 ? (
          <div className="empty-state">
            <div style={{fontSize:48,marginBottom:12}}>📋</div>
            <h3>Нет объявлений</h3>
            <p>Подайте первое объявление и начните продавать</p>
            <button className="btn-post" onClick={() => nav('/post')}>Подать объявление</button>
          </div>
        ) : (
          listings.map(item => {
            const days = daysLeft(item.expires_at)
            const isExpired = days !== null && days < 0
            const isPromoted = item.promoted_until && new Date(item.promoted_until) > new Date()
            return (
              <div key={item.id} className={`lcard ${isExpired ? 'expired' : ''} ${isPromoted ? 'promoted' : ''}`}>
                <div className="lthumb">
                  {item.image_url ? <img src={item.image_url} alt={item.product_name} /> :
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" strokeWidth="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>}
                </div>
                <div className="lbody">
                  <div style={{display:'flex',alignItems:'center',gap:6,marginBottom:4,flexWrap:'wrap'}}>
                    <div className="ltitle">{item.product_name}</div>
                    {isExpired
                      ? <span className="badge-expired">Архив</span>
                      : <span className={item.is_active ? 'badge-active' : 'badge-inactive'}>{item.is_active ? 'Активно' : 'Скрыто'}</span>
                    }
                    {isPromoted && <span className="badge-promoted">⭐ Топ</span>}
                  </div>
                  <div className="lprice">{fmt(item.unit_price)}</div>
                  <div className="lmeta">
                    {item.category && <span>{item.category}</span>}
                    {item.city && <span>{item.city}</span>}
                    <span>{new Date(item.created_at).toLocaleDateString('ru-RU')}</span>
                    {(item.view_count ?? 0) > 0 && (
                      <span className="lstat">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                        {item.view_count}
                      </span>
                    )}
                    {(item.likes_count ?? 0) > 0 && (
                      <span className="lstat">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="#EF4444" stroke="#EF4444" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                        {item.likes_count}
                      </span>
                    )}
                    <ExpiryBadge expiresAt={item.expires_at} isActive={item.is_active && !isExpired} />
                  </div>
                  <div className="lactions">
                    <button className="btn-sm btn-edit" onClick={() => setEditItem(item as any)}>✏️ Редактировать</button>
                    <Link to={`/product/${item.id}`}><button className="btn-sm btn-edit">👁 Просмотр</button></Link>
                    {!isExpired && (
                      <button className={`btn-sm ${item.is_active ? 'btn-toggle-on' : 'btn-toggle-off'}`} onClick={() => toggleActive(item)}>
                        {item.is_active ? '✓ Активно' : '○ Скрыто'}
                      </button>
                    )}
                    <button className="btn-sm btn-extend" onClick={() => handleExtend(item)} title="Продлить на 30 дней">⏱ Продлить</button>
                    {!isPromoted && (
                      <button className="btn-sm btn-promote" onClick={() => handlePromote(item)} title="Поднять в топ на 7 дней">⭐ В топ</button>
                    )}
                    <button className="btn-sm btn-del" onClick={() => setConfirmId(item.id)}>✕</button>
                  </div>
                </div>
              </div>
            )
          })
        )}
      </div>

      {confirmId !== null && (
        <div className="confirm-overlay" onClick={() => setConfirmId(null)}>
          <div className="confirm-box" onClick={e => e.stopPropagation()}>
            <div style={{fontSize:40,marginBottom:12}}>⚠️</div>
            <h3>Удалить объявление?</h3>
            <p>Это действие нельзя отменить.</p>
            <div className="confirm-btns">
              <button onClick={() => setConfirmId(null)} style={{padding:'10px 20px',borderRadius:10,background:'#F1F5F9',color:'#475569',fontWeight:700,border:'none',cursor:'pointer'}}>Отмена</button>
              <button onClick={() => handleDelete(confirmId)} style={{padding:'10px 20px',borderRadius:10,background:'#EF4444',color:'#fff',fontWeight:700,border:'none',cursor:'pointer'}}>Удалить</button>
            </div>
          </div>
        </div>
      )}

      {editItem && (
        <EditListingModal
          item={editItem}
          onClose={() => setEditItem(null)}
          onSaved={updated => setListings(l => l.map(x => x.id === updated.id ? updated : x))}
        />
      )}
    </>
  )
}
