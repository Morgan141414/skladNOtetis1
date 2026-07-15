import { FormEvent, useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiCheckoutCart, apiGetCart, apiCreatePayment, apiInstallmentOptions, apiGetCards, type Cart, type InstallmentPlan, type SavedCard } from '../api'
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
.checkout-note { border:1px solid #BFDBFE; background:#EFF6FF; color:#1D4ED8; border-radius:14px; padding:14px 16px; font-size:13px; line-height:1.55; }
.plan-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; }
.plan { border:1.5px solid #E2E8F0; border-radius:14px; padding:12px 10px; background:#fff; text-align:center; transition:all .16s; }
.plan:hover { border-color:#C7D2FE; }
.plan-active { border-color:#5B4FE8; background:#F8FAFF; box-shadow:0 0 0 3px rgba(91,79,232,.09); }
.plan-months { color:#1E1B4B; font-size:14px; font-weight:900; }
.plan-monthly { color:#5B4FE8; font-size:13px; font-weight:800; margin-top:4px; }
.plan-tag { color:#94A3B8; font-size:11px; font-weight:700; margin-top:4px; }
.plan-summary { margin-top:12px; background:#F8FAFF; border:1px solid #E0E7FF; border-radius:12px; padding:12px 14px; font-size:13px; color:#334155; line-height:1.5; }
.pay-with { font-size:13px; font-weight:800; color:#334155; margin-bottom:8px; }
.saved-card { display:flex; align-items:center; gap:10px; width:100%; text-align:left; border:1.5px solid #E2E8F0; border-radius:12px; padding:12px 14px; background:#fff; margin-bottom:8px; transition:all .16s; }
.saved-card:hover { border-color:#C7D2FE; }
.saved-card-active { border-color:#5B4FE8; background:#F8FAFF; box-shadow:0 0 0 3px rgba(91,79,232,.09); }
.saved-card-radio { color:#5B4FE8; font-size:13px; }
.saved-card-num { flex:1; font-size:14px; font-weight:700; color:#1E1B4B; }
.saved-card-badge { background:#D1FAE5; color:#065F46; font-size:10px; font-weight:800; padding:2px 8px; border-radius:20px; }
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
  .field-grid, .choice-grid { grid-template-columns:1fr; }
}
`

const deliveryOptions = [
  { id: 'courier', title: 'Доставка по Казахстану', copy: 'Продавец подтвердит срок и способ доставки в заявке.' },
  { id: 'pickup', title: 'Самовывоз / склад', copy: 'Подходит для B2B-заказов и локальной передачи товара.' },
]

const paymentOptions = [
  { id: 'card', title: 'Оплата картой онлайн', copy: 'Visa / Mastercard. Оплата на защищённой странице банка.' },
  { id: 'installment', title: 'Рассрочка 3–12 мес', copy: 'Разбейте платёж на равные части. 3 и 6 мес — без переплаты.' },
  { id: 'invoice', title: 'Счёт / оплата продавцу', copy: 'После подтверждения продавец отправит условия оплаты.' },
]

export default function CheckoutPage() {
  const { user, openAuth } = useStore()
  const { show } = useToast()
  const nav = useNavigate()
  const [cart, setCart] = useState<Cart | null>(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [createdCount, setCreatedCount] = useState(0)
  const [paidReturn, setPaidReturn] = useState<'ok' | 'fail' | null>(null)
  const [months, setMonths] = useState(3)
  const [plans, setPlans] = useState<InstallmentPlan[]>([])
  const [cards, setCards] = useState<SavedCard[]>([])
  const [cardId, setCardId] = useState<number | 'new'>('new')
  const [form, setForm] = useState({
    name: user?.name ?? '',
    phone: user?.phone ?? '',
    city: '',
    address: '',
    comment: '',
    delivery: 'courier',
    payment: 'card',
  })

  useEffect(() => {
    // Handle return from the payment gateway (?paid=1&payment_id=...)
    const q = new URLSearchParams(window.location.search)
    if (q.has('paid')) {
      setPaidReturn(q.get('paid') === '1' ? 'ok' : 'fail')
      if (q.get('paid') === '1') window.dispatchEvent(new CustomEvent('marqet:cart-updated'))
    }
  }, [])

  useEffect(() => {
    if (!user) { openAuth('login'); return }
    apiGetCart()
      .then(setCart)
      .catch((err) => setError(err.message || 'Не удалось загрузить корзину'))
      .finally(() => setLoading(false))
    apiGetCards()
      .then(r => {
        const active = r.items.filter(c => c.status === 'active')
        setCards(active)
        const def = active.find(c => c.is_default) ?? active[0]
        if (def) setCardId(def.id)
      })
      .catch(() => setCards([]))
  }, [user])

  const totalKnown = useMemo(() => cart?.items.every(item => item.unit_price != null) ?? false, [cart])
  const totalAmount = cart?.total_amount ?? 0
  const fmt = (n: number | null | undefined) => n != null ? n.toLocaleString('ru-KZ') + ' ₸' : 'Цена по запросу'

  useEffect(() => {
    if (totalKnown && totalAmount > 0) {
      apiInstallmentOptions(totalAmount).then(r => setPlans(r.plans)).catch(() => setPlans([]))
    } else {
      setPlans([])
    }
  }, [totalKnown, totalAmount])

  const selectedPlan = plans.find(p => p.months === months) ?? null

  function setField(name: string, value: string) {
    setForm(prev => ({ ...prev, [name]: value }))
  }

  async function submit(e: FormEvent) {
    e.preventDefault()
    if (!cart?.items.length) return
    if (!form.name.trim() || !form.phone.trim() || !form.city.trim()) {
      setError('Заполните имя, телефон и город, чтобы продавец мог подтвердить заказ.')
      return
    }
    setSubmitting(true)
    setError(null)
    const notes = [
      `Покупатель: ${form.name.trim()}`,
      `Телефон: ${form.phone.trim()}`,
      `Город: ${form.city.trim()}`,
      form.address.trim() ? `Адрес: ${form.address.trim()}` : null,
      `Доставка: ${deliveryOptions.find(x => x.id === form.delivery)?.title}`,
      `Оплата: ${paymentOptions.find(x => x.id === form.payment)?.title}`,
      form.comment.trim() ? `Комментарий: ${form.comment.trim()}` : null,
    ].filter(Boolean).join('\n')

    try {
      const created = await apiCheckoutCart({ notes, source: 'marqet' })
      const wantsOnlinePay = (form.payment === 'card' || form.payment === 'installment') && totalKnown && totalAmount > 0

      if (wantsOnlinePay) {
        const useSaved = form.payment === 'card' && cardId !== 'new'
        const payment = await apiCreatePayment({
          amount: totalAmount,
          method: form.payment as 'card' | 'installment',
          installment_months: form.payment === 'installment' ? months : 0,
          inquiry_ids: created.map(c => c.id),
          return_url: `${window.location.origin}/checkout`,
          description: `Оплата заказа marqet.kz (${created.length} поз.)`,
          payment_method_id: useSaved ? (cardId as number) : undefined,
        })
        if (useSaved) {
          // One-click charge — settled server-side, no gateway redirect.
          if (payment.status === 'paid') { setPaidReturn('ok'); return }
          setError(`Оплата не прошла: ${payment.failure_reason ?? 'банк отклонил операцию'}`)
          return
        }
        if (payment.redirect_url) {
          window.location.href = payment.redirect_url  // to gateway
          return
        }
      }

      setCreatedCount(created.length)
      setCart({ items: [], total_items: 0, total_amount: 0 })
      window.dispatchEvent(new CustomEvent('marqet:cart-updated'))
      show('Заявки отправлены продавцам')
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
            <h1 className="checkout-title">Подтвердите заявку продавцам</h1>
            <p className="checkout-sub">
              marqet.kz создаст заявки по товарам из корзины. Продавцы увидят заказ в qpartner/складе и смогут подтвердить наличие, доставку и условия оплаты.
            </p>
          </div>
          <Link className="checkout-back" to="/cart">Вернуться в корзину</Link>
        </div>

        {loading ? (
          <div className="checkout-loading">Загрузка корзины...</div>
        ) : paidReturn === 'ok' ? (
          <div className="checkout-success">
            <h2>Оплата прошла успешно ✓</h2>
            <p>Мы зафиксировали оплату и передали заявки продавцам. Статус заказа виден в сообщениях.</p>
            <div className="checkout-actions">
              <Link className="checkout-primary" to="/messages">Открыть сообщения</Link>
              <Link className="checkout-secondary" to="/">Продолжить покупки</Link>
            </div>
          </div>
        ) : paidReturn === 'fail' ? (
          <div className="checkout-success">
            <h2>Оплата не завершена</h2>
            <p>Платёж отменён или не прошёл. Заявки продавцам уже созданы — можно повторить оплату из раздела сообщений или оформить заказ заново.</p>
            <div className="checkout-actions">
              <Link className="checkout-primary" to="/cart">Вернуться в корзину</Link>
              <Link className="checkout-secondary" to="/">В каталог</Link>
            </div>
          </div>
        ) : createdCount > 0 ? (
          <div className="checkout-success">
            <h2>Заявки отправлены</h2>
            <p>Создано заявок: {createdCount}. Дальше продавцы подтвердят условия и ответят в сообщениях.</p>
            <div className="checkout-actions">
              <Link className="checkout-primary" to="/messages">Открыть сообщения</Link>
              <Link className="checkout-secondary" to="/">Продолжить покупки</Link>
            </div>
          </div>
        ) : !cart || cart.items.length === 0 ? (
          <div className="checkout-empty">
            <h2>Корзина пуста</h2>
            <p>Добавьте товары из каталога, чтобы оформить заявку продавцу.</p>
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
                    <button key={option.id} type="button" className={`choice ${form.payment === option.id ? 'choice-active' : ''}`} onClick={() => setField('payment', option.id)}>
                      <div className="choice-title">{option.title}</div>
                      <div className="choice-copy">{option.copy}</div>
                    </button>
                  ))}
                </div>

                {form.payment === 'card' && cards.length > 0 && (
                  <div style={{ marginTop: 16 }}>
                    <div className="pay-with">Оплатить картой</div>
                    {cards.map(c => (
                      <button key={c.id} type="button" className={`saved-card ${cardId === c.id ? 'saved-card-active' : ''}`} onClick={() => setCardId(c.id)}>
                        <span className="saved-card-radio">{cardId === c.id ? '●' : '○'}</span>
                        <span className="saved-card-num">{c.brand ?? 'Карта'} •••• {c.last4 ?? '····'}</span>
                        {c.is_default && <span className="saved-card-badge">основная</span>}
                      </button>
                    ))}
                    <button type="button" className={`saved-card ${cardId === 'new' ? 'saved-card-active' : ''}`} onClick={() => setCardId('new')}>
                      <span className="saved-card-radio">{cardId === 'new' ? '●' : '○'}</span>
                      <span className="saved-card-num">Новая карта — ввести на странице банка</span>
                    </button>
                  </div>
                )}

                {form.payment === 'installment' && (
                  plans.length > 0 ? (
                    <div style={{ marginTop: 16 }}>
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
                    </div>
                  ) : (
                    <div className="checkout-note" style={{ marginTop: 14 }}>
                      Рассрочка доступна для заказов с известной суммой от 6 000 ₸. Для этого заказа используйте оплату картой или счёт.
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
                {form.payment === 'card'
                  ? 'После оформления вы перейдёте на защищённую страницу оплаты картой.'
                  : form.payment === 'installment'
                  ? 'После оформления вы перейдёте к оплате в рассрочку. Первый платёж — на странице банка.'
                  : 'Оплата не списывается автоматически. Заказ создаёт заявки продавцам и фиксирует ваши условия.'}
              </div>
              <button className="checkout-submit" type="submit" disabled={submitting}>
                {submitting
                  ? 'Обрабатываем...'
                  : form.payment === 'card'
                  ? `Оплатить${totalKnown ? ' ' + fmt(cart.total_amount) : ''}`
                  : form.payment === 'installment'
                  ? (selectedPlan ? `Оформить рассрочку · ${selectedPlan.monthly.toLocaleString('ru-KZ')} ₸/мес` : 'Оформить рассрочку')
                  : 'Отправить заявки продавцам'}
              </button>
            </aside>
          </form>
        )}
      </main>
    </>
  )
}
