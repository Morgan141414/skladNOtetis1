import { useState, useRef, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useStore } from '../store'
import { apiGetCart } from '../api'
import { useT, useLocale, LOCALES } from '../i18n'

const Logo = () => (
  <svg width="36" height="36" viewBox="0 0 120 120" fill="none">
    <defs>
      <linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#5B4FE8"/>
        <stop offset="100%" stopColor="#3B82F6"/>
      </linearGradient>
    </defs>
    <path d="M20 35 L30 35 L44 80 L96 80 L106 45 L34 45" stroke="#1E1B4B" strokeWidth="8" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
    <circle cx="50" cy="94" r="8" fill="#1E1B4B"/>
    <circle cx="88" cy="94" r="8" fill="#1E1B4B"/>
    <path d="M42 70 L42 45 L62 62 L82 45 L82 70" stroke="url(#lg)" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
  </svg>
)

const css = `
.hdr { background: #fff; border-bottom: 1px solid #E2E8F0; position: sticky; top:0; z-index:200; }
.hdr-inner { max-width:1280px; margin:0 auto; padding:0 20px; display:flex; align-items:center; gap:16px; height:64px; }
.hdr-logo { display:flex; align-items:center; gap:10px; text-decoration:none; white-space:nowrap; flex-shrink:0; }
.hdr-logo-name { font-size:20px; font-weight:800; letter-spacing:-0.5px; line-height:1; }
.hdr-logo-name .mn { background:linear-gradient(135deg,#5B4FE8,#3B82F6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hdr-logo-name .mt { color:#1E1B4B; font-style:normal; -webkit-text-fill-color:#1E1B4B; }
.search-wrap { flex:1; max-width:520px; position:relative; }
.search-inp { width:100%; height:42px; padding:0 16px 0 44px; border:1.5px solid #E2E8F0; border-radius:22px; font-size:14px; outline:none; background:#F5F5FA; transition:all .2s; }
.search-inp:focus { border-color:#5B4FE8; background:#fff; box-shadow:0 0 0 3px rgba(91,79,232,.1); }
.search-ico { position:absolute; left:14px; top:50%; transform:translateY(-50%); color:#94A3B8; pointer-events:none; }
.hdr-right { margin-left:auto; display:flex; align-items:center; gap:8px; }
.btn-post { display:flex; align-items:center; gap:6px; padding:9px 18px; border-radius:22px; background:var(--brand-grad); color:#fff; font-size:14px; font-weight:700; border:none; transition:opacity .2s; white-space:nowrap; }
.btn-post:hover { opacity:.9; }
.btn-icon { width:40px; height:40px; border-radius:22px; border:1.5px solid #E2E8F0; background:#fff; color:#475569; display:flex; align-items:center; justify-content:center; position:relative; transition:all .2s; text-decoration:none; flex-shrink:0; }
.btn-icon:hover { border-color:#5B4FE8; color:#5B4FE8; }
.btn-icon .badge { position:absolute; top:-4px; right:-4px; min-width:18px; height:18px; background:#EF4444; color:#fff; font-size:10px; font-weight:800; border-radius:9px; display:flex; align-items:center; justify-content:center; padding:0 4px; border:2px solid #fff; }
.btn-login { padding:8px 16px; border-radius:22px; border:1.5px solid #E2E8F0; background:#fff; color:#334155; font-size:14px; font-weight:600; transition:all .2s; }
.btn-login:hover { border-color:#5B4FE8; color:#5B4FE8; }
.btn-reg { padding:8px 16px; border-radius:22px; border:none; background:#EEF2FF; color:#5B4FE8; font-size:14px; font-weight:700; transition:all .2s; }
.btn-reg:hover { background:#E0E7FF; }
.user-wrap { position:relative; }
.user-trigger { display:flex; align-items:center; gap:8px; padding:6px 12px; border-radius:22px; border:1.5px solid #E2E8F0; background:#fff; cursor:pointer; transition:all .2s; }
.user-trigger:hover { border-color:#5B4FE8; }
.avatar { width:30px; height:30px; border-radius:50%; background:var(--brand-grad); color:#fff; font-weight:700; font-size:13px; display:flex; align-items:center; justify-content:center; }
.uname { font-size:14px; font-weight:600; color:#334155; max-width:110px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.dd { position:absolute; right:0; top:calc(100% + 6px); background:#fff; border:1px solid #E2E8F0; border-radius:14px; box-shadow:0 8px 32px rgba(0,0,0,.12); min-width:180px; overflow:hidden; z-index:300; }
.dd a, .dd button { display:block; width:100%; padding:11px 16px; font-size:14px; color:#334155; background:none; border:none; text-align:left; transition:background .15s; cursor:pointer; }
.dd a:hover, .dd button:hover { background:#F8FAFC; }
.dd .danger { color:#EF4444; }
@media(max-width:640px){
  .hdr-inner{padding:0 12px;gap:8px}
  .search-wrap{min-width:0}
  .uname,.btn-login,.btn-reg,.btn-post span{display:none}
  .btn-post,.btn-icon{width:40px;padding:0;justify-content:center}
}
.verified-badge { display:inline-flex;align-items:center;gap:3px;background:#D1FAE5;color:#065F46;padding:2px 6px;border-radius:8px;font-size:10px;font-weight:700;margin-left:4px; }
.lang { display:flex; align-items:center; gap:2px; border:1.5px solid #E2E8F0; border-radius:22px; padding:2px; flex-shrink:0; }
.lang button { padding:5px 9px; border-radius:20px; border:0; background:none; color:#64748B; font-size:12px; font-weight:800; font-family:inherit; letter-spacing:.02em; }
.lang button.on { background:#EEF2FF; color:#5B4FE8; }
@media(max-width:640px){ .lang button { padding:5px 6px; font-size:11px; } }
`

