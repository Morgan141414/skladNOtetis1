import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  apiGetSupplierMarketplaceOrder,
  apiGetSupplierMarketplaceOrders,
  apiUpdateSupplierMarketplaceOrderStatus,
  type MarketplaceOrderDetail,
  type MarketplaceOrderListItem,
  type MarketplaceOrderStatus,
  type SupplierMarketplaceOrderNextStatus,
} from '../../api'
import { OrderStatusBadge } from '../account/accountUi'
import { useToast } from '../../components/Toast'
import './seller.css'

const fmtMoney = (value: number | null) => value == null ? 'По запросу' : `${value.toLocaleString('ru-KZ')} ₸`
const fmtDate = (value: string) => new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', hour: '2-digit', minute: '2-digit' }).format(new Date(value))
const PAGE_SIZE = 20

const nextActions: Partial<Record<MarketplaceOrderStatus, { status: SupplierMarketplaceOrderNextStatus; label: string }[]>> = {
  pending: [{ status: 'accepted', label: 'Принять' }, { status: 'cancelled', label: 'Отменить' }],
  pending_payment: [{ status: 'cancelled', label: 'Отменить' }],
  paid: [{ status: 'accepted', label: 'Принять' }, { status: 'cancelled', label: 'Отменить' }],
  accepted: [{ status: 'preparing', label: 'В подготовку' }, { status: 'cancelled', label: 'Отменить' }],
  preparing: [{ status: 'shipped', label: 'Отправлен' }, { status: 'cancelled', label: 'Отменить' }],
  shipped: [{ status: 'delivered', label: 'Доставлен' }],
  delivered: [{ status: 'completed', label: 'Завершить' }],
}

const statusFilters: Array<{ key: string; label: string; status?: MarketplaceOrderStatus }> = [
  { key: 'all', label: 'Все' },
  { key: 'pending_payment', label: 'Ждут оплаты', status: 'pending_payment' },
  { key: 'paid', label: 'Оплачены', status: 'paid' },
  { key: 'accepted', label: 'Приняты', status: 'accepted' },
  { key: 'preparing', label: 'Готовятся', status: 'preparing' },
  { key: 'shipped', label: 'В пути', status: 'shipped' },
  { key: 'completed', label: 'Завершены', status: 'completed' },
  { key: 'refund_requested', label: 'Возвраты', status: 'refund_requested' },
  { key: 'refunded', label: 'Возвращены', status: 'refunded' },
  { key: 'cancelled', label: 'Отменены', status: 'cancelled' },
]

const paymentStatusLabels: Record<string, string> = {
  unpaid: 'Не оплачен',
  pending: 'Платеж создан',
  requires_action: 'Требует подтверждения',
  authorized: 'Авторизован',
  paid: 'Оплачен',
  failed: 'Ошибка оплаты',
  cancelled: 'Платеж отменен',
  refunded: 'Возврат',
}

const mergeUniqueOrders = (current: MarketplaceOrderListItem[], next: MarketplaceOrderListItem[]) => {
  const seen = new Set<number>()
  return [...current, ...next].filter(order => {
    if (seen.has(order.id)) return false
    seen.add(order.id)
    return true
  })
}

