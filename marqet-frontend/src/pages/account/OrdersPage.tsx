import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiGetMyOrders, type AccountOrdersResponse } from '../../api'
import { AccountShell, EmptyState, MockDataNotice, OrderStatusBadge } from './accountUi'

const fmtMoney = (value: number | null) => value == null ? 'По запросу' : `${value.toLocaleString('ru-KZ')} ₸`
const fmtDate = (value: string) => new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', year: 'numeric' }).format(new Date(value))

export default function OrdersPage() {
  const [data, setData] = useState<AccountOrdersResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    apiGetMyOrders({ limit: 50 })
      .then(setData)
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить заказы'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <AccountShell title="Мои заказы" subtitle="История покупок, статусы оплаты и доставки.">
      {data?.is_mock && <MockDataNotice unavailable={data.unavailable} />}
      {loading && <div className="acct-section"><p>Загрузка заказов...</p></div>}
      {error && <div className="acct-notice">{error}</div>}
      {!loading && !error && data?.items.length === 0 && (
        <EmptyState
          title="Заказов пока нет"
          text="Когда вы оформите покупку на marqet.kz, она появится в этом разделе."
          action={<Link className="acct-primary" to="/">Перейти в каталог</Link>}
        />
      )}
      <div className="acct-row-list">
        {data?.items.map(order => (
          <Link className="acct-order-row" to={`/account/orders/${order.id}`} key={order.id}>
            <div>
              <strong>{order.number}</strong>
              <span>{order.product_name ?? `${order.items_count} товар(ов)`}</span>
              <div className="acct-order-meta">{order.supplier_name ?? 'Поставщик'} · {fmtDate(order.created_at)}</div>
            </div>
            <OrderStatusBadge status={order.status} />
            <div className="acct-money">{fmtMoney(order.total_amount)}</div>
          </Link>
        ))}
      </div>
    </AccountShell>
  )
}
