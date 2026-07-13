import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  apiGetSupplierMarketplaceLedger,
  apiGetSupplierMarketplaceWallet,
  type SupplierMarketplaceLedgerEntry,
  type SupplierMarketplaceWallet,
} from '../../api'
import './seller.css'

const fmtMoney = (value: number | null | undefined) => `${Number(value ?? 0).toLocaleString('ru-KZ')} ₸`
const fmtDate = (value: string) => new Intl.DateTimeFormat('ru-KZ', { day: '2-digit', month: 'long', hour: '2-digit', minute: '2-digit' }).format(new Date(value))

const entryLabels: Record<SupplierMarketplaceLedgerEntry['entry_type'], string> = {
  credit: 'Начисление',
  debit: 'Списание',
  hold: 'Холд',
  release: 'Выплата',
  refund: 'Возврат',
  adjust: 'Корректировка',
}

export default function SellerWalletPage() {
  const [wallet, setWallet] = useState<SupplierMarketplaceWallet | null>(null)
  const [ledger, setLedger] = useState<SupplierMarketplaceLedgerEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      apiGetSupplierMarketplaceWallet(),
      apiGetSupplierMarketplaceLedger({ limit: 80 }),
    ])
      .then(([walletData, ledgerData]) => {
        setWallet(walletData)
        setLedger(ledgerData.items)
      })
      .catch(e => setError(e instanceof Error ? e.message : 'Не удалось загрузить кошелек продавца'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <main className="seller-wrap">
      <section className="seller-head">
        <div>
          <div className="seller-eyebrow">Финансы продавца</div>
          <h1>Кошелек маркетплейса</h1>
          <p>Разделяйте деньги в ожидании завершения заказа и средства, доступные продавцу после выполнения.</p>
        </div>
        <div className="seller-head-actions">
          <Link className="seller-secondary" to="/seller/orders">Заказы</Link>
          <Link className="seller-primary" to="/account">Мои объявления</Link>
        </div>
      </section>

      {loading && <section className="seller-section"><p>Загрузка кошелька...</p></section>}
      {error && <section className="seller-alert">{error}</section>}

      {wallet && (
        <>
          <section className="seller-wallet-grid">
            <div className="seller-balance-card seller-balance-main">
              <span>Доступно к выплате</span>
              <strong>{fmtMoney(wallet.available_amount)}</strong>
              <small>Средства после завершенных заказов.</small>
            </div>
            <div className="seller-balance-card">
              <span>В холде</span>
              <strong>{fmtMoney(wallet.pending_amount)}</strong>
              <small>Оплаты, ожидающие выполнения заказа.</small>
            </div>
            <div className="seller-balance-card">
              <span>Операций</span>
              <strong>{wallet.ledger_entries.toLocaleString('ru-KZ')}</strong>
              <small>Всего записей в журнале.</small>
            </div>
          </section>

          <section className="seller-section">
            <div className="seller-section-head">
              <h2>Журнал операций</h2>
              <span>{ledger.length} из {wallet.ledger_entries}</span>
            </div>
            {ledger.length === 0 ? (
              <p>Операций пока нет. После оплаты заказа появится hold-запись.</p>
            ) : (
              <div className="seller-ledger">
                {ledger.map(entry => (
                  <article className="seller-ledger-row" key={entry.id}>
                    <div>
                      <strong>{entryLabels[entry.entry_type]}</strong>
                      <span>{entry.description ?? entry.order_number ?? 'Операция marketplace'}</span>
                      <small>{entry.order_number ? `Заказ ${entry.order_number} · ` : ''}{fmtDate(entry.created_at)}</small>
                    </div>
                    <span className={`seller-ledger-status seller-ledger-${entry.status}`}>{entry.status}</span>
                    <div className="seller-money">{fmtMoney(entry.amount)}</div>
                  </article>
                ))}
              </div>
            )}
          </section>
        </>
      )}
    </main>
  )
}
