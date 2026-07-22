import { useEffect, useState } from 'react'
import { apiBindCard, apiBindPayoutAccount } from '../api'

const css = `
.cardm-back { position:fixed; inset:0; background:rgba(15,23,42,.55); backdrop-filter:blur(2px); z-index:1000; display:flex; align-items:center; justify-content:center; padding:20px; }
.cardm { background:#fff; border-radius:18px; width:100%; max-width:420px; max-height:92vh; overflow:auto; box-shadow:0 24px 60px rgba(15,23,42,.28); }
.cardm-head { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:20px 22px 6px; }
.cardm-title { font-size:18px; font-weight:900; color:#1E1B4B; }
.cardm-x { background:none; border:0; color:#94A3B8; font-size:20px; line-height:1; cursor:pointer; padding:4px 6px; }
.cardm-x:hover { color:#475569; }
.cardm-body { padding:8px 22px 22px; }
.cardm-frame { width:100%; border:0; display:block; }
.cardm-load, .cardm-err { padding:30px 6px; text-align:center; color:#64748B; font-size:14px; }
.cardm-err { color:#DC2626; }
`

export default function AddCardModal({ kind, onClose, onBound }: {
  kind: 'method' | 'payout'
  onClose: () => void
  onBound: () => void
}) {
  const [url, setUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const bind = kind === 'method' ? apiBindCard : apiBindPayoutAccount
    bind(`${window.location.origin}/account`)
      .then(r => setUrl(r.redirect_url))
      .catch(e => setError(e.message || 'Не удалось открыть форму оплаты'))
  }, [kind])

  useEffect(() => {
    // The gateway page signals completion from inside its iframe.
    function onMessage(e: MessageEvent) {
      if (e.origin !== window.location.origin) return
      if (e.data?.type === 'marqet:card-bound' && e.data?.status === 'active') {
        onBound()
        onClose()
      }
    }
    window.addEventListener('message', onMessage)
    return () => window.removeEventListener('message', onMessage)
  }, [onBound, onClose])

  useEffect(() => {
    function onEsc(e: KeyboardEvent) { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', onEsc)
    return () => document.removeEventListener('keydown', onEsc)
  }, [onClose])

  return (
    <>
      <style>{css}</style>
      <div className="cardm-back" onClick={onClose}>
        <div className="cardm" onClick={e => e.stopPropagation()}>
          <div className="cardm-head">
            <div className="cardm-title">
              {kind === 'method' ? 'Добавить способ оплаты' : 'Карта для получения выплат'}
            </div>
            <button className="cardm-x" onClick={onClose} aria-label="Закрыть">✕</button>
          </div>
          <div className="cardm-body">
            {error ? (
              <div className="cardm-err">{error}</div>
            ) : !url ? (
              <div className="cardm-load">Открываем защищённую форму...</div>
            ) : (
              <iframe
                className="cardm-frame"
                src={url}
                height={430}
                title="Форма оплаты"
                // Card fields live inside the gateway document, not in the SPA.
                sandbox="allow-scripts allow-forms allow-same-origin"
              />
            )}
          </div>
        </div>
      </div>
    </>
  )
}