export default function SellerOrdersPage() {
  const { show } = useToast()
  const [searchParams] = useSearchParams()
  const [orders, setOrders] = useState<MarketplaceOrderListItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState<number | null>(null)
  const [activeFilter, setActiveFilter] = useState(statusFilters[0].key)
  const [offset, setOffset] = useState(0)
  const [details, setDetails] = useState<Record<number, MarketplaceOrderDetail>>({})
  const [openDetailId, setOpenDetailId] = useState<number | null>(null)
  const [detailLoadingId, setDetailLoadingId] = useState<number | null>(null)

  const selectedFilter = statusFilters.find(filter => filter.key === activeFilter) ?? statusFilters[0]
  const requestedOrderId = Number(searchParams.get('order_id'))

  async function load(nextOffset = 0) {
    setError('')
    try {
      const result = await apiGetSupplierMarketplaceOrders({ status: selectedFilter.status, limit: PAGE_SIZE, offset: nextOffset })
      setOrders(items => nextOffset === 0 ? result.items : mergeUniqueOrders(items, result.items))
      setTotal(result.total)
      if (nextOffset === 0 && Number.isFinite(requestedOrderId) && requestedOrderId > 0) {
        const found = result.items.find(item => item.id === requestedOrderId)
        if (found) {
          setOpenDetailId(found.id)
          if (!details[found.id]) {
            const detail = await apiGetSupplierMarketplaceOrder(found.id)
            setDetails(current => ({ ...current, [found.id]: detail }))
          }
        } else if (!selectedFilter.status) {
          const detail = await apiGetSupplierMarketplaceOrder(requestedOrderId)
          setDetails(current => ({ ...current, [requestedOrderId]: detail }))
          setOrders(items => items.some(item => item.id === requestedOrderId) ? items : [detail, ...items])
          setOpenDetailId(requestedOrderId)
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Не удалось загрузить заказы продавца')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    setLoading(true)
    setOffset(0)
    setOpenDetailId(null)
    void load(0)
  }, [selectedFilter.status, requestedOrderId])

  async function updateStatus(order: MarketplaceOrderListItem, status: SupplierMarketplaceOrderNextStatus) {
    const cancelReason = status === 'cancelled' ? window.prompt('Причина отмены заказа')?.trim() : undefined
    if (status === 'cancelled' && !cancelReason) return
    setBusyId(order.id)
    try {
      const updated = await apiUpdateSupplierMarketplaceOrderStatus(order.id, { status, cancel_reason: cancelReason })
      setOrders(items => items.map(item => item.id === order.id ? { ...item, status: updated.status, updated_at: updated.updated_at } : item))
      setDetails(current => current[order.id] ? { ...current, [order.id]: updated } : current)
      show('Статус заказа обновлен')
    } catch (e) {
      show(e instanceof Error ? e.message : 'Не удалось обновить статус', 'error')
    } finally {
      setBusyId(null)
    }
  }

  async function toggleDetails(order: MarketplaceOrderListItem) {
    if (openDetailId === order.id) {
      setOpenDetailId(null)
      return
    }
    setOpenDetailId(order.id)
    if (details[order.id]) return
    setDetailLoadingId(order.id)
    try {
      const detail = await apiGetSupplierMarketplaceOrder(order.id)
      setDetails(current => ({ ...current, [order.id]: detail }))
    } catch (e) {
      show(e instanceof Error ? e.message : 'Не удалось загрузить детали заказа', 'error')
      setOpenDetailId(null)
    } finally {
      setDetailLoadingId(null)
    }
  }

  async function loadMore() {
    const nextOffset = offset + PAGE_SIZE
    await load(nextOffset)
    setOffset(nextOffset)
  }

  function selectFilter(key: string) {
    setActiveFilter(key)
  }

  const hasMore = orders.length < total

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
          <Link className="seller-primary" to="/account/listings">Мои объявления</Link>
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

      <section className="seller-section seller-orders-toolbar">
        <div className="seller-filter-tabs" aria-label="Фильтр заказов продавца">
          {statusFilters.map(filter => (
            <button
              type="button"
              key={filter.key}
              className={activeFilter === filter.key ? 'active' : undefined}
              onClick={() => selectFilter(filter.key)}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </section>

      {orders.length > 0 && (
        <section className="seller-section">
          <div className="seller-section-head">
            <h2>Всего заказов: {total}</h2>
            <span>Показано {orders.length}</span>
          </div>
          <div className="seller-order-list">
            {orders.map(order => {
              const detail = details[order.id]
              return (
                <div className="seller-order-item" key={order.id}>
                  <article className="seller-order-row">
                    <div>
                      <strong>{order.number}</strong>
                      <span>{order.product_name ?? `${order.items_count} товар(ов)`}</span>
                      <small>{fmtDate(order.created_at)} · {paymentStatusLabels[order.payment_status ?? 'unpaid'] ?? order.payment_status ?? 'Не оплачен'}</small>
                    </div>
                    <OrderStatusBadge status={order.status} />
                    <div className="seller-money">{fmtMoney(order.total_amount)}</div>
                    <div className="seller-actions">
                      <button className="seller-secondary" type="button" onClick={() => toggleDetails(order)} disabled={detailLoadingId === order.id}>
                        {openDetailId === order.id ? 'Скрыть' : detailLoadingId === order.id ? 'Загрузка...' : 'Подробнее'}
                      </button>
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
                  {openDetailId === order.id && detail && (
                    <section className="seller-order-detail">
                      <div className="seller-detail-grid">
                        <div>
                          <h3>Покупатель</h3>
                          <p>{detail.buyer_name || 'Имя не указано'}</p>
                          <p>{detail.buyer_phone || 'Телефон не указан'}{detail.buyer_email ? ` · ${detail.buyer_email}` : ''}</p>
                        </div>
                        <div>
                          <h3>Доставка</h3>
                          <p>{detail.delivery_address || 'Адрес доставки пока не указан.'}</p>
                          {detail.notes && <p>{detail.notes}</p>}
                        </div>
                        <div>
                          <h3>Оплата</h3>
                          <p>{detail.latest_payment ? `${paymentStatusLabels[detail.latest_payment.status] ?? detail.latest_payment.status} · ${fmtMoney(detail.latest_payment.amount)}` : 'Платеж еще не создан'}</p>
                          <p>{detail.latest_payment?.provider ?? 'Провайдер не указан'}</p>
                        </div>
                      </div>
                      <div className="seller-detail-columns">
                        <div>
                          <h3>Состав заказа</h3>
                          <div className="seller-detail-items">
                            {detail.items.map(item => (
                              <div className="seller-detail-item" key={item.id}>
                                <div className="seller-detail-thumb">
                                  {item.image_url ? <img src={item.image_url} alt={item.product_name} /> : <span />}
                                </div>
                                <div>
                                  <strong>{item.product_name}</strong>
                                  <span>{item.quantity} {item.unit ?? 'шт'} · {fmtMoney(item.unit_price)}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                        <div>
                          <h3>История</h3>
                          <div className="seller-detail-timeline">
                            {detail.timeline.map(step => (
                              <div className="seller-detail-step" key={step.id}>
                                <strong>{step.title}</strong>
                                <span>{step.description}</span>
                                <small>{fmtDate(step.created_at)}</small>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </section>
                  )}
                </div>
              )
            })}
          </div>
          {hasMore && (
            <div className="seller-load-more">
              <button className="seller-secondary" type="button" onClick={loadMore} disabled={loading}>Показать еще</button>
            </div>
          )}
        </section>
      )}
    </main>
  )
}
