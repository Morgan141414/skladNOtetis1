import { Link, NavLink } from 'react-router-dom'
import { useStore } from '../../store'
import type { MarketplaceOrderStatus, PaymentMethod } from '../../api'
import './account.css'

const navItems = [
  { to: '/account/hub', label: 'Обзор', icon: 'grid' },
  { to: '/account/orders', label: 'Заказы', icon: 'box' },
  { to: '/account/payment-methods', label: 'Оплата', icon: 'card' },
  { to: '/account/loyalty', label: 'Бонусы', icon: 'star' },
  { to: '/messages', label: 'Поддержка', icon: 'message' },
  { to: '/account', label: 'Объявления', icon: 'tag' },
]

export function AccountIcon({ name, size = 18 }: { name: string; size?: number }) {
  const common = { width: size, height: size, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const }
  if (name === 'box') return <svg {...common}><path d="m21 8-9-5-9 5 9 5 9-5Z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>
  if (name === 'card') return <svg {...common}><rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3 10h18"/><path d="M7 15h4"/></svg>
  if (name === 'star') return <svg {...common}><path d="m12 3 2.7 5.5 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3Z"/></svg>
  if (name === 'message') return <svg {...common}><path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z"/></svg>
  if (name === 'tag') return <svg {...common}><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8Z"/><path d="M7.5 7.5h.01"/></svg>
  if (name === 'check') return <svg {...common}><path d="m20 6-11 11-5-5"/></svg>
  if (name === 'clock') return <svg {...common}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
  if (name === 'alert') return <svg {...common}><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>
  return <svg {...common}><rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/></svg>
}

export function AccountShell({ title, subtitle, children, actions }: { title: string; subtitle?: string; children: React.ReactNode; actions?: React.ReactNode }) {
  const { user, openAuth } = useStore()

  if (!user) {
    return (
      <div className="acct-wrap">
        <div className="acct-auth">
          <div className="acct-auth-icon"><AccountIcon name="grid" size={30} /></div>
          <h1>Войдите в аккаунт</h1>
          <p>Личный кабинет покупателя доступен после авторизации.</p>
          <button onClick={() => openAuth('login')} className="acct-primary">Войти</button>
        </div>
      </div>
    )
  }

  return (
    <div className="acct-wrap">
      <div className="acct-head">
        <div>
          <p className="acct-eyebrow">Личный кабинет</p>
          <h1>{title}</h1>
          {subtitle && <p>{subtitle}</p>}
        </div>
        <div className="acct-head-actions">{actions}</div>
      </div>
      <div className="acct-layout">
        <aside className="acct-side" aria-label="Навигация личного кабинета">
          <div className="acct-user">
            <div className="acct-avatar">{user.name?.[0]?.toUpperCase() ?? 'M'}</div>
            <div>
              <strong>{user.name}</strong>
              <span>{user.email}</span>
            </div>
          </div>
          <nav className="acct-nav">
            {navItems.map(item => (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => isActive ? 'active' : undefined}>
                <AccountIcon name={item.icon} />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </aside>
        <main className="acct-main">{children}</main>
      </div>
    </div>
  )
}

export function MockDataNotice({ unavailable }: { unavailable?: boolean }) {
  return (
    <div className="acct-notice">
      <AccountIcon name={unavailable ? 'clock' : 'alert'} />
      <span>{unavailable ? 'Backend для этого раздела готовится. Показан безопасный шаблон интерфейса.' : 'Показаны демо-данные для проверки интерфейса.'}</span>
    </div>
  )
}

export function AccountStatCard({ label, value, icon, hint, to }: { label: string; value: string | number; icon: string; hint?: string; to?: string }) {
  const body = (
    <>
      <span className="acct-stat-icon"><AccountIcon name={icon} /></span>
      <strong>{value}</strong>
      <span>{label}</span>
      {hint && <small>{hint}</small>}
    </>
  )
  return to ? <Link to={to} className="acct-stat">{body}</Link> : <div className="acct-stat">{body}</div>
}

export function OrderStatusBadge({ status }: { status: MarketplaceOrderStatus }) {
  const labels: Record<MarketplaceOrderStatus, string> = {
    draft: 'Черновик',
    pending_payment: 'Ожидает оплаты',
    paid: 'Оплачен',
    accepted: 'Принят',
    preparing: 'Готовится',
    shipped: 'В пути',
    delivered: 'Доставлен',
    completed: 'Завершен',
    cancelled: 'Отменен',
    refund_requested: 'Запрошен возврат',
    refunded: 'Возврат',
  }
  const tone = ['cancelled', 'refunded'].includes(status) ? 'danger' : ['delivered', 'completed', 'paid'].includes(status) ? 'success' : 'info'
  return <span className={`acct-badge acct-badge-${tone}`}>{labels[status]}</span>
}

export function PaymentCard({ method }: { method: PaymentMethod }) {
  return (
    <div className="acct-payment-card">
      <div className="acct-payment-mark">{method.brand.toUpperCase()}</div>
      <div>
        <strong>{method.brand === 'kaspi' ? 'Kaspi token' : `Карта заканчивается на ${method.last4}`}</strong>
        <span>{method.expiry_month && method.expiry_year ? `До ${String(method.expiry_month).padStart(2, '0')}/${method.expiry_year}` : 'Токенизированный способ оплаты'}</span>
      </div>
      {method.is_default && <span className="acct-badge acct-badge-success">Основная</span>}
    </div>
  )
}

export function EmptyState({ title, text, action }: { title: string; text: string; action?: React.ReactNode }) {
  return (
    <div className="acct-empty">
      <AccountIcon name="box" size={34} />
      <h2>{title}</h2>
      <p>{text}</p>
      {action}
    </div>
  )
}
