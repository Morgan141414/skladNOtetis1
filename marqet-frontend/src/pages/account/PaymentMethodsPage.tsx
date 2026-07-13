import { useEffect, useState } from 'react'
import { apiDeletePaymentMethod, apiGetPaymentMethods, apiSetDefaultPaymentMethod, type PaymentMethod, type PaymentMethodsResponse } from '../../api'
import { AccountShell, EmptyState, MockDataNotice, PaymentCard } from './accountUi'

export default function PaymentMethodsPage() {
  const [data, setData] = useState<PaymentMethodsResponse | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    apiGetPaymentMethods()
      .then(setData)
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить способы оплаты'))
  }, [])

  function updateLocal(updater: (items: PaymentMethod[]) => PaymentMethod[]) {
    setData(prev => prev ? { ...prev, items: updater(prev.items) } : prev)
  }

  async function makeDefault(id: string) {
    if (data?.is_mock) {
      updateLocal(items => items.map(item => ({ ...item, is_default: item.id === id })))
      return
    }
    const next = await apiSetDefaultPaymentMethod(id)
    updateLocal(items => items.map(item => ({ ...item, is_default: item.id === next.id })))
  }

  async function remove(id: string) {
    if (data?.is_mock) {
      updateLocal(items => items.filter(item => item.id !== id))
      return
    }
    await apiDeletePaymentMethod(id)
    updateLocal(items => items.filter(item => item.id !== id))
  }

  return (
    <AccountShell
      title="Способы оплаты"
      subtitle="Здесь будут сохраненные токенизированные карты и платежные методы."
      actions={<button className="acct-primary" disabled>Добавить карту · Скоро</button>}
    >
      {data?.is_mock && <MockDataNotice unavailable={data.unavailable} />}
      {error && <div className="acct-notice">{error}</div>}
      <section className="acct-section">
        <h2>Безопасность платежей</h2>
        <p>
          marqet.kz не должен хранить номер карты, CVV или 3DS-коды. После подключения провайдера здесь будут
          отображаться только маска карты, бренд, срок действия и токен провайдера.
        </p>
      </section>
      {data && data.items.length === 0 ? (
        <EmptyState title="Карт пока нет" text="После подключения PSP здесь появится безопасная привязка карты через платежную страницу провайдера." />
      ) : (
        <div className="acct-row-list">
          {data?.items.map(method => (
            <section className="acct-section" key={method.id}>
              <PaymentCard method={method} />
              <div className="acct-actions" style={{marginTop:14}}>
                <button className="acct-secondary" onClick={() => makeDefault(method.id)} disabled={method.is_default}>Сделать основной</button>
                <button className="acct-secondary" onClick={() => remove(method.id)}>Удалить</button>
              </div>
            </section>
          ))}
        </div>
      )}
    </AccountShell>
  )
}
