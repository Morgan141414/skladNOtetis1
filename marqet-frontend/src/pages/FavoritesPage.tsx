import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useStore } from '../store'
import { apiGetMyFavorites, apiToggleFavorite } from '../api'
import type { Product } from '../components/ProductCard'
import { useToast } from '../components/Toast'

const css = `
.fav-wrap { max-width:1280px; margin:0 auto; padding:32px 20px 60px; }
.fav-title { font-size:26px; font-weight:900; color:#1E1B4B; margin-bottom:24px; display:flex; align-items:center; gap:10px; }
.fav-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:18px; }
.fav-empty { text-align:center; padding:80px 0; }
.fav-empty h3 { font-size:20px; font-weight:700; color:#475569; margin-bottom:8px; }
.fav-empty p { font-size:14px; color:#94A3B8; margin-bottom:24px; }
.fcard { background:#fff; border-radius:16px; border:1px solid #E2E8F0; overflow:hidden; transition:all .22s; position:relative; }
.fcard:hover { border-color:#C7D2FE; box-shadow:0 8px 24px rgba(91,79,232,.1); transform:translateY(-2px); }
.fcard-img { width:100%; aspect-ratio:4/3; background:#F1F5F9; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.fcard-img img { width:100%; height:100%; object-fit:cover; }
.fcard-body { padding:14px 16px 16px; }
.fcard-name { font-size:15px; font-weight:700; color:#1E1B4B; line-height:1.3; margin-bottom:6px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.fcard-price { font-size:20px; font-weight:800; color:#5B4FE8; margin-bottom:8px; }
.fcard-seller { font-size:12px; color:#64748B; }
.fcard-unfav { position:absolute; top:10px; right:10px; width:32px; height:32px; border-radius:50%; background:#fff; border:none; box-shadow:0 2px 8px rgba(0,0,0,.12); display:flex; align-items:center; justify-content:center; cursor:pointer; color:#EF4444; transition:all .18s; }
.fcard-unfav:hover { background:#FEF2F2; transform:scale(1.1); }
.fcard-unfav:disabled { opacity:.6; cursor:wait; transform:none; }
`

function fmt(n: number | null): string {
  return n !== null ? n.toLocaleString('ru-KZ') + ' ₸' : 'По запросу'
}

function mapRow(r: any): Product {
  return {
    id: r.id,
    supplier_id: r.supplier_id,
    name: r.product_name,
    description: r.description,
    price: r.unit_price != null ? parseFloat(r.unit_price) : null,
    unit: r.unit,
    supplier_name: r.supplier_name,
    supplier_phone: r.supplier_phone,
    image_url: r.image_url,
    category: r.category,
    avg_rating: r.avg_rating,
    review_count: r.review_count,
  }
}

export default function FavoritesPage() {
  const { user, openAuth } = useStore()
  const { show } = useToast()
  const [items, setItems] = useState<Array<Product>>([])
  const [loading, setLoading] = useState(true)
  const [removingIds, setRemovingIds] = useState<Set<number>>(() => new Set())

  useEffect(() => {
    if (!user) { openAuth('login'); return }
    apiGetMyFavorites()
      .then(d => { setItems(d.items.map(mapRow)) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [user])

  async function unfav(id: number) {
    if (removingIds.has(id)) return
    setRemovingIds(prev => new Set(prev).add(id))
    try {
      const result = await apiToggleFavorite(id)
      if (!result.favorited) {
        setItems(prev => prev.filter(x => x.id !== id))
        show('Товар убран из избранного')
        return
      }
      show('Товар остался в избранном')
    } catch {
      show('Не удалось убрать из избранного')
    } finally {
      setRemovingIds(prev => {
        const next = new Set(prev)
        next.delete(id)
        return next
      })
    }
  }

  if (!user) return null

  return (
    <>
      <style>{css}</style>
      <div className="fav-wrap">
        <h1 className="fav-title">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="#EF4444" stroke="#EF4444" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          Избранное
        </h1>

        {loading ? (
          <div style={{textAlign:'center',padding:'60px 0',color:'#94A3B8'}}>Загрузка...</div>
        ) : items.length === 0 ? (
          <div className="fav-empty">
            <div style={{fontSize:56,marginBottom:12}}>💔</div>
            <h3>Избранных пока нет</h3>
            <p>Нажмите на сердечко на карточке товара, чтобы сохранить</p>
            <Link to="/" style={{display:'inline-flex',alignItems:'center',gap:8,padding:'12px 24px',borderRadius:14,background:'var(--brand-grad)',color:'#fff',fontWeight:700,fontSize:14}}>
              Перейти в каталог
            </Link>
          </div>
        ) : (
          <div className="fav-grid">
            {items.map(p => (
              <div key={p.id} className="fcard">
                <button
                  className="fcard-unfav"
                  onClick={() => unfav(p.id)}
                  disabled={removingIds.has(p.id)}
                  title="Убрать из избранного"
                  aria-label={`Убрать ${p.name} из избранного`}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                </button>
                <Link to={`/product/${p.id}`} style={{textDecoration:'none'}}>
                  <div className="fcard-img">
                    {p.image_url
                      ? <img src={p.image_url} alt={p.name} loading="lazy" />
                      : <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" strokeWidth="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
                    }
                  </div>
                  <div className="fcard-body">
                    <div className="fcard-name">{p.name}</div>
                    <div className="fcard-price">{fmt(p.price)}</div>
                    {p.supplier_name && <div className="fcard-seller">{p.supplier_name}</div>}
                  </div>
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  )
}
