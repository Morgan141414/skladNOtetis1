import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiGetLoyaltyAccount, type LoyaltyAccount } from '../../api'
import { AccountShell, AccountStatCard, MockDataNotice } from './accountUi'

const tierLabels: Record<LoyaltyAccount['tier'], string> = {
  bronze: 'Bronze',
  silver: 'Silver',
  gold: 'Gold',
  platinum: 'Platinum',
}

const tierSteps: Array<{ tier: LoyaltyAccount['tier']; label: string; points: number; benefit: string }> = [
  { tier: 'bronze', label: 'Bronze', points: 0, benefit: 'Стартовый уровень и базовые начисления' },
  { tier: 'silver', label: 'Silver', points: 5000, benefit: 'Приоритетная поддержка по заказам' },
  { tier: 'gold', label: 'Gold', points: 15000, benefit: 'Больше персональных предложений' },
  { tier: 'platinum', label: 'Platinum', points: 50000, benefit: 'Максимальный статус покупателя' },
]

const tierRank = new Map(tierSteps.map((step, index) => [step.tier, index]))
const fmtPoints = (value: number) => value.toLocaleString('ru-KZ')
const fmtMoney = (value: number) => `${value.toLocaleString('ru-KZ')} ₸`

export default function LoyaltyPage() {
  const [account, setAccount] = useState<LoyaltyAccount | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    apiGetLoyaltyAccount()
      .then(setAccount)
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить бонусы'))
  }, [])

  const currentRank = account ? tierRank.get(account.tier) ?? 0 : 0
  const pointTarget = account?.next_tier_points && account.next_tier_points > 0 ? account.next_tier_points : tierSteps[currentRank]?.points ?? 0
  const progress = account && pointTarget > 0
    ? Math.min(100, Math.round((account.points_balance / pointTarget) * 100))
    : account?.tier === 'platinum' ? 100 : 0
  const pointsToNext = account ? Math.max(0, pointTarget - account.points_balance) : 0
  const visibleHistory = account?.history ?? []

  return (
    <AccountShell
      title="Бонусы и лояльность"
      subtitle="Баланс, уровень и история начислений за оплаченные заказы."
      actions={<Link className="acct-primary" to="/">Перейти к покупкам</Link>}
    >
      {account?.is_mock && <MockDataNotice unavailable={account.unavailable} />}
      {error && <div className="acct-notice">{error}</div>}
      <section className="acct-section acct-loyalty-hero">
        <div>
          <div className="acct-tier-pill">{account ? tierLabels[account.tier] : 'Загрузка'}</div>
          <h2>{account ? `${fmtPoints(account.points_balance)} бонусов доступно` : 'Загружаем бонусный баланс'}</h2>
          <p>
            1 бонус начисляется за каждые 1 000 ₸ завершенных и оплаченных заказов. Баллы из заказов в пути
            сначала попадают в ожидание и становятся доступными после завершения сделки.
          </p>
          <div className="acct-actions">
            <Link className="acct-secondary" to="/account/orders">Мои заказы</Link>
            <Link className="acct-secondary" to="/account/payment-methods">Способы оплаты</Link>
          </div>
        </div>
        <div className="acct-loyalty-score">
          <span>Ожидают</span>
          <strong>{account ? fmtPoints(account.points_pending) : '-'}</strong>
          <small>начислятся после завершения заказов</small>
        </div>
      </section>
      <div className="acct-grid">
        <AccountStatCard label="Доступно баллов" value={account ? fmtPoints(account.points_balance) : '-'} icon="star" />
        <AccountStatCard label="Ожидают начисления" value={account ? fmtPoints(account.points_pending) : '-'} icon="clock" />
        <AccountStatCard label="Уровень" value={account ? tierLabels[account.tier] : '-'} icon="check" />
        <AccountStatCard label="Завершенные покупки" value={account ? fmtMoney(account.lifetime_spend) : '-'} icon="card" />
      </div>
      <section className="acct-section">
        <h2>Прогресс уровня</h2>
        <p>
          {account?.tier === 'platinum'
            ? 'Вы уже на максимальном уровне программы.'
            : `До следующего уровня: ${fmtPoints(pointsToNext)} баллов`}
        </p>
        <div className="acct-progress" aria-label="Прогресс уровня">
          <span style={{width:`${progress}%`}} />
        </div>
        <div className="acct-tier-ladder">
          {tierSteps.map((step, index) => (
            <div className={`acct-tier-step ${index <= currentRank ? 'active' : ''}`} key={step.tier}>
              <strong>{step.label}</strong>
              <span>{fmtPoints(step.points)}+ баллов</span>
              <small>{step.benefit}</small>
            </div>
          ))}
        </div>
      </section>
      <section className="acct-section acct-loyalty-rules">
        <div>
          <h2>Как начисляются бонусы</h2>
          <p>Баллы считаются только по заказам с подтвержденной оплатой. При отмене, возврате или споре начисление не попадает в доступный баланс.</p>
        </div>
        <div className="acct-rule-grid">
          <div><strong>1 000 ₸</strong><span>стоимости товара</span></div>
          <div><strong>1 балл</strong><span>после завершения</span></div>
          <div><strong>0 риска</strong><span>возвраты исключаются</span></div>
        </div>
      </section>
      <section className="acct-section">
        <h2>История баллов</h2>
        <div className="acct-ledger">
          {account && visibleHistory.length === 0 && <p>Операций пока нет. После первой завершенной покупки история появится здесь.</p>}
          {visibleHistory.map(event => (
            <div className="acct-ledger-row" key={event.id}>
              <div>
                <strong>{event.title}</strong>
                <span>
                  {new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', year: 'numeric' }).format(new Date(event.created_at))}
                  {event.order_number ? ` · ${event.order_number}` : ''}
                </span>
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
