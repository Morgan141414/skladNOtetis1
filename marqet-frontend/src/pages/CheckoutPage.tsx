import { FormEvent, useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  apiCheckoutMarketplaceOrders,
  apiCreateMarketplacePayment,
  apiGetCart,
  apiGetPaymentMethods,
  apiInstallmentOptions,
  type Cart,
  type InstallmentPlan,
  type MarketplaceOrderDetail,
  type MarketplacePayment,
  type PaymentMethod,
} from '../api'
import { useStore } from '../store'
import { useToast } from '../components/Toast'

const css = `
.checkout-wrap { max-width:1120px; margin:0 auto; padding:28px 20px 70px; }
.checkout-head { display:flex; align-items:flex-end; justify-content:space-between; gap:18px; margin-bottom:22px; }
.checkout-kicker { font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; color:#5B4FE8; margin-bottom:6px; }
.checkout-title { font-size:30px; line-height:1.2; font-weight:900; color:#1E1B4B; }
.checkout-sub { color:#64748B; margin-top:8px; max-width:650px; line-height:1.6; }
.checkout-back { color:#5B4FE8; font-size:14px; font-weight:700; white-space:nowrap; }
.checkout-grid { display:grid; grid-template-columns:minmax(0,1fr) 360px; gap:24px; align-items:start; }
.checkout-panel, .checkout-summary { background:#fff; border:1px solid #E2E8F0; border-radius:16px; box-shadow:0 12px 30px rgba(15,23,42,.04); }
.checkout-panel { padding:22px; }
.checkout-summary { padding:22px; position:sticky; top:82px; }
.section-title { display:flex; align-items:center; gap:10px; color:#1E1B4B; font-size:17px; font-weight:900; margin-bottom:16px; }
.section-title span { width:28px; height:28px; border-radius:9px; background:#EEF2FF; color:#5B4FE8; display:flex; align-items:center; justify-content:center; font-size:13px; }
.checkout-form { display:flex; flex-direction:column; gap:22px; }
.field-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
.field { display:flex; flex-direction:column; gap:7px; }
.field-full { grid-column:1 / -1; }
.field label { color:#334155; font-size:13px; font-weight:800; }
.field input, .field textarea { width:100%; border:1.5px solid #E2E8F0; border-radius:12px; padding:12px 13px; font-size:15px; color:#1E293B; background:#fff; outline:none; transition:border-color .16s, box-shadow .16s; }
.field textarea { min-height:96px; resize:vertical; line-height:1.5; }
.field input:focus, .field textarea:focus { border-color:#5B4FE8; box-shadow:0 0 0 3px rgba(91,79,232,.12); }
.choice-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }
.choice { border:1.5px solid #E2E8F0; border-radius:14px; padding:14px; background:#fff; text-align:left; transition:all .16s; min-height:94px; }
.choice:hover { border-color:#C7D2FE; }
.choice-active { border-color:#5B4FE8; background:#F8FAFF; box-shadow:0 0 0 3px rgba(91,79,232,.09); }
.choice-title { color:#1E1B4B; font-size:14px; font-weight:900; margin-bottom:6px; }
.choice-copy { color:#64748B; font-size:12px; line-height:1.45; }
.payment-methods { display:grid; gap:10px; margin-top:14px; }
.payment-method { width:100%; border:1.5px solid #E2E8F0; border-radius:14px; padding:12px 14px; background:#fff; display:grid; grid-template-columns:minmax(0,1fr) auto; gap:12px; align-items:center; text-align:left; transition:border-color .16s, box-shadow .16s, background .16s; }
.payment-method:hover { border-color:#C7D2FE; }
.payment-method-active { border-color:#5B4FE8; background:#F8FAFF; box-shadow:0 0 0 3px rgba(91,79,232,.09); }
.payment-method strong { display:block; color:#1E1B4B; font-size:14px; margin-bottom:3px; }
.payment-method span { display:block; color:#64748B; font-size:12px; line-height:1.45; }
.payment-chip { display:inline-flex; align-items:center; justify-content:center; min-height:28px; border-radius:999px; background:#EEF2FF; color:#4338CA; padding:4px 9px; font-size:11px; font-weight:900; white-space:nowrap; }
.plan-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin-top:16px; }
.plan { border:1.5px solid #E2E8F0; border-radius:14px; padding:12px 10px; background:#fff; text-align:center; transition:all .16s; }
.plan:hover { border-color:#C7D2FE; }
.plan-active { border-color:#5B4FE8; background:#F8FAFF; box-shadow:0 0 0 3px rgba(91,79,232,.09); }
.plan-months { color:#1E1B4B; font-size:14px; font-weight:900; }
.plan-monthly { color:#5B4FE8; font-size:13px; font-weight:800; margin-top:4px; }
.plan-tag { color:#94A3B8; font-size:11px; font-weight:700; margin-top:4px; }
.plan-summary { margin-top:12px; background:#F8FAFF; border:1px solid #E0E7FF; border-radius:12px; padding:12px 14px; font-size:13px; color:#334155; line-height:1.5; }
.checkout-note { border:1px solid #BFDBFE; background:#EFF6FF; color:#1D4ED8; border-radius:14px; padding:14px 16px; font-size:13px; line-height:1.55; }
.summary-title { color:#1E1B4B; font-size:17px; font-weight:900; margin-bottom:14px; }
.summary-items { display:flex; flex-direction:column; gap:12px; margin-bottom:16px; max-height:310px; overflow:auto; padding-right:4px; }
.summary-item { display:grid; grid-template-columns:52px minmax(0,1fr); gap:12px; align-items:center; }
.summary-img { width:52px; height:52px; border-radius:10px; background:#F1F5F9; overflow:hidden; display:flex; align-items:center; justify-content:center; color:#CBD5E1; }
.summary-img img { width:100%; height:100%; object-fit:cover; }
.summary-name { color:#1E1B4B; font-size:13px; font-weight:800; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.summary-meta { color:#94A3B8; font-size:12px; margin-top:3px; }
.summary-row { display:flex; justify-content:space-between; gap:12px; color:#475569; font-size:14px; margin:10px 0; }
.summary-total { display:flex; justify-content:space-between; gap:12px; color:#1E1B4B; font-size:20px; font-weight:900; padding-top:14px; border-top:2px solid #F1F5F9; margin-top:12px; }
.checkout-submit { width:100%; min-height:52px; border:0; border-radius:14px; margin-top:16px; color:#fff; background:var(--brand-grad); font-size:15px; font-weight:900; display:flex; align-items:center; justify-content:center; gap:8px; }
.checkout-submit:disabled { opacity:.55; cursor:not-allowed; }
.checkout-empty, .checkout-loading, .checkout-success { background:#fff; border:1px solid #E2E8F0; border-radius:16px; padding:50px 22px; text-align:center; color:#64748B; }
.checkout-success h2, .checkout-empty h2 { color:#1E1B4B; font-size:22px; margin-bottom:8px; }
.checkout-created { max-width:620px; margin:18px auto 0; display:flex; flex-direction:column; gap:10px; text-align:left; }
.checkout-created-item { border:1px solid #E2E8F0; border-radius:12px; padding:12px 14px; background:#F8FAFC; color:#334155; font-size:13px; line-height:1.45; }
.checkout-created-item strong { color:#1E1B4B; display:block; margin-bottom:4px; }
.checkout-payment-state { margin-top:8px; display:flex; flex-direction:column; gap:6px; }
.checkout-status-pill { width:max-content; max-width:100%; border-radius:999px; padding:5px 10px; font-size:11px; font-weight:900; background:#EEF2FF; color:#4338CA; }
.checkout-status-pill.ok { background:#DCFCE7; color:#166534; }
.checkout-status-pill.warn { background:#FEF3C7; color:#92400E; }
.checkout-status-pill.bad { background:#FEE2E2; color:#991B1B; }
.checkout-status-copy { color:#64748B; font-size:12px; line-height:1.45; }
.checkout-actions { display:flex; justify-content:center; gap:12px; flex-wrap:wrap; margin-top:22px; }
.checkout-primary, .checkout-secondary { min-height:44px; border-radius:12px; padding:0 18px; display:inline-flex; align-items:center; justify-content:center; font-size:14px; font-weight:800; }
.checkout-primary { background:var(--brand-grad); color:#fff; }
.checkout-secondary { background:#EEF2FF; color:#5B4FE8; }
.checkout-error { color:#DC2626; background:#FEF2F2; border:1px solid #FECACA; border-radius:12px; padding:12px 14px; font-size:13px; line-height:1.45; }
@media(max-width:860px) {
  .checkout-head { align-items:flex-start; flex-direction:column; }
  .checkout-grid { grid-template-columns:1fr; }
  .checkout-summary { position:static; }
}
@media(max-width:620px) {
  .checkout-wrap { padding:22px 14px 54px; }
  .checkout-title { font-size:24px; }
  .checkout-panel, .checkout-summary { padding:18px; border-radius:14px; }
  .field-grid, .choice-grid, .plan-grid { grid-template-columns:1fr; }
}
`

