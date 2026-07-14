import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiGetMyOrders, type AccountOrdersResponse, type MarketplaceOrderStatus } from '../../api'
import { AccountIcon, AccountShell, EmptyState, MockDataNotice, OrderStatusBadge } from './accountUi'

const fmtMoney = (value: number | null) => value == null ? 'По запросу' : `${value.toLocaleString('ru-KZ')} ₸`
const fmtDate = (value: string) => new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', year: 'numeric' }).format(new Date(value))
const PAGE_SIZE = 12

type OrderFilter = {
  key: string
  label: string
  status?: MarketplaceOrderStatus
}

const orderFilters: OrderFilter[] = [
  { key: 'all', label: 'Все' },
  { key: 'pending_payment', label: 'Ждут оплаты', status: 'pending_payment' },
  { key: 'paid', label: 'Оплачены', status: 'paid' },
  { key: 'preparing', label: 'Готовятся', status: 'preparing' },
  { key: 'shipped', label: 'В пути', status: 'shipped' },
  { key: 'delivered', label: 'Доставлены', status: 'delivered' },
  { key: 'completed', label: 'Завершены', status: 'completed' },
  { key: 'refund_requested', label: 'Возвраты', status: 'refund_requested' },
  { key: 'cancelled', label: 'Отменены', status: 'cancelled' },
]

function financeBadge(order: AccountOrdersResponse['items'][number]) {
  if (order.status === 'completed') return { label: 'Выплачено продавцу', tone: 'success' }
  if (order.status === 'refund_requested') return { label: 'Запрошен возврат', tone: 'info' }
  if (order.status === 'refunded') return { label: 'Возврат оформлен', tone: 'danger' }
  if (['paid', 'accepted', 'preparing', 'shipped', 'delivered'].includes(order.status)) {
    return { label: 'Деньги в холде', tone: 'hold' }
  }
  if (order.payment_status === 'failed') return { label: 'Оплата не прошла', tone: 'danger' }
  if (order.status === 'cancelled') return { label: 'Отменен', tone: 'danger' }
  return { label: 'Ожидает оплаты', tone: 'info' }
}

export default function OrdersPage() {
  const [data, setData] = useState<AccountOrdersResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeFilter, setActiveFilter] = useState(orderFilters[0].key)
  const [query, setQuery] = useState('')
  const [offset, setOffset] = useState(0)
  const [reloadKey, setReloadKey] = useState(0)

  const selectedFilter = orderFilters.find(filter => filter.key === activeFilter) ?? orderFilters[0]

  useEffect(() => {
    let mounted = true
    setLoading(true)
    setError('')
    apiGetMyOrders({ status: selectedFilter.status, limit: PAGE_SIZE, offset })
      .then(response => {
        if (mounted) setData(response)
      })
      .catch(e => {
        if (mounted) setError(e instanceof Error ? e.message : 'Не удалось загрузить заказы')
      })
      .finally(() => {
        if (mounted) setLoading(false)
      })
    return () => { mounted = false }
  }, [selectedFilter.status, offset, reloadKey])

  const filteredItems = useMemo(() => {
    const needle = query.trim().toLowerCase()
    if (!needle) return data?.items ?? []
    return (data?.items ?? []).filter(order => [
      order.number,
      order.product_name,
      order.supplier_name,
      order.status,
      order.payment_status,
    ].some(value => String(value ?? '').toLowerCase().includes(needle)))
  }, [data?.items, query])

  const total = data?.total ?? 0
  const hasPrevious = offset > 0
  const hasNext = offset + PAGE_SIZE < total

  function selectFilter(key: string) {
    setActiveFilter(key)
    setOffset(0)
    setQuery('')
  }

  function retry() {
    setData(null)
    setReloadKey(value => value + 1)
  }

  return (
    <AccountShell title="Мои заказы" subtitle="История покупок, статусы оплаты и доставки.">
      {data?.is_mock && <MockDataNotice unavailable={data.unavailable} />}
      <div className="acct-section acct-orders-toolbar">
        <div className="acct-filter-tabs" aria-label="Фильтр заказов по статусу">
          {orderFilters.map(filter => (
            <button
              key={filter.key}
              className={activeFilter === filter.key ? 'active' : undefined}
              type="button"
              onClick={() => selectFilter(filter.key)}
            >
              {filter.label}
            </button>
          ))}
        </div>
        <label className="acct-search">
          <AccountIcon name="search" />
          <input
            value={query}
            onChange={event => setQuery(event.target.value)}
            placeholder="Найти по номеру, товару или продавцу"
          />
        </label>
      </div>
      {loading && (
        <div className="acct-row-list" aria-busy="true">
          {Array.from({ length: 4 }).map((_, index) => <div className="acct-order-row acct-skeleton" key={index} />)}
        </div>
      )}
      {error && (
        <div className="acct-notice acct-notice-action">
          <span>{error}</span>
          <button className="acct-secondary" type="button" onClick={retry}>Повторить</button>
        </div>
      )}
      {!loading && !error && data?.items.length === 0 && (
        <EmptyState
          title="Заказов пока нет"
          text="Когда вы оформите покупку на marqet.kz, она появится в этом разделе."
          action={<Link className="acct-primary" to="/">Перейти в каталог</Link>}
        />
      )}
      {!loading && !error && data?.items.length !== 0 && filteredItems.length === 0 && (
        <EmptyState
          title="Ничего не найдено"
          text="Попробуйте изменить поиск или открыть другой статус заказов."
          action={<button className="acct-secondary" type="button" onClick={() => setQuery('')}>Сбросить поиск</button>}
        />
      )}
      <div className="acct-row-list">
        {!loading && !error && filteredItems.map(order => {
          const badge = financeBadge(order)
          return (
            <Link className="acct-order-row" to={`/account/orders/${order.id}`} key={order.id}>
              <div>
                <strong>{order.number}</strong>
                <span>{order.product_name ?? `${order.items_count} товар(ов)`}</span>
                <div className="acct-order-meta">{order.supplier_name ?? 'Поставщик'} · {fmtDate(order.created_at)}</div>
              </div>
              <div className="acct-order-badges">
                <OrderStatusBadge status={order.status} />
                <span className={`acct-finance-badge acct-finance-${badge.tone}`}>{badge.label}</span>
              </div>
              <div className="acct-money">{fmtMoney(order.total_amount)}</div>
            </Link>
          )
        })}
      </div>
      {!loading && !error && total > PAGE_SIZE && (
        <div className="acct-pagination">
          <span>{offset + 1}-{Math.min(offset + PAGE_SIZE, total)} из {total}</span>
          <div>
            <button className="acct-secondary" type="button" disabled={!hasPrevious} onClick={() => setOffset(value => Math.max(0, value - PAGE_SIZE))}>Назад</button>
            <button className="acct-secondary" type="button" disabled={!hasNext} onClick={() => setOffset(value => value + PAGE_SIZE)}>Дальше</button>
          </div>
        </div>
      )}
    </AccountShell>
  )
}