export default function Header({ onSearch }: { onSearch?: (q: string) => void }) {
  const { user, logout, openAuth, openNCA } = useStore()
  const t = useT()
  const [locale, setLocale] = useLocale()
  const [q, setQ] = useState('')
  const [dd, setDd] = useState(false)
  const [cartCount, setCartCount] = useState(0)
  const ref = useRef<HTMLDivElement>(null)
  const nav = useNavigate()

  useEffect(() => {
    // Keep <html lang> in sync for screen readers and Google.
    const current = LOCALES.find(l => l.id === locale)
    if (current) document.documentElement.lang = current.htmlLang
  }, [locale])

  useEffect(() => {
    const h = (e: MouseEvent) => { if (ref.current && !ref.current.contains(e.target as Node)) setDd(false) }
    document.addEventListener('mousedown', h)
    return () => document.removeEventListener('mousedown', h)
  }, [])

  useEffect(() => {
    if (!user) { setCartCount(0); return }
    const refreshCart = () => apiGetCart().then(c => setCartCount(c.total_items)).catch(() => {})
    refreshCart()
    window.addEventListener('marqet:cart-updated', refreshCart)
    return () => window.removeEventListener('marqet:cart-updated', refreshCart)
  }, [user])

  function search(e: React.FormEvent) {
    e.preventDefault()
    onSearch?.(q)
    nav(`/?search=${encodeURIComponent(q)}`)
  }

  return (
    <>
      <style>{css}</style>
      <header className="hdr">
        <div className="hdr-inner">
          <Link to="/" className="hdr-logo">
            <Logo />
            <div className="hdr-logo-name">
              <span className="mn">marqet</span><em className="mt">.kz</em>
            </div>
          </Link>

          <div className="search-wrap">
            <form onSubmit={search}>
              <svg className="search-ico" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
              <input className="search-inp" placeholder={t('header.search')} value={q} onChange={e => setQ(e.target.value)} />
            </form>
          </div>

          <div className="hdr-right">
            <div className="lang">
              {LOCALES.map(l => (
                <button key={l.id} className={locale === l.id ? 'on' : ''} onClick={() => setLocale(l.id)} lang={l.htmlLang}>
                  {l.label}
                </button>
              ))}
            </div>

            <button className="btn-post" onClick={() => user ? nav('/post') : openAuth('register')}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 5v14M5 12h14"/></svg>
              <span>{t('header.post')}</span>
            </button>

            {user && (
              <>
                <Link to="/favorites" className="btn-icon" title={t('header.favorites')}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                </Link>
                <Link to="/cart" className="btn-icon" title={t('header.cart')}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                  {cartCount > 0 && <span className="badge">{cartCount > 9 ? '9+' : cartCount}</span>}
                </Link>
              </>
            )}

            {user ? (
              <div className="user-wrap" ref={ref}>
                <button className="user-trigger" onClick={() => setDd(d => !d)}>
                  <div className="avatar">{user.name[0]?.toUpperCase()}</div>
                  <span className="uname">{user.name}</span>
                  {user.is_nca_verified && <span className="verified-badge">✓ {t('header.iin')}</span>}
                </button>
                {dd && (
                  <div className="dd">
                    <Link to="/account/hub" onClick={() => setDd(false)}>{t('header.account')}</Link>
                    <Link to="/account/orders" onClick={() => setDd(false)}>{t('header.orders')}</Link>
                    <Link to="/account/payment-methods" onClick={() => setDd(false)}>{t('header.paymentMethods')}</Link>
                    <Link to="/account/loyalty" onClick={() => setDd(false)}>{t('header.loyalty')}</Link>
                    <Link to="/seller/orders" onClick={() => setDd(false)}>{t('header.sellerOrders')}</Link>
                    <Link to="/seller/wallet" onClick={() => setDd(false)}>{t('header.sellerWallet')}</Link>
                    <Link to="/account/listings" onClick={() => setDd(false)}>{t('header.myListings')}</Link>
                    <Link to="/favorites" onClick={() => setDd(false)}>{t('header.favorites')}</Link>
                    <Link to="/cart" onClick={() => setDd(false)}>{t('header.cart')}{cartCount > 0 ? ` (${cartCount})` : ''}</Link>
                    <Link to="/messages" onClick={() => setDd(false)}>{t('header.messages')}</Link>
                    {!user.is_nca_verified && <button onClick={() => { openNCA(); setDd(false) }}>{t('header.verifyIin')}</button>}
                    <button className="danger" onClick={() => { logout(); setDd(false) }}>{t('header.logout')}</button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <button className="btn-login" onClick={() => openAuth('login')}>{t('header.login')}</button>
                <button className="btn-reg" onClick={() => openAuth('register')}>{t('header.register')}</button>
              </>
            )}
          </div>
        </div>
      </header>
    </>
  )
}
