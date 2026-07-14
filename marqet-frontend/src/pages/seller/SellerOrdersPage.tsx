import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  apiGetSupplierMarketplaceOrders,
  apiUpdateSupplierMarketplaceOrderStatus,
  type MarketplaceOrderListItem,
  type MarketplaceOrderStatus,
  type SupplierMarketplaceOrderNextStatus,
} from '../../api'
import { OrderStatusBadge } from '../account/accountUi'
import { useToast } from '../../components/Toast'
import './seller.css'

const fmtMoney = (value: number | null) => value == null ? 'По запросу' : `${value.toLocaleString('ru-KZ')} ₸`
const fmtDate = (value: string) => new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', hour: '2-digit', minute: '2-digit' }).format(new Date(value))

const nextActions: Partial<Record<MarketplaceOrderStatus, { status: SupplierMarketplaceOrderNextStatus; label: string }[]>> = {
  pending: [{ status: 'accepted', label: 'Принять' }, { status: 'cancelled', label: 'Отменить' }],
  pending_payment: [{ status: 'cancelled', label: 'Отменить' }],
  paid: [{ status: 'accepted', label: 'Принять' }, { status: 'cancelled', label: 'Отменить' }],
  accepted: [{ status: 'preparing', label: 'В подготовку' }, { status: 'cancelled', label: 'Отменить' }],
  preparing: [{ status: 'shipped', label: 'Отправлен' }, { status: 'cancelled', label: 'Отменить' }],
  shipped: [{ status: 'delivered', label: 'Доставлен' }],
  delivered: [{ status: 'completed', label: 'Завершить' }],
}

export default function SellerOrdersPage() {
  const { show } = useToast()
  const [orders, setOrders] = useState<MarketplaceOrderListItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState<number | null>(null)

  async function load() {
    setError('')
    try {
      const result = await apiGetSupplierMarketplaceOrders({ limit: 80 })
      setOrders(result.items)
      setTotal(result.total)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Не удалось загрузить заказы продавца')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { void load() }, [])

  async function updateStatus(order: MarketplaceOrderListItem, status: SupplierMarketplaceOrderNextStatus) {
    const cancelReason = status === 'cancelled' ? window.prompt('Причина отмены заказа')?.trim() : undefined
    if (status === 'cancelled' && !cancelReason) return
    setBusyId(order.id)
    try {
      const updated = await apiUpdateSupplierMarketplaceOrderStatus(order.id, { status, cancel_reason: cancelReason })
      setOrders(items => items.map(item => item.id === order.id ? { ...item, status: updated.status, updated_at: updated.updated_at } : item))
      show('Статус заказа обновлен')
    } catch (e) {
      show(e instanceof Error ? e.message : 'Не удалось обновить статус', 'error')
    } finally {
      setBusyId(null)
    }
  }

  return (
    <main className="seller-wrap">
      <section className="seller-head">
        <div>
          <div className="seller-eyebrow">Кабинет продавца</div>
          <h1>Заказы маркетплейса</h1>
          <p>Принимайте заказы, отмечайте отправку и завершение. Деньги переходят из холда в доступный баланс только после завершения.</p>
        </div>
        <div className="seller-head-actions">
          <Link className="seller-secondary" to="/seller/wallet">Кошелек</Link>
          <Link className="seller-primary" to="/account">Мои объявления</Link>
        </div>
      </section>

      {loading && <section className="seller-section"><p>Загрузка заказов...</p></section>}
      {error && <section className="seller-alert">{error}</section>}
      {!loading && !error && orders.length === 0 && (
        <section className="seller-empty">
          <h2>Заказов пока нет</h2>
          <p>Когда покупатель оформит товар у вашего поставщика, заказ появится здесь.</p>
        </section>
      )}

      {orders.length > 0 && (
        <section className="seller-section">
          <div className="seller-section-head">
            <h2>Всего заказов: {total}</h2>
          </div>
          <div className="seller-order-list">
            {orders.map(order => (
              <article className="seller-order-row" key={order.id}>
                <div>
                  <strong>{order.number}</strong>
                  <span>{order.product_name ?? `${order.items_count} товар(ов)`}</span>
                  <small>{fmtDate(order.created_at)} · {order.payment_status ?? 'unpaid'}</small>
                </div>
                <OrderStatusBadge status={order.status} />
                <div className="seller-money">{fmtMoney(order.total_amount)}</div>
                <div className="seller-actions">
                  {(nextActions[order.status] ?? []).map(action => (
                    <button
                      className={action.status === 'cancelled' ? 'seller-danger' : 'seller-secondary'}
                      type="button"
                      key={action.status}
                      disabled={busyId === order.id}
                      onClick={() => updateStatus(order, action.status)}
                    >
                      {action.label}
                    </button>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  )
}
