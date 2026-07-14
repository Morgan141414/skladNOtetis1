import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useStore } from '../store'
import { apiAddToCart, apiCheckFavorite, apiToggleFavorite } from '../api'
import { useToast } from './Toast'

export interface Product {
  id: number
  supplier_id?: number | null
  name: string
  description: string | null
  price: number | null
  unit: string | null
  supplier_name: string | null
  supplier_phone: string | null
  image_url: string | null
  category: string | null
  view_count?: number
  avg_rating?: number | null
  review_count?: number | null
  likes_count?: number | null
  promoted_until?: string | null
  supplier_city?: string | null
}

const css = `
.pcard { background:#fff; border-radius:16px; border:1px solid #E2E8F0; overflow:hidden; transition:all .22s; display:flex; flex-direction:column; position:relative; }
.pcard:hover { border-color:#C7D2FE; box-shadow:0 8px 24px rgba(91,79,232,.1); transform:translateY(-2px); }
.pcard-img-wrap { position:relative; }
.pcard-img { width:100%; aspect-ratio:4/3; background:#F1F5F9; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.pcard-img img { width:100%; height:100%; object-fit:cover; transition:transform .3s; }
.pcard:hover .pcard-img img { transform:scale(1.04); }
.pcard-noimg { display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; color:#CBD5E1; height:100%; }
.pcard-badges { position:absolute; top:10px; left:10px; right:50px; display:flex; flex-wrap:wrap; gap:6px; z-index:4; pointer-events:none; }
.pcard-cat, .pcard-top { display:inline-flex; align-items:center; min-height:24px; background:rgba(91,79,232,.92); color:#fff; font-size:11px; font-weight:800; padding:3px 9px; border-radius:20px; letter-spacing:.2px; }
.pcard-top { background:linear-gradient(135deg,#F59E0B,#EF4444); }
.pcard-fav { position:absolute; top:10px; right:10px; width:32px; height:32px; border-radius:50%; background:#fff; border:none; box-shadow:0 2px 8px rgba(0,0,0,.12); display:flex; align-items:center; justify-content:center; cursor:pointer; z-index:2; transition:all .18s; }
.pcard-fav:hover { transform:scale(1.15); }
.pcard-fav.active { background:#FEF2F2; }
.pcard-fav:disabled { opacity:.65; cursor:wait; transform:none; }
.pcard-body { padding:14px 16px 16px; flex:1; display:flex; flex-direction:column; gap:5px; }
.pcard-name { font-size:15px; font-weight:700; color:#1E1B4B; line-height:1.3; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.pcard-name:hover { color:#5B4FE8; }
.pcard-desc { font-size:13px; color:#64748B; line-height:1.5; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.pcard-price { font-size:20px; font-weight:800; color:#5B4FE8; margin-top:4px; }
.pcard-unit { font-size:12px; color:#94A3B8; font-weight:500; }
.pcard-pay { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-top:2px; }
.pcard-monthly { white-space:nowrap; padding:4px 7px; border-radius:8px; background:#FFFBEB; color:#92400E; font-size:11px; font-weight:800; }
.pcard-rating { display:flex; align-items:center; gap:4px; margin-top:2px; }
.pcard-stars { color:#F59E0B; font-size:13px; letter-spacing:1px; }
.pcard-rating-val { font-size:12px; font-weight:700; color:#92400E; }
.pcard-rating-cnt { font-size:11px; color:#94A3B8; }
.pcard-likes { display:flex; align-items:center; gap:3px; font-size:11px; color:#94A3B8; margin-top:1px; }
.pcard-trust { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; margin-top:4px; }
.pcard-trust span { min-height:28px; display:flex; align-items:center; justify-content:center; padding:4px 6px; border-radius:8px; background:#F8FAFC; color:#64748B; font-size:11px; font-weight:700; text-align:center; }
.pcard-footer { margin-top:auto; padding-top:12px; border-top:1px solid #F1F5F9; display:flex; flex-direction:column; gap:8px; }
.pcard-seller { display:flex; align-items:center; gap:6px; min-width:0; }
.seller-avatar { width:24px; height:24px; border-radius:50%; background:var(--brand-grad); color:#fff; font-size:10px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.seller-name { font-size:12px; color:#475569; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.seller-city { margin-left:auto; font-size:11px; color:#94A3B8; white-space:nowrap; }
.pcard-actions { display:flex; gap:6px; }
.btn-cart { flex:1; height:38px; border-radius:10px; font-size:12px; font-weight:700; background:#EEF2FF; color:#5B4FE8; border:none; transition:all .18s; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:5px; }
.btn-cart:hover { background:#E0E7FF; }
.btn-cart.added { background:#D1FAE5; color:#059669; }
.btn-detail { flex:1; height:38px; border-radius:10px; font-size:12px; font-weight:700; background:var(--brand-grad); color:#fff; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:5px; transition:opacity .18s; text-decoration:none; }
.btn-detail:hover { opacity:.9; }
.btn-share-card { width:36px; height:38px; border-radius:10px; border:1.5px solid #E2E8F0; background:#fff; color:#64748B; display:flex; align-items:center; justify-content:center; transition:all .18s; flex-shrink:0; position:relative; cursor:pointer; }
.btn-share-card:hover { border-color:#5B4FE8; color:#5B4FE8; }
.share-tip { position:absolute; bottom:calc(100% + 6px); left:50%; transform:translateX(-50%); background:#1E1B4B; color:#fff; font-size:11px; font-weight:600; padding:3px 8px; border-radius:5px; white-space:nowrap; pointer-events:none; z-index:10; }
.share-tip::after { content:''; position:absolute; top:100%; left:50%; transform:translateX(-50%); border:4px solid transparent; border-top-color:#1E1B4B; }
`

