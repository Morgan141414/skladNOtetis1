import { useEffect, useState, type FormEvent } from 'react'
import { apiBindPaymentMethod, apiDeletePaymentMethod, apiGetPaymentMethods, apiSetDefaultPaymentMethod, type PaymentMethod, type PaymentMethodsResponse } from '../../api'
import { AccountShell, EmptyState, MockDataNotice, PaymentCard } from './accountUi'

const emptyForm = {
  provider: 'test_psp',
  provider_token: '',
  brand: 'visa' as PaymentMethod['brand'],
  last4: '',
  expiry_month: '',
  expiry_year: '',
  holder_name: '',
  is_default: true,
}

export default function PaymentMethodsPage() {
  const [data, setData] = useState<PaymentMethodsResponse | null>(null)
  const [error, setError] = useState('')
  const [formOpen, setFormOpen] = useState(false)
  const [form, setForm] = useState(emptyForm)
  const [saving, setSaving] = useState(false)
  const [busyId, setBusyId] = useState<string | null>(null)

  useEffect(() => {
    apiGetPaymentMethods()
      .then(setData)
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить способы оплаты'))
  }, [])

  function updateLocal(updater: (items: PaymentMethod[]) => PaymentMethod[]) {
    setData(prev => prev ? { ...prev, items: updater(prev.items) } : prev)
  }

  async function makeDefault(id: string) {
    setBusyId(id)
    if (data?.is_mock) {
      updateLocal(items => items.map(item => ({ ...item, is_default: item.id === id })))
      setBusyId(null)
      return
    }
    try {
      const next = await apiSetDefaultPaymentMethod(id)
      updateLocal(items => items.map(item => ({ ...item, is_default: item.id === next.id })))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Не удалось сделать способ оплаты основным')
    } finally {
      setBusyId(null)
    }
  }

  async function remove(id: string) {
    setBusyId(id)
    if (data?.is_mock) {
      updateLocal(items => items.filter(item => item.id !== id))
      setBusyId(null)
      return
    }
    try {
      await apiDeletePaymentMethod(id)
      updateLocal(items => items.filter(item => item.id !== id))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Не удалось удалить способ оплаты')
    } finally {
      setBusyId(null)
    }
  }

  async function addPaymentMethod(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    const last4 = form.last4.replace(/\D/g, '').slice(-4)
    if (last4.length !== 4) {
      setError('Укажите последние 4 цифры карты или платежного метода')
      return
    }
    if (form.provider_token.trim().length < 8) {
      setError('Укажите токен платежного провайдера')
      return
    }
    setSaving(true)
    try {
      const created = await apiBindPaymentMethod({
        provider: form.provider.trim(),
        provider_token: form.provider_token.trim(),
        brand: form.brand,
        last4,
        expiry_month: form.expiry_month ? Number(form.expiry_month) : null,
        expiry_year: form.expiry_year ? Number(form.expiry_year) : null,
        holder_name: form.holder_name.trim() || null,
        is_default: form.is_default,
      })
      setData(prev => {
        const current = prev?.items ?? []
        const items = form.is_default
          ? current.map(item => ({ ...item, is_default: false }))
          : current
        return { items: [created, ...items] }
      })
      setForm(emptyForm)
      setFormOpen(false)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Не удалось добавить способ оплаты')
    } finally {
      setSaving(false)
    }
  }

  return (
    <AccountShell
      title="Способы оплаты"
      subtitle="Сохраненные токенизированные карты и платежные методы для быстрого оформления заказа."
      actions={<button className="acct-primary" onClick={() => setFormOpen(open => !open)}>{formOpen ? 'Закрыть' : 'Добавить способ'}</button>}
    >
      {data?.is_mock && <MockDataNotice unavailable={data.unavailable} />}
      {error && <div className="acct-notice">{error}</div>}
      {formOpen && (
        <form className="acct-section acct-payment-form" onSubmit={addPaymentMethod}>
          <div>
            <h2>Новый способ оплаты</h2>
            <p>Введите только токен провайдера и маску карты. Полный номер карты, CVV и 3DS-коды на marqet.kz не сохраняются.</p>
          </div>
          <div className="acct-form-grid">
            <label>
              Провайдер
              <input value={form.provider} onChange={e => setForm(prev => ({ ...prev, provider: e.target.value }))} required maxLength={64} />
            </label>
            <label>
              PSP token
              <input value={form.provider_token} onChange={e => setForm(prev => ({ ...prev, provider_token: e.target.value }))} required minLength={8} maxLength={512} placeholder="tok_live_..." />
            </label>
            <label>
              Бренд
              <select value={form.brand} onChange={e => setForm(prev => ({ ...prev, brand: e.target.value as PaymentMethod['brand'] }))}>
                <option value="visa">Visa</option>
                <option value="mastercard">Mastercard</option>
                <option value="kaspi">Kaspi</option>
                <option value="halyk">Halyk</option>
                <option value="unknown">Другое</option>
              </select>
            </label>
            <label>
              Последние 4 цифры
              <input value={form.last4} onChange={e => setForm(prev => ({ ...prev, last4: e.target.value.replace(/\D/g, '').slice(0, 4) }))} inputMode="numeric" maxLength={4} placeholder="4242" required />
            </label>
            <label>
              Месяц
              <input value={form.expiry_month} onChange={e => setForm(prev => ({ ...prev, expiry_month: e.target.value.replace(/\D/g, '').slice(0, 2) }))} inputMode="numeric" placeholder="12" />
            </label>
            <label>
              Год
              <input value={form.expiry_year} onChange={e => setForm(prev => ({ ...prev, expiry_year: e.target.value.replace(/\D/g, '').slice(0, 4) }))} inputMode="numeric" placeholder="2030" />
            </label>
            <label className="acct-form-wide">
              Имя держателя
              <input value={form.holder_name} onChange={e => setForm(prev => ({ ...prev, holder_name: e.target.value }))} maxLength={255} />
            </label>
          </div>
          <label className="acct-check">
            <input type="checkbox" checked={form.is_default} onChange={e => setForm(prev => ({ ...prev, is_default: e.target.checked }))} />
            Сделать основным способом оплаты
          </label>
          <div className="acct-actions">
            <button className="acct-primary" disabled={saving}>{saving ? 'Сохраняем...' : 'Сохранить способ'}</button>
            <button type="button" className="acct-secondary" onClick={() => setFormOpen(false)} disabled={saving}>Отмена</button>
          </div>
        </form>
      )}
      <section className="acct-section">
        <h2>Безопасность платежей</h2>
        <p>
          marqet.kz не хранит номер карты, CVV или 3DS-коды. Для повторной оплаты используется только токен платежного
          провайдера, а в интерфейсе отображаются бренд, срок действия и последние 4 цифры.
        </p>
      </section>
      {data && data.items.length === 0 ? (
        <EmptyState title="Карт пока нет" text="Добавьте токенизированный способ оплаты, полученный от платежного провайдера." />
      ) : (
        <div className="acct-row-list">
          {data?.items.map(method => (
            <section className="acct-section" key={method.id}>
              <PaymentCard method={method} />
              <div className="acct-actions" style={{marginTop:14}}>
                <button className="acct-secondary" onClick={() => makeDefault(method.id)} disabled={method.is_default || busyId === method.id}>Сделать основной</button>
                <button className="acct-secondary" onClick={() => remove(method.id)} disabled={busyId === method.id}>Удалить</button>
              </div>
            </section>
          ))}
        </div>
      )}
    </AccountShell>
  )
}
