import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { apiCreateMarketplacePayment, apiGetOrder, type MarketplaceOrderDetail, type MarketplacePayment } from '../../api'
import { AccountIcon, AccountShell, EmptyState, MockDataNotice, OrderStatusBadge } from './accountUi'
import { useToast } from '../../components/Toast'

const fmtMoney = (value: number | null) => value == null ? 'По запросу' : `${value.toLocaleString('ru-KZ')} ₸`
const fmtDateTime = (value: string) => new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', hour: '2-digit', minute: '2-digit' }).format(new Date(value))

const paymentLabels: Record<MarketplacePayment['status'], string> = {
  pending: 'Ожидает подтверждения',
  requires_action: 'Требуется действие',
  authorized: 'Авторизован',
  paid: 'Оплачен',
  failed: 'Не прошел',
  cancelled: 'Отменен',
  refunded: 'Возвращен',
}

const canRetryPayment = (order: MarketplaceOrderDetail) =>
  order.status === 'pending_payment' && (!order.latest_payment || ['pending', 'failed', 'cancelled'].includes(order.latest_payment.status))

export default function OrderDetailPage() {
  const params = useParams()
  const orderId = Number(params.id)
  const { show } = useToast()
  const [order, setOrder] = useState<MarketplaceOrderDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [paying, setPaying] = useState(false)

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

  async function retryPayment() {
    if (!order || paying) return
    setPaying(true)
    try {
      const payment = await apiCreateMarketplacePayment(order.id, { provider: 'manual_card' })
      setOrder({ ...order, latest_payment: payment, payment_status: payment.status })
      show('Платежная попытка создана')
      if (payment.payment_url) {
        window.location.assign(payment.payment_url)
      }
    } catch (e) {
      show(e instanceof Error ? e.message : 'Не удалось создать платеж', 'error')
    } finally {
      setPaying(false)
    }
  }

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
            <h2>Оплата</h2>
            <div className="acct-payment-status">
              <div>
                <strong>{order.latest_payment ? paymentLabels[order.latest_payment.status] : 'Платеж еще не создан'}</strong>
                <span>
                  {order.latest_payment
                    ? `${order.latest_payment.provider} · ${fmtMoney(order.latest_payment.amount)}`
                    : 'Создайте платежную попытку, чтобы продолжить оплату после подключения провайдера.'}
                </span>
              </div>
              {order.latest_payment?.payment_url ? (
                <a className="acct-primary" href={order.latest_payment.payment_url}>Перейти к оплате</a>
              ) : (
                <button className="acct-primary" type="button" onClick={retryPayment} disabled={!canRetryPayment(order) || paying}>
                  {paying ? 'Создаем...' : 'Повторить оплату'}
                </button>
              )}
            </div>
            <p style={{ marginTop: 12 }}>
              marqet.kz не хранит номер карты и CVV. Статус оплаты меняется только после защищенного подтверждения платежного провайдера.
            </p>
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
