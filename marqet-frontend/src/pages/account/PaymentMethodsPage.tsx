import { useEffect, useState, type FormEvent } from 'react'
import { apiBindPaymentMethod, apiDeletePaymentMethod, apiGetPaymentMethods, apiSetDefaultPaymentMethod, type PaymentMethod, type PaymentMethodsResponse } from '../../api'
import { AccountIcon, AccountShell, AccountStatCard, EmptyState, MockDataNotice, PaymentCard } from './accountUi'

const providerOptions = [
  { value: 'test_psp', label: 'Sandbox PSP', hint: 'Для тестовой интеграции и ручной проверки' },
  { value: 'kaspi_pay', label: 'Kaspi Pay', hint: 'Токен из платежного кабинета Kaspi' },
  { value: 'halyk_epay', label: 'Halyk ePay', hint: 'Токенизированная карта Halyk/ePay' },
  { value: 'manual', label: 'Ручной провайдер', hint: 'Для временной операционной обработки' },
] as const

const brandLabels: Record<PaymentMethod['brand'], string> = {
  visa: 'Visa',
  mastercard: 'Mastercard',
  kaspi: 'Kaspi',
  halyk: 'Halyk',
  unknown: 'Другое',
}

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

function normalizeProvider(value: string) {
  return value.trim().toLowerCase().replace(/\s+/g, '_').slice(0, 64)
}

function normalizeToken(value: string) {
  return value.trim().replace(/\s+/g, '').slice(0, 512)
}

function validateExpiry(month: string, year: string) {
  if (!month && !year) return ''
  const parsedMonth = Number(month)
  const parsedYear = Number(year)
  const currentYear = new Date().getFullYear()
  if (!Number.isInteger(parsedMonth) || parsedMonth < 1 || parsedMonth > 12) return 'Месяц должен быть от 01 до 12'
  if (!Number.isInteger(parsedYear) || parsedYear < currentYear || parsedYear > currentYear + 20) return `Год должен быть от ${currentYear} до ${currentYear + 20}`
  return ''
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
    const method = data?.items.find(item => item.id === id)
    if (method && !window.confirm(`Удалить способ оплаты ${brandLabels[method.brand]} •••• ${method.last4}?`)) return
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
    const provider = normalizeProvider(form.provider)
    const providerToken = normalizeToken(form.provider_token)
    const expiryError = validateExpiry(form.expiry_month, form.expiry_year)
    if (!provider) {
      setError('Выберите или укажите платежного провайдера')
      return
    }
    if (last4.length !== 4) {
      setError('Укажите последние 4 цифры карты или платежного метода')
      return
    }
    if (providerToken.length < 8) {
      setError('Укажите токен платежного провайдера. Номер карты, CVV и 3DS-коды сюда вводить нельзя.')
      return
    }
    if (expiryError) {
      setError(expiryError)
      return
    }
    setSaving(true)
    try {
      const created = await apiBindPaymentMethod({
        provider,
        provider_token: providerToken,
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

  const methods = data?.items ?? []
  const defaultMethod = methods.find(method => method.is_default)
  const activeCount = methods.filter(method => method.status === 'active').length
  const expiringCount = methods.filter(method => {
    if (!method.expiry_month || !method.expiry_year) return false
    const now = new Date()
    const expiry = new Date(method.expiry_year, method.expiry_month - 1, 1)
    const sixMonthsAhead = new Date(now.getFullYear(), now.getMonth() + 6, 1)
    return expiry <= sixMonthsAhead
  }).length

  return (
    <AccountShell
      title="Способы оплаты"
      subtitle="Сохраненные токенизированные карты и платежные методы для быстрого оформления заказа."
      actions={<button className="acct-primary" onClick={() => setFormOpen(open => !open)}>{formOpen ? 'Закрыть' : 'Добавить способ'}</button>}
    >
      {data?.is_mock && <MockDataNotice unavailable={data.unavailable} />}
      {error && <div className="acct-notice">{error}</div>}
      <div className="acct-grid">
        <AccountStatCard label="Активных способов" value={data ? activeCount : '-'} icon="card" />
        <AccountStatCard label="Основной способ" value={defaultMethod ? `•••• ${defaultMethod.last4}` : 'Не выбран'} icon="check" />
        <AccountStatCard label="Провайдеры" value={data ? new Set(methods.map(method => method.provider || 'manual')).size : '-'} icon="grid" />
        <AccountStatCard label="Скоро истекают" value={data ? expiringCount : '-'} icon="clock" />
      </div>
      <section className="acct-section acct-payment-security">
        <div>
          <span className="acct-security-icon"><AccountIcon name="check" /></span>
          <h2>Безопасная привязка</h2>
          <p>
            marqet.kz хранит только токен платежного провайдера, бренд, срок действия и последние 4 цифры. Полный номер карты,
            CVV и 3DS-коды должны оставаться на стороне банка или PSP.
          </p>
        </div>
        <div className="acct-payment-rail">
          <span>Tokenization</span>
          <span>3DS ready</span>
          <span>Escrow flow</span>
        </div>
      </section>
      {formOpen && (
        <form className="acct-section acct-payment-form" onSubmit={addPaymentMethod}>
          <div>
            <h2>Новый способ оплаты</h2>
            <p>Введите токен, полученный от платежного провайдера. Это не номер карты: он нужен только для повторной оплаты через защищенный PSP-flow.</p>
          </div>
          <div className="acct-form-grid">
            <label>
              Провайдер
              <select value={form.provider} onChange={e => {
                const provider = e.target.value
                setForm(prev => ({
                  ...prev,
                  provider,
                  brand: provider === 'kaspi_pay' ? 'kaspi' : provider === 'halyk_epay' ? 'halyk' : prev.brand,
                }))
              }}>
                {providerOptions.map(option => <option value={option.value} key={option.value}>{option.label}</option>)}
              </select>
              <span className="acct-field-hint">{providerOptions.find(option => option.value === form.provider)?.hint}</span>
            </label>
            <label>
              Токен провайдера
              <input value={form.provider_token} onChange={e => setForm(prev => ({ ...prev, provider_token: e.target.value.replace(/\s+/g, '') }))} required minLength={8} maxLength={512} placeholder="tok_live_..." autoComplete="off" />
              <span className="acct-field-hint">Не вводите PAN, CVV, SMS-коды или пароль банка.</span>
            </label>
            <label>
              Бренд
              <select value={form.brand} onChange={e => setForm(prev => ({ ...prev, brand: e.target.value as PaymentMethod['brand'] }))}>
                {Object.entries(brandLabels).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
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
      {data && data.items.length === 0 ? (
        <EmptyState
          title="Карт пока нет"
          text="Добавьте токенизированный способ оплаты, чтобы быстрее оплачивать заказы и использовать защищенный escrow-сценарий."
          action={<button className="acct-primary" onClick={() => setFormOpen(true)}>Добавить способ</button>}
        />
      ) : (
        <div className="acct-row-list">
          {data?.items.map(method => (
            <section className="acct-section" key={method.id}>
              <PaymentCard method={method} />
              <div className="acct-actions" style={{marginTop:14}}>
                <button className="acct-secondary" onClick={() => makeDefault(method.id)} disabled={method.is_default || busyId === method.id}>
                  {method.is_default ? 'Уже основной' : busyId === method.id ? 'Обновляем...' : 'Сделать основной'}
                </button>
                <button className="acct-secondary" onClick={() => remove(method.id)} disabled={busyId === method.id}>
                  {busyId === method.id ? 'Удаляем...' : 'Удалить'}
                </button>
              </div>
            </section>
          ))}
        </div>
      )}
    </AccountShell>
  )
}
