import { useEffect, useState } from 'react'
import { apiGetLoyaltyAccount, type LoyaltyAccount } from '../../api'
import { AccountShell, AccountStatCard, MockDataNotice } from './accountUi'

const tierLabels: Record<LoyaltyAccount['tier'], string> = {
  bronze: 'Bronze',
  silver: 'Silver',
  gold: 'Gold',
  platinum: 'Platinum',
}

export default function LoyaltyPage() {
  const [account, setAccount] = useState<LoyaltyAccount | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    apiGetLoyaltyAccount()
      .then(setAccount)
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить бонусы'))
  }, [])

  const progress = account ? Math.min(100, Math.round((account.points_balance / account.next_tier_points) * 100)) : 0

  return (
    <AccountShell title="Бонусы и лояльность" subtitle="Баланс, уровень и история начислений.">
      {account?.is_mock && <MockDataNotice unavailable={account.unavailable} />}
      {error && <div className="acct-notice">{error}</div>}
      <div className="acct-grid">
        <AccountStatCard label="Доступно баллов" value={account?.points_balance ?? '-'} icon="star" />
        <AccountStatCard label="Ожидают начисления" value={account?.points_pending ?? '-'} icon="clock" />
        <AccountStatCard label="Уровень" value={account ? tierLabels[account.tier] : '-'} icon="check" />
        <AccountStatCard label="Покупки" value={account ? `${account.lifetime_spend.toLocaleString('ru-KZ')} ₸` : '-'} icon="card" />
      </div>
      <section className="acct-section">
        <h2>Прогресс уровня</h2>
        <p>До следующего уровня: {account ? `${Math.max(0, account.next_tier_points - account.points_balance).toLocaleString('ru-KZ')} баллов` : 'загрузка'}</p>
        <div className="acct-progress" aria-label="Прогресс уровня">
          <span style={{width:`${progress}%`}} />
        </div>
      </section>
      <section className="acct-section">
        <h2>История баллов</h2>
        <div className="acct-ledger">
          {account?.history.length === 0 && <p>Операций пока нет.</p>}
          {account?.history.map(event => (
            <div className="acct-ledger-row" key={event.id}>
              <div>
                <strong>{event.title}</strong>
                <span>{new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', year: 'numeric' }).format(new Date(event.created_at))}</span>
              </div>
              <div className={event.points_delta >= 0 ? 'acct-points-pos' : 'acct-points-neg'}>
                {event.points_delta > 0 ? '+' : ''}{event.points_delta}
              </div>
            </div>
          ))}
        </div>
      </section>
    </AccountShell>
  )
}
