import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { apiGetOrder, type MarketplaceOrderDetail } from '../../api'
import { AccountIcon, AccountShell, EmptyState, MockDataNotice, OrderStatusBadge } from './accountUi'

const fmtMoney = (value: number | null) => value == null ? 'По запросу' : `${value.toLocaleString('ru-KZ')} ₸`
const fmtDateTime = (value: string) => new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', hour: '2-digit', minute: '2-digit' }).format(new Date(value))

export default function OrderDetailPage() {
  const params = useParams()
  const orderId = Number(params.id)
  const [order, setOrder] = useState<MarketplaceOrderDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!Number.isFinite(orderId)) {
      setError('Некорректный номер заказа')
      setLoading(false)
      return
    }
    apiGetOrder(orderId)
      .then(setOrder)
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить заказ'))
      .finally(() => setLoading(false))
  }, [orderId])

  return (
    <AccountShell
      title={order ? `Заказ ${order.number}` : 'Детали заказа'}
      subtitle="Состав заказа, доставка и история статусов."
      actions={<Link className="acct-secondary" to="/account/orders">Назад к заказам</Link>}
    >
      {order?.is_mock && <MockDataNotice unavailable={order.unavailable} />}
      {loading && <div className="acct-section"><p>Загрузка заказа...</p></div>}
      {error && <EmptyState title="Заказ не найден" text={error} action={<Link className="acct-primary" to="/account/orders">К списку заказов</Link>} />}
      {order && (
        <>
          <section className="acct-section acct-detail-top">
            <div>
              <h2>{order.product_name ?? 'Заказ marqet.kz'}</h2>
              <p>{order.supplier_name ?? 'Поставщик'} · {fmtDateTime(order.created_at)}</p>
            </div>
            <div style={{display:'grid',gap:10,justifyItems:'end'}}>
              <OrderStatusBadge status={order.status} />
              <div className="acct-money">{fmtMoney(order.total_amount)}</div>
            </div>
          </section>

          <section className="acct-section">
            <h2>Товары</h2>
            <div className="acct-items">
              {order.items.map(item => (
                <div className="acct-item" key={item.id}>
                  <div className="acct-item-img">
                    {item.image_url ? <img src={item.image_url} alt={item.product_name} /> : <AccountIcon name="box" />}
                  </div>
                  <div>
                    <strong>{item.product_name}</strong>
                    <div className="acct-order-meta">{item.quantity} {item.unit ?? 'шт'}</div>
                  </div>
                  <div className="acct-money">{fmtMoney(item.unit_price)}</div>
                </div>
              ))}
            </div>
          </section>

          <section className="acct-section">
            <h2>Доставка и контакт</h2>
            <p>{order.delivery_address ?? 'Адрес доставки пока не указан.'}</p>
            <p>{order.buyer_name ?? 'Покупатель'} {order.buyer_phone ? `· ${order.buyer_phone}` : ''}</p>
            {order.notes && <p>{order.notes}</p>}
          </section>

          <section className="acct-section">
            <h2>История заказа</h2>
            <div className="acct-timeline">
              {order.timeline.map(step => (
                <div className="acct-timeline-step" key={step.id}>
                  <div className="acct-dot"><AccountIcon name="check" size={14} /></div>
                  <div>
                    <strong>{step.title}</strong>
                    {step.description && <p>{step.description}</p>}
                    <span className="acct-order-meta">{fmtDateTime(step.created_at)}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </>
      )}
    </AccountShell>
  )
}