function Stars({ rating }: { rating: number }) {
  const full = Math.round(rating)
  return <span className="pcard-stars">{'★'.repeat(full)}{'☆'.repeat(5 - full)}</span>
}

function fmt(n: number | null): string {
  if (n === null) return 'По запросу'
  return n.toLocaleString('ru-KZ') + ' ₸'
}

function monthly(n: number | null): string | null {
  if (n === null || n <= 0) return null
  return Math.ceil(n / 12).toLocaleString('ru-KZ') + ' ₸/мес'
}

export default function ProductCard({ p, onContact }: { p: Product; onContact?: (p: Product) => void }) {
  const { user, openAuth } = useStore()
  const { show } = useToast()
  const [favorited, setFavorited] = useState(false)
  const [likes, setLikes] = useState(p.likes_count ?? 0)
  const [favoriteBusy, setFavoriteBusy] = useState(false)
  const [cartAdded, setCartAdded] = useState(false)
  const [copied, setCopied] = useState(false)
  const promoted = Boolean(p.promoted_until && new Date(p.promoted_until) > new Date())
  const monthlyPrice = monthly(p.price)

  useEffect(() => {
    setLikes(p.likes_count ?? 0)
    if (!user) {
      setFavorited(false)
      return
    }
    let mounted = true
    apiCheckFavorite(p.id)
      .then(result => {
        if (!mounted) return
        setFavorited(result.favorited)
        setLikes(result.likes_count)
      })
      .catch(() => {})
    return () => { mounted = false }
  }, [p.id, p.likes_count, user])

  async function handleFav(e: React.MouseEvent) {
    e.preventDefault()
    e.stopPropagation()
    if (!user) { openAuth('login'); return }
    if (favoriteBusy) return
    setFavoriteBusy(true)
    try {
      const r = await apiToggleFavorite(p.id)
      setFavorited(r.favorited)
      setLikes(r.likes_count)
      show(r.favorited ? 'Добавлено в избранное' : 'Убрано из избранного')
    } catch {
      show('Не удалось обновить избранное')
    } finally {
      setFavoriteBusy(false)
    }
  }

  async function handleCart(e: React.MouseEvent) {
    e.preventDefault()
    e.stopPropagation()
    if (!user) { openAuth('login'); return }
    const cart = await apiAddToCart(p.id, 1).catch(() => null)
    if (!cart) {
      show('Не удалось добавить товар')
      return
    }
    window.dispatchEvent(new CustomEvent('marqet:cart-updated'))
    setCartAdded(true)
    show('Добавлено в корзину')
    setTimeout(() => setCartAdded(false), 3000)
  }

  async function handleShare(e: React.MouseEvent) {
    e.preventDefault()
    e.stopPropagation()
    const url = `${window.location.origin}/product/${p.id}`
    if (navigator.share) {
      try { await navigator.share({ title: p.name, url }) } catch {}
    } else {
      try { await navigator.clipboard.writeText(url) } catch {
        const ta = document.createElement('textarea')
        ta.value = url; document.body.appendChild(ta); ta.select()
        document.execCommand('copy'); document.body.removeChild(ta)
      }
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <>
      <style>{css}</style>
      <div className="pcard">
        <Link to={`/product/${p.id}`} style={{textDecoration:'none'}}>
          <div className="pcard-img-wrap">
            <div className="pcard-img">
              {p.image_url
                ? <img src={p.image_url} alt={p.name} loading="lazy" />
                : <div className="pcard-noimg">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
                  </div>
              }
            </div>
            <div className="pcard-badges">
              {promoted && <span className="pcard-top">Топ</span>}
              {p.category && <span className="pcard-cat">{p.category}</span>}
            </div>
          </div>
        </Link>

        <button className={`pcard-fav ${favorited ? 'active' : ''}`} onClick={handleFav} disabled={favoriteBusy} aria-label={favorited ? 'Убрать из избранного' : 'Добавить в избранное'}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill={favorited ? '#EF4444' : 'none'} stroke={favorited ? '#EF4444' : '#94A3B8'} strokeWidth="2">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </button>

        <div className="pcard-body">
          <Link to={`/product/${p.id}`} className="pcard-name">{p.name}</Link>
          {p.description && <div className="pcard-desc">{p.description}</div>}
          <div>
            <div className="pcard-pay">
              <div>
                <div className="pcard-price">{fmt(p.price)}</div>
                {p.unit && <div className="pcard-unit">за {p.unit}</div>}
              </div>
              {monthlyPrice && <div className="pcard-monthly">{monthlyPrice}</div>}
            </div>
          </div>
          {p.avg_rating != null && p.avg_rating > 0 && (
            <div className="pcard-rating">
              <Stars rating={p.avg_rating} />
              <span className="pcard-rating-val">{p.avg_rating.toFixed(1)}</span>
              {p.review_count != null && p.review_count > 0 && (
                <span className="pcard-rating-cnt">({p.review_count})</span>
              )}
            </div>
          )}
          {likes > 0 && (
            <div className="pcard-likes">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="#EF4444" stroke="#EF4444" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              {likes}
            </div>
          )}
          <div className="pcard-trust">
            <span>Безопасная заявка</span>
            <span>{p.view_count ? `${p.view_count} просмотров` : 'Новый товар'}</span>
          </div>
          <div className="pcard-footer">
            {p.supplier_name && (
              <div className="pcard-seller">
                <div className="seller-avatar">{p.supplier_name[0]?.toUpperCase()}</div>
                <span className="seller-name">{p.supplier_name}</span>
                {p.supplier_city && <span className="seller-city">{p.supplier_city}</span>}
              </div>
            )}
            <div className="pcard-actions">
              <button className={`btn-cart ${cartAdded ? 'added' : ''}`} onClick={handleCart} aria-label={`Добавить ${p.name} в корзину`}>
                {cartAdded
                  ? <><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><polyline points="20 6 9 17 4 12"/></svg>В корзине</>
                  : <><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>В корзину</>
                }
              </button>
              <Link to={`/product/${p.id}`} className="btn-detail">Подробнее →</Link>
              <button className="btn-share-card" onClick={handleShare} aria-label={`Поделиться товаром ${p.name}`}>
                {copied && <span className="share-tip">Скопировано!</span>}
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