const deliveryOptions = [
  { id: 'courier', title: 'Доставка по Казахстану', copy: 'Продавец подтвердит срок и способ доставки в заказе.' },
  { id: 'pickup', title: 'Самовывоз / склад', copy: 'Подходит для B2B-заказов и локальной передачи товара.' },
]

const paymentOptions = [
  { id: 'saved_card', title: 'Сохраненный способ', copy: 'Создадим платежную заявку по токенизированному способу. Если провайдер вернет ссылку, покажем подтверждение.' },
  { id: 'installment', title: 'Рассрочка 3-12 мес', copy: 'Зафиксируем выбранный срок рассрочки в заказе и платежной заявке.' },
  { id: 'invoice', title: 'Счет / ручное подтверждение', copy: 'Заказ сохранится в системе, оплату подтвердит продавец или менеджер.' },
]

type CreatedCheckout = {
  order: MarketplaceOrderDetail
  payment?: MarketplacePayment
  paymentError?: string
}

type PaymentState = {
  label: string
  copy: string
  tone: 'ok' | 'warn' | 'bad' | 'info'
  action?: string
}

function isManualPayment(payment: MarketplacePayment | undefined) {
  return !payment || ['manual', 'manual_invoice', 'invoice'].includes(payment.provider)
}

function describePayment(payment: MarketplacePayment | undefined, fallbackStatus?: string | null, paymentError?: string): PaymentState {
  if (paymentError) {
    return {
      label: 'Платеж не создан',
      copy: `${paymentError}. Откройте заказ и повторите оплату другим способом.`,
      tone: 'bad',
    }
  }
  if (!payment) {
    return {
      label: fallbackStatus === 'paid' ? 'Оплата подтверждена' : 'Платеж ожидает создания',
      copy: fallbackStatus === 'paid'
        ? 'Заказ уже отмечен как оплаченный.'
        : 'Откройте заказ, чтобы создать или повторить платежную попытку.',
      tone: fallbackStatus === 'paid' ? 'ok' : 'warn',
    }
  }
  if (payment.status === 'pending' && !payment.payment_url && isManualPayment(payment)) {
    return {
      label: 'Счет ожидает подтверждения',
      copy: 'Заказ создан. Продавец или менеджер подтвердит оплату вручную и обновит статус заказа.',
      tone: 'warn',
    }
  }
  if (payment.status === 'pending' && !payment.payment_url) {
    return {
      label: 'Платежная заявка создана',
      copy: payment.provider === 'installment'
        ? 'Рассрочка зафиксирована в заказе. Провайдер или менеджер должен подтвердить платежный сценарий.'
        : 'Провайдер пока не вернул ссылку на подтверждение. Откройте заказ позже или выберите счет для ручного подтверждения.',
      tone: 'warn',
    }
  }
  switch (payment.status) {
    case 'requires_action':
      return {
        label: 'Нужно подтверждение в банке',
        copy: payment.payment_url
          ? 'Перейдите к оплате и завершите 3DS или подтверждение в приложении банка.'
          : 'Платеж ожидает действия у провайдера. Если ссылка не появилась, откройте заказ и проверьте доступные варианты оплаты.',
        tone: 'warn',
        action: payment.payment_url ? 'Подтвердить оплату' : undefined,
      }
    case 'authorized':
      return {
        label: 'Платеж авторизован',
        copy: 'Провайдер подтвердил авторизацию. Финальный статус обновится после подтверждения оплаты.',
        tone: 'ok',
      }
    case 'paid':
      return {
        label: 'Оплата подтверждена',
        copy: 'Платеж прошел, заказ передан продавцу в работу.',
        tone: 'ok',
      }
    case 'failed':
      return {
        label: 'Оплата не прошла',
        copy: 'Откройте заказ и попробуйте другой способ оплаты или создайте счет.',
        tone: 'bad',
      }
    case 'cancelled':
      return {
        label: 'Платеж отменен',
        copy: 'Можно открыть заказ и создать новую платежную попытку.',
        tone: 'bad',
      }
    case 'refunded':
      return {
        label: 'Возврат оформлен',
        copy: 'Платеж возвращен покупателю через провайдера.',
        tone: 'ok',
      }
    default:
      return {
        label: 'Платеж создан',
        copy: payment.payment_url
          ? 'Перейдите по ссылке провайдера для завершения оплаты.'
          : 'Ожидаем подтверждение от платежного провайдера.',
        tone: 'info',
        action: payment.payment_url ? 'Перейти к оплате' : undefined,
      }
  }
}

