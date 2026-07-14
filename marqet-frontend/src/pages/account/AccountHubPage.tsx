import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiGetAccountSummary, type AccountSummary } from '../../api'
import { AccountShell, AccountStatCard, MockDataNotice } from './accountUi'

export default function AccountHubPage() {
  const [summary, setSummary] = useState<AccountSummary | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    apiGetAccountSummary()
      .then(setSummary)
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить личный кабинет'))
  }, [])

  return (
    <AccountShell
      title="Обзор покупателя"
      subtitle="Заказы, бонусы, оплата и продавческие инструменты в одном месте."
      actions={<Link className="acct-secondary" to="/account/listings">Мои объявления</Link>}
    >
      {summary?.is_mock && <MockDataNotice unavailable={summary.unavailable} />}
      {error && <div className="acct-notice">{error}</div>}
      <div className="acct-grid">
        <AccountStatCard label="Активные заказы" value={summary?.active_orders ?? '-'} icon="box" to="/account/orders" />
        <AccountStatCard label="Доставлено" value={summary?.delivered_orders ?? '-'} icon="check" hint="История покупок" to="/account/orders" />
        <AccountStatCard label="Бонусные баллы" value={summary?.bonus_points ?? '-'} icon="star" to="/account/loyalty" />
        <AccountStatCard label="Способы оплаты" value={summary?.saved_payment_methods ?? '-'} icon="card" to="/account/payment-methods" />
      </div>
      <section className="acct-section">
        <h2>Быстрые действия</h2>
        <div className="acct-actions">
          <Link className="acct-primary" to="/">Перейти в каталог</Link>
          <Link className="acct-secondary" to="/cart">Открыть корзину</Link>
          <Link className="acct-secondary" to="/messages">Сообщения</Link>
          <Link className="acct-secondary" to="/post">Подать объявление</Link>
        </div>
      </section>
      <section className="acct-section">
        <h2>Что будет дальше</h2>
        <p>
          Этот раздел уже готов как пользовательская оболочка. Реальные заказы, безопасная токенизация карт
          и бонусный ledger будут подключаться через отдельный backend-слой без изменения текущего каталога и корзины.
        </p>
      </section>
    </AccountShell>
  )
}
