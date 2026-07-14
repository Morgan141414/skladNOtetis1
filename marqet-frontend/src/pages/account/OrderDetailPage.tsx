import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import {
  apiCancelMarketplaceOrder,
  apiCreateMarketplacePayment,
  apiGetOrder,
  apiGetPaymentMethods,
  apiRequestMarketplaceRefund,
  type MarketplaceOrderDetail,
  type MarketplacePayment,
  type PaymentMethod,
} from '../../api'
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

const canCancelOrder = (order: MarketplaceOrderDetail) =>
  ['draft', 'pending_payment'].includes(order.status)

const canRequestRefund = (order: MarketplaceOrderDetail) =>
  ['paid', 'accepted', 'preparing', 'shipped', 'delivered', 'completed'].includes(order.status)

const escrowText = (order: MarketplaceOrderDetail) => {
  if (order.status === 'completed') return 'Деньги переданы продавцу после завершения заказа.'
  if (['paid', 'accepted', 'preparing', 'shipped', 'delivered'].includes(order.status)) {
    return 'Деньги зарезервированы marqet.kz и будут доступны продавцу после завершения заказа.'
  }
  if (order.status === 'refund_requested') return 'Запрос на возврат принят. Возврат будет проведен через платежного провайдера.'
  if (order.status === 'refunded') return 'Возврат по заказу оформлен.'
  return 'Покупка защищена: продавец получает деньги только после завершения заказа.'
}

export default function OrderDetailPage() {
  const params = useParams()
  const orderId = Number(params.id)
  const { show } = useToast()
  const [order, setOrder] = useState<MarketplaceOrderDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [paying, setPaying] = useState(false)
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([])
  const [selectedPaymentMethodId, setSelectedPaymentMethodId] = useState('')
  const [orderAction, setOrderAction] = useState<'cancel' | 'refund' | ''>('')
  const [reason, setReason] = useState('')
  const [actionSaving, setActionSaving] = useState(false)

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
    apiGetPaymentMethods()
      .then(data => {
        const active = data.items.filter(method => method.status === 'active')
        setPaymentMethods(active)
        const primary = active.find(method => method.is_default) ?? active[0]
        if (primary) setSelectedPaymentMethodId(primary.id)
      })
      .catch(() => setPaymentMethods([]))
  }, [orderId])

  async function retryPayment() {
    if (!order || paying) return
    setPaying(true)
    try {
      const selected = paymentMethods.find(method => method.id === selectedPaymentMethodId)
      const payment = await apiCreateMarketplacePayment(order.id, {
        provider: selected?.provider ?? 'manual_invoice',
        payment_method_id: selected ? Number(selected.id) : null,
      })
      setOrder({ ...order, latest_payment: payment, payment_status: payment.status })
      show(selected ? 'Платеж создан по сохраненному способу' : 'Платеж создан как счет для ручного подтверждения')
      if (payment.payment_url) {
        window.location.assign(payment.payment_url)
      }
    } catch (e) {
      show(e instanceof Error ? e.message : 'Не удалось создать платеж', 'error')
    } finally {
      setPaying(false)
    }
  }

  async function submitOrderAction(action: 'cancel' | 'refund') {
    if (!order || actionSaving) return
    const trimmed = reason.trim()
    if (trimmed.length < 3) {
      show('Укажите причину минимум из 3 символов', 'error')
      return
    }
    setActionSaving(true)
    try {
      const updated = action === 'cancel'
        ? await apiCancelMarketplaceOrder(order.id, trimmed)
        : await apiRequestMarketplaceRefund(order.id, trimmed)
      setOrder(updated)
      setOrderAction('')
      setReason('')
      show(action === 'cancel' ? 'Заказ отменен' : 'Запрос на возврат отправлен')
    } catch (e) {
      show(e instanceof Error ? e.message : 'Не удалось выполнить действие', 'error')
    } finally {
      setActionSaving(false)
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
                    : paymentMethods.length > 0
                      ? 'Выберите сохраненный токенизированный способ оплаты или создайте счет для ручного подтверждения.'
                      : 'Сохраненных способов оплаты нет. Можно создать счет для ручного подтверждения.'}
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
            {!order.latest_payment && canRetryPayment(order) && paymentMethods.length > 0 && (
              <div className="acct-row-list" style={{ marginTop: 12 }}>
                {paymentMethods.map(method => (
                  <button
                    key={method.id}
                    className={`acct-secondary ${selectedPaymentMethodId === method.id ? 'active' : ''}`}
                    type="button"
                    onClick={() => setSelectedPaymentMethodId(method.id)}
                    style={{ justifyContent: 'space-between' }}
                  >
                    <span>{method.brand.toUpperCase()} · {method.last4}</span>
                    {method.is_default && <span>Основной</span>}
                  </button>
                ))}
              </div>
            )}
            <p style={{ marginTop: 12 }}>
              {escrowText(order)}
            </p>
          </section>

          {(canCancelOrder(order) || canRequestRefund(order) || order.status === 'refund_requested') && (
            <section className="acct-section">
              <h2>Действия с заказом</h2>
              {order.status === 'refund_requested' ? (
                <p>Запрос на возврат уже отправлен. Мы обновим статус после обработки платежным провайдером.</p>
              ) : (
                <>
                  <div className="acct-actions">
                    {canCancelOrder(order) && (
                      <button className="acct-secondary" type="button" onClick={() => setOrderAction('cancel')}>
                        Отменить заказ
                      </button>
                    )}
                    {canRequestRefund(order) && (
                      <button className="acct-secondary" type="button" onClick={() => setOrderAction('refund')}>
                        Запросить возврат
                      </button>
                    )}
                  </div>
                  {orderAction && (
                    <div className="acct-reason-box">
                      <label>
                        Причина
                        <textarea
                          value={reason}
                          onChange={event => setReason(event.target.value)}
                          rows={3}
                          placeholder={orderAction === 'cancel' ? 'Например, изменились планы' : 'Опишите, почему нужен возврат'}
                        />
                      </label>
                      <div className="acct-actions">
                        <button
                          className="acct-primary"
                          type="button"
                          onClick={() => submitOrderAction(orderAction)}
                          disabled={actionSaving}
                        >
                          {actionSaving ? 'Отправляем...' : orderAction === 'cancel' ? 'Подтвердить отмену' : 'Отправить запрос'}
                        </button>
                        <button className="acct-secondary" type="button" onClick={() => setOrderAction('')} disabled={actionSaving}>
                          Не сейчас
                        </button>
                      </div>
                    </div>
                  )}
                </>
              )}
            </section>
          )}

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