export default function CheckoutPage() {
  const { user, openAuth } = useStore()
  const { show } = useToast()
  const [cart, setCart] = useState<Cart | null>(null)
  const [loading, setLoading] = useState(true)
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([])
  const [methodsLoading, setMethodsLoading] = useState(false)
  const [plans, setPlans] = useState<InstallmentPlan[]>([])
  const [plansLoading, setPlansLoading] = useState(false)
  const [months, setMonths] = useState(3)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [createdCheckout, setCreatedCheckout] = useState<CreatedCheckout[]>([])
  const [form, setForm] = useState({
    name: user?.name ?? '',
    phone: user?.phone ?? '',
    city: '',
    address: '',
    comment: '',
    delivery: 'courier',
    payment: 'invoice',
    payment_method_id: '',
  })

  useEffect(() => {
    if (!user) { openAuth('login'); return }
    setLoading(true)
    setMethodsLoading(true)
    Promise.allSettled([apiGetCart(), apiGetPaymentMethods()])
      .then(([cartResult, methodsResult]) => {
        if (cartResult.status === 'fulfilled') {
          setCart(cartResult.value)
        } else {
          setError(cartResult.reason?.message || 'Не удалось загрузить корзину')
        }
        if (methodsResult.status === 'fulfilled') {
          const active = methodsResult.value.items.filter(method => method.status === 'active')
          setPaymentMethods(active)
          const primary = active.find(method => method.is_default) ?? active[0]
          if (primary) {
            setForm(prev => ({
              ...prev,
              payment: 'saved_card',
              payment_method_id: String(primary.id),
            }))
          }
        }
      })
      .finally(() => {
        setLoading(false)
        setMethodsLoading(false)
      })
  }, [user])

  const totalKnown = useMemo(() => cart?.items.every(item => item.unit_price != null) ?? false, [cart])
  const totalAmount = cart?.total_amount ?? 0
  const fmt = (n: number | null | undefined) => n != null ? n.toLocaleString('ru-KZ') + ' ₸' : 'Цена по запросу'

  useEffect(() => {
    if (!totalKnown || totalAmount <= 0) {
      setPlans([])
      return
    }
    setPlansLoading(true)
    apiInstallmentOptions(totalAmount)
      .then(result => {
        setPlans(result.plans)
        const first = result.plans[0]
        if (first) setMonths(first.months)
      })
      .catch(() => setPlans([]))
      .finally(() => setPlansLoading(false))
  }, [totalKnown, totalAmount])

  const selectedPlan = plans.find(plan => plan.months === months) ?? null

  function setField(name: string, value: string) {
    setForm(prev => ({ ...prev, [name]: value }))
  }

  function selectPayment(payment: string) {
    setForm(prev => ({
      ...prev,
      payment,
      payment_method_id: payment === 'saved_card' ? (prev.payment_method_id || String(paymentMethods[0]?.id || '')) : '',
    }))
  }

  async function submit(e: FormEvent) {
    e.preventDefault()
    if (!cart?.items.length) return
    if (!form.name.trim() || !form.phone.trim() || !form.city.trim()) {
      setError('Заполните имя, телефон и город, чтобы продавец мог подтвердить заказ.')
      return
    }
    if (form.payment === 'saved_card' && !form.payment_method_id) {
      setError('Выберите сохраненный способ оплаты или переключитесь на счет.')
      return
    }
    if (form.payment === 'installment' && !selectedPlan) {
      setError('Рассрочка недоступна для текущей суммы. Выберите сохраненный способ оплаты или счет.')
      return
    }
    setSubmitting(true)
    setError(null)
    const deliveryAddress = [form.city.trim(), form.address.trim()].filter(Boolean).join(', ')
    const notes = [
      `Доставка: ${deliveryOptions.find(x => x.id === form.delivery)?.title}`,
      `Оплата: ${paymentOptions.find(x => x.id === form.payment)?.title}`,
      selectedPlan ? `Рассрочка: ${selectedPlan.months} мес, ${selectedPlan.monthly.toLocaleString('ru-KZ')} ₸/мес, всего ${selectedPlan.total.toLocaleString('ru-KZ')} ₸` : null,
      form.comment.trim() ? `Комментарий: ${form.comment.trim()}` : null,
    ].filter(Boolean).join('\n')

    try {
      const created = await apiCheckoutMarketplaceOrders({
        source: 'marqet',
        buyer_name: form.name.trim(),
        buyer_phone: form.phone.trim(),
        delivery_address: deliveryAddress,
        notes,
      })
      const payments = await Promise.allSettled(
        created.items.map(order => apiCreateMarketplacePayment(order.id, {
          provider: form.payment === 'saved_card'
            ? paymentMethods.find(method => String(method.id) === form.payment_method_id)?.provider ?? 'saved_card'
            : form.payment === 'installment'
              ? 'installment'
              : 'manual_invoice',
          payment_method_id: form.payment === 'saved_card' ? Number(form.payment_method_id) : null,
        })),
      )
      setCreatedCheckout(created.items.map((order, index) => {
        const payment = payments[index]
        return {
          order,
          payment: payment.status === 'fulfilled' ? payment.value : undefined,
          paymentError: payment.status === 'rejected'
            ? payment.reason?.message || 'Не удалось создать платеж'
            : undefined,
        }
      }))
      setCart({ items: [], total_items: 0, total_amount: 0 })
      window.dispatchEvent(new CustomEvent('marqet:cart-updated'))
      show(form.payment === 'invoice'
        ? 'Заказы созданы и ожидают ручного подтверждения оплаты'
        : 'Заказы созданы, статус оплаты появится после подтверждения провайдера')
    } catch (err: any) {
      setError(err.message || 'Не удалось оформить заказ')
    } finally {
      setSubmitting(false)
    }
  }

  if (!user) return null

  return (
    <>
      <style>{css}</style>
      <main className="checkout-wrap">
        <div className="checkout-head">
          <div>
            <div className="checkout-kicker">Оформление заказа</div>
            <h1 className="checkout-title">Подтвердите заказ</h1>
            <p className="checkout-sub">
              marqet.kz создаст заказы по продавцам, закрепит товары за покупателем и подготовит платежную заявку или счет. Продавцы увидят заказ в qpartner/складе.
            </p>
          </div>
          <Link className="checkout-back" to="/cart">Вернуться в корзину</Link>
        </div>

        {loading ? (
          <div className="checkout-loading">Загрузка корзины...</div>
        ) : createdCheckout.length > 0 ? (
          <div className="checkout-success">
            <h2>Заказы созданы</h2>
            <p>Создано заказов: {createdCheckout.length}. Статус оплаты будет обновлен после подтверждения провайдером, продавцом или менеджером.</p>
            <div className="checkout-created">
              {createdCheckout.map(({ order, payment, paymentError }) => {
                const state = describePayment(payment, order.payment_status, paymentError)
                return (
                  <div className="checkout-created-item" key={order.id}>
                    <strong>{order.number} · {order.supplier_name || 'Продавец'}</strong>
                    Сумма: {fmt(order.total_amount)}
                    <div className="checkout-payment-state">
                      <span className={`checkout-status-pill ${state.tone === 'info' ? '' : state.tone}`}>{state.label}</span>
                      <span className="checkout-status-copy">{state.copy}</span>
                      {payment?.payment_url && state.action && (
                        <div>
                          <a className="checkout-secondary" href={payment.payment_url}>{state.action}</a>
                        </div>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
            <div className="checkout-actions">
              <Link className="checkout-primary" to="/account/orders">Открыть мои заказы</Link>
              <Link className="checkout-secondary" to="/">Продолжить покупки</Link>
            </div>
          </div>
        ) : !cart || cart.items.length === 0 ? (
          <div className="checkout-empty">
            <h2>Корзина пуста</h2>
            <p>Добавьте товары из каталога, чтобы оформить заказ продавцу.</p>
            <div className="checkout-actions">
              <Link className="checkout-primary" to="/">Перейти в каталог</Link>
            </div>
          </div>
        ) : (
          <form className="checkout-grid" onSubmit={submit}>
            <div className="checkout-form">
              <section className="checkout-panel">
                <h2 className="section-title"><span>1</span> Контакты покупателя</h2>
                <div className="field-grid">
                  <div className="field">
                    <label htmlFor="buyer-name">Имя</label>
                    <input id="buyer-name" value={form.name} onChange={e => setField('name', e.target.value)} autoComplete="name" />
                  </div>
                  <div className="field">
                    <label htmlFor="buyer-phone">Телефон</label>
                    <input id="buyer-phone" value={form.phone} onChange={e => setField('phone', e.target.value)} autoComplete="tel" />
                  </div>
                  <div className="field">
                    <label htmlFor="buyer-city">Город</label>
                    <input id="buyer-city" value={form.city} onChange={e => setField('city', e.target.value)} autoComplete="address-level2" />
                  </div>
                  <div className="field">
                    <label htmlFor="buyer-address">Адрес или ориентир</label>
                    <input id="buyer-address" value={form.address} onChange={e => setField('address', e.target.value)} autoComplete="street-address" />
                  </div>
                </div>
              </section>

              <section className="checkout-panel">
                <h2 className="section-title"><span>2</span> Доставка</h2>
                <div className="choice-grid">
                  {deliveryOptions.map(option => (
                    <button key={option.id} type="button" className={`choice ${form.delivery === option.id ? 'choice-active' : ''}`} onClick={() => setField('delivery', option.id)}>
                      <div className="choice-title">{option.title}</div>
                      <div className="choice-copy">{option.copy}</div>
                    </button>
                  ))}
                </div>
              </section>

              <section className="checkout-panel">
                <h2 className="section-title"><span>3</span> Оплата и комментарий</h2>
                <div className="choice-grid">
                  {paymentOptions.map(option => (
                    <button
                      key={option.id}
                      type="button"
                      className={`choice ${form.payment === option.id ? 'choice-active' : ''}`}
                      onClick={() => selectPayment(option.id)}
                      disabled={option.id === 'saved_card' && !methodsLoading && paymentMethods.length === 0}
                    >
                      <div className="choice-title">{option.title}</div>
                      <div className="choice-copy">{option.copy}</div>
                    </button>
                  ))}
                </div>
                {form.payment === 'saved_card' && (
                  <div className="payment-methods">
                    {methodsLoading ? (
                      <div className="checkout-note">Загружаем сохраненные способы оплаты...</div>
                    ) : paymentMethods.length > 0 ? (
                      paymentMethods.map(method => (
                        <button
                          key={method.id}
                          type="button"
                          className={`payment-method ${form.payment_method_id === String(method.id) ? 'payment-method-active' : ''}`}
                          onClick={() => setField('payment_method_id', String(method.id))}
                        >
                          <span>
                            <strong>{method.brand.toUpperCase()} · {method.last4}</strong>
                            {method.expiry_month && method.expiry_year
                              ? `Действует до ${String(method.expiry_month).padStart(2, '0')}/${method.expiry_year}`
                              : 'Токенизированный способ оплаты'}
                          </span>
                          {method.is_default && <span className="payment-chip">Основной</span>}
                        </button>
                      ))
                    ) : (
                      <div className="checkout-note">
                        Сохраненных способов оплаты пока нет. Добавьте токенизированный способ в личном кабинете или выберите счет.
                      </div>
                    )}
                  </div>
                )}
                {form.payment === 'installment' && (
                  plansLoading ? (
                    <div className="checkout-note" style={{ marginTop: 14 }}>Загружаем варианты рассрочки...</div>
                  ) : plans.length > 0 ? (
                    <>
                      <div className="plan-grid">
                        {plans.map(plan => (
                          <button key={plan.months} type="button" className={`plan ${months === plan.months ? 'plan-active' : ''}`} onClick={() => setMonths(plan.months)}>
                            <div className="plan-months">{plan.months} мес</div>
                            <div className="plan-monthly">{plan.monthly.toLocaleString('ru-KZ')} ₸/мес</div>
                            <div className="plan-tag">{plan.interest_free ? 'без переплаты' : `+${plan.markup_percent}%`}</div>
                          </button>
                        ))}
                      </div>
                      {selectedPlan && (
                        <div className="plan-summary">
                          {selectedPlan.months} платежей по <b>{selectedPlan.monthly.toLocaleString('ru-KZ')} ₸</b>
                          {' · итого '}<b>{selectedPlan.total.toLocaleString('ru-KZ')} ₸</b>
                          {selectedPlan.interest_free ? ' · без переплаты' : ` · переплата ${selectedPlan.markup_percent}%`}
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="checkout-note" style={{ marginTop: 14 }}>
                      Рассрочка доступна для заказов с известной суммой от 6 000 ₸. Для этого заказа используйте сохраненный способ оплаты или счет.
                    </div>
                  )
                )}
                <div className="field" style={{ marginTop: 14 }}>
                  <label htmlFor="buyer-comment">Комментарий к заказу</label>
                  <textarea id="buyer-comment" value={form.comment} onChange={e => setField('comment', e.target.value)} placeholder="Например: нужна доставка до пятницы, отправьте документы для юрлица." />
                </div>
              </section>
            </div>

            <aside className="checkout-summary">
              <div className="summary-title">Ваш заказ</div>
              <div className="summary-items">
                {cart.items.map(item => (
                  <div className="summary-item" key={item.id}>
                    <div className="summary-img">
                      {item.image_url ? <img src={item.image_url} alt={item.product_name} /> : (
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
                      )}
                    </div>
                    <div>
                      <div className="summary-name">{item.product_name}</div>
                      <div className="summary-meta">{item.quantity} {item.unit || 'шт.'} · {item.supplier_name || 'Продавец'}</div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="summary-row"><span>Товаров</span><span>{cart.total_items} шт.</span></div>
              <div className="summary-row"><span>Доставка</span><span>После подтверждения</span></div>
              <div className="summary-total"><span>Итого</span><span>{totalKnown ? fmt(cart.total_amount) : 'По запросу'}</span></div>
              {error && <div className="checkout-error" style={{ marginTop: 14 }}>{error}</div>}
              <div className="checkout-note" style={{ marginTop: 14 }}>
                {form.payment === 'installment' && selectedPlan
                  ? `Рассрочка будет сохранена в заказе: ${selectedPlan.months} мес по ${selectedPlan.monthly.toLocaleString('ru-KZ')} ₸.`
                  : 'Мы не храним номер карты и CVV. Если провайдер вернет ссылку на подтверждение, она появится в заказе; счет подтверждается продавцом или менеджером.'}
              </div>
              <button className="checkout-submit" type="submit" disabled={submitting}>
                {submitting
                  ? 'Создаем заказ...'
                  : form.payment === 'invoice'
                    ? 'Создать заказ и счет'
                    : form.payment === 'installment'
                      ? (selectedPlan ? `Оформить рассрочку · ${selectedPlan.monthly.toLocaleString('ru-KZ')} ₸/мес` : 'Оформить рассрочку')
                      : `Создать заказ и платеж${totalKnown ? ' · ' + fmt(cart.total_amount) : ''}`}
              </button>
            </aside>
          </form>
        )}
      </main>
    </>
  )
}
