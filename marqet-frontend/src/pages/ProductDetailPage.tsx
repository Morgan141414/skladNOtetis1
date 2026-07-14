import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useStore } from '../store'
import { apiGetProduct, apiBrowseCatalog, apiTrackView, apiCheckFavorite, apiToggleFavorite, apiAddToCart } from '../api'
import type { Product } from '../components/ProductCard'
import ContactSellerModal from '../components/ContactSellerModal'
import { useToast } from '../components/Toast'

const css = `
.detail-wrap { max-width:1100px; margin:0 auto; padding:24px 20px 60px; }
.breadcrumb { display:flex; align-items:center; gap:6px; font-size:13px; color:#94A3B8; margin-bottom:20px; }
.breadcrumb a { color:#5B4FE8; font-weight:600; }
.breadcrumb span { color:#CBD5E1; }
.detail-grid { display:grid; grid-template-columns:1fr 360px; gap:28px; align-items:start; }
.detail-img-block { border-radius:18px; overflow:hidden; background:#F1F5F9; aspect-ratio:4/3; display:flex; align-items:center; justify-content:center; position:relative; }
.detail-img-block img { width:100%; height:100%; object-fit:cover; }
.detail-noimg { display:flex; flex-direction:column; align-items:center; gap:10px; color:#CBD5E1; }
.detail-cat-badge { position:absolute; top:14px; left:14px; background:var(--brand-grad); color:#fff; font-size:12px; font-weight:700; padding:4px 12px; border-radius:20px; }
.detail-title-row { display:flex; align-items:flex-start; gap:12px; margin:20px 0 6px; }
.detail-title { font-size:26px; font-weight:800; color:#1E1B4B; line-height:1.3; flex:1; }
.btn-save-detail,
.btn-share-detail { width:40px; height:40px; flex-shrink:0; border-radius:12px; border:1.5px solid #E2E8F0; background:#fff; color:#64748B; display:flex; align-items:center; justify-content:center; transition:all .18s; position:relative; margin-top:4px; }
.btn-save-detail:hover,
.btn-share-detail:hover { border-color:#5B4FE8; color:#5B4FE8; }
.btn-save-detail.active { border-color:#FECACA; background:#FEF2F2; color:#EF4444; }
.btn-save-detail:disabled { opacity:.65; cursor:wait; }
.share-copied-detail { position:absolute; bottom:calc(100% + 8px); right:0; background:#1E1B4B; color:#fff; font-size:11px; font-weight:600; padding:4px 10px; border-radius:6px; white-space:nowrap; pointer-events:none; }
.share-copied-detail::after { content:''; position:absolute; top:100%; right:12px; border:5px solid transparent; border-top-color:#1E1B4B; }
.detail-rating { display:flex; align-items:center; gap:6px; margin-bottom:8px; }
.detail-stars { color:#F59E0B; font-size:16px; letter-spacing:1px; }
.detail-rating-val { font-size:14px; font-weight:700; color:#92400E; }
.detail-rating-cnt { font-size:13px; color:#94A3B8; }
.detail-price { font-size:36px; font-weight:900; color:#5B4FE8; margin-bottom:4px; }
.detail-unit { font-size:14px; color:#94A3B8; margin-bottom:18px; }
.detail-desc { font-size:15px; color:#475569; line-height:1.7; margin-bottom:24px; background:#F8FAFC; border-radius:12px; padding:16px; }
.detail-meta { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; }
.meta-chip { padding:6px 14px; border-radius:20px; background:#F1F5F9; font-size:13px; color:#475569; font-weight:500; }
.seller-card { background:#fff; border:1.5px solid #E2E8F0; border-radius:16px; padding:20px; position:sticky; top:80px; }
.seller-card h3 { font-size:14px; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:.6px; margin-bottom:14px; }
.seller-row { display:flex; align-items:center; gap:12px; margin-bottom:20px; }
.seller-big-avatar { width:48px; height:48px; border-radius:50%; background:var(--brand-grad); color:#fff; font-size:20px; font-weight:800; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.seller-nm { font-size:17px; font-weight:800; color:#1E1B4B; transition:color .18s; }
.seller-nm:hover { color:#5B4FE8; }
.seller-sub { font-size:13px; color:#94A3B8; }
.btn-contact { width:100%; height:50px; border-radius:14px; font-size:15px; font-weight:700; border:none; margin-bottom:10px; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px; transition:all .18s; }
.btn-phone-full { background:var(--brand-grad); color:#fff; }
.btn-phone-full:hover { opacity:.9; }
.btn-phone-locked { background:#F8FAFC; color:#94A3B8; border:1.5px solid #E2E8F0; }
.btn-msg { background:#EEF2FF; color:#5B4FE8; }
.btn-msg:hover { background:#E0E7FF; }
.btn-cart-detail { background:#16A34A; color:#fff; }
.btn-cart-detail:hover { background:#15803D; }
.btn-cart-detail:disabled { opacity:.65; cursor:wait; }
.phone-reveal { background:#F0FDF4; border:1.5px solid #86EFAC; border-radius:14px; padding:16px; text-align:center; margin-bottom:10px; }
.ph { font-size:22px; font-weight:800; color:#166534; letter-spacing:1px; }
.ph-label { font-size:12px; color:#4ADE80; margin-bottom:4px; }
.related-section { margin-top:40px; }
.related-section h2 { font-size:20px; font-weight:800; color:#1E1B4B; margin-bottom:18px; }
.related-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px; }
.rel-card { background:#fff; border-radius:14px; border:1px solid #E2E8F0; overflow:hidden; transition:all .2s; }
.rel-card:hover { border-color:#C7D2FE; box-shadow:0 4px 16px rgba(91,79,232,.1); transform:translateY(-1px); }
.rel-card img { width:100%; aspect-ratio:4/3; object-fit:cover; }
.rel-card-body { padding:12px 14px; }
.rel-card-name { font-size:13px; font-weight:700; color:#1E1B4B; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:4px; }
.rel-card-price { font-size:15px; font-weight:800; color:#5B4FE8; }
.loading-detail { display:flex; align-items:center; justify-content:center; padding:120px 0; }
.spinner2 { width:40px; height:40px; border:3px solid #E2E8F0; border-top-color:#5B4FE8; border-radius:50%; animation:spin .7s linear infinite; }
@keyframes spin { to{transform:rotate(360deg)} }
@media(max-width:768px) { .detail-grid{grid-template-columns:1fr} .seller-card{position:static} }
.seller-map { margin-top:16px; border-radius:10px; overflow:hidden; height:140px; }
.seller-map iframe { width:100%; height:100%; border:0; }
`

function Stars({ rating }: { rating: number }) {
  const full = Math.round(rating)
  return <span className="detail-stars">{'★'.repeat(full)}{'☆'.repeat(5 - full)}</span>
}

function SellerMap({ city }: { city: string }) {
  const [src, setSrc] = useState<string | null>(null)
  useEffect(() => {
    fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(city + ', Казахстан')}&format=json&limit=1`)
      .then(r => r.json())
      .then((res: any[]) => {
        if (res[0]) {
          const lat = parseFloat(res[0].lat), lon = parseFloat(res[0].lon), d = 0.04
          setSrc(`https://www.openstreetmap.org/export/embed.html?bbox=${lon-d},${lat-d},${lon+d},${lat+d}&layer=mapnik&marker=${lat},${lon}`)
        }
      })
      .catch(() => {})
  }, [city])
  return src ? (
    <div className="seller-map"><iframe src={src} loading="lazy" title="Карта" /></div>
  ) : (
    <div style={{marginTop:12,fontSize:12,color:'#94A3B8',display:'flex',alignItems:'center',gap:4}}>
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
      {city}
    </div>
  )
}

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const nav = useNavigate()
  const { user, openAuth } = useStore()
  const { show } = useToast()
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [showPhone, setShowPhone] = useState(false)
  const [showContact, setShowContact] = useState(false)
  const [related, setRelated] = useState<Product[]>([])
  const [copied, setCopied] = useState(false)
  const [favorited, setFavorited] = useState(false)
  const [likes, setLikes] = useState(0)
  const [favoriteBusy, setFavoriteBusy] = useState(false)
  const [cartBusy, setCartBusy] = useState(false)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    setShowPhone(false)
    setShowContact(false)
    setFavorited(false)
    apiGetProduct(Number(id))
      .then(p => { setProduct(p); setLikes(p.likes_count ?? 0); apiTrackView(p.id) })
      .catch(() => nav('/'))
      .finally(() => setLoading(false))
  }, [id])

  useEffect(() => {
    if (!product) return
    setLikes(product.likes_count ?? 0)
    if (!user) {
      setFavorited(false)
      return
    }
    let mounted = true
    apiCheckFavorite(product.id)
      .then(result => {
        if (!mounted) return
        setFavorited(result.favorited)
        setLikes(result.likes_count)
      })
      .catch(() => {})
    return () => { mounted = false }
  }, [product?.id, product?.likes_count, user])

  useEffect(() => {
    if (!product?.category) return
    apiBrowseCatalog({ category: product.category, limit: 5 })
      .then(r => setRelated(r.items.filter(x => x.id !== product.id).slice(0, 4)))
      .catch(() => {})
  }, [product?.category, product?.id])

  if (loading) return (
    <><style>{css}</style>
    <div className="loading-detail"><div className="spinner2" /></div></>
  )

  if (!product) return null

  function handlePhone() {
    if (!user) { openAuth('login'); return }
    setShowPhone(true)
  }

  function handleMsg() {
    if (!user) { openAuth('login'); return }
    setShowContact(true)
  }

  async function handleFavorite() {
    if (!product) return
    if (!user) { openAuth('login'); return }
    if (favoriteBusy) return
    setFavoriteBusy(true)
    try {
      const result = await apiToggleFavorite(product.id)
      setFavorited(result.favorited)
      setLikes(result.likes_count)
      show(result.favorited ? 'Добавлено в избранное' : 'Убрано из избранного')
    } catch {
      show('Не удалось обновить избранное')
    } finally {
      setFavoriteBusy(false)
    }
  }

  async function handleCart() {
    if (!product) return
    if (!user) { openAuth('login'); return }
    if (cartBusy) return
    setCartBusy(true)
    try {
      await apiAddToCart(product.id, 1)
      window.dispatchEvent(new CustomEvent('marqet:cart-updated'))
      show('Добавлено в корзину')
    } catch {
      show('Не удалось добавить товар')
    } finally {
      setCartBusy(false)
    }
  }

  async function handleShare() {
    const url = window.location.href
    if (navigator.share) {
      try { await navigator.share({ title: product!.name, url }) } catch {}
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

  const fmt = (n: number | null) => n !== null ? n.toLocaleString('ru-KZ') + ' ₸' : 'Цена по запросу'

  return (
    <>
      <style>{css}</style>

      <div className="detail-wrap">
        <div className="breadcrumb">
          <Link to="/">Каталог</Link>
          {product.category && (
            <><span>›</span><Link to={`/?cat=${encodeURIComponent(product.category)}`}>{product.category}</Link></>
          )}
          <span>›</span>
          <span style={{ color: '#475569' }}>{product.name}</span>
        </div>

        <div className="detail-grid">
          {/* Left: image + info */}
          <div>
            <div className="detail-img-block">
              {product.image_url
                ? <img src={product.image_url} alt={product.name} />
                : <div className="detail-noimg">
                    <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
                    <span style={{ fontSize: 14 }}>Нет фотографии</span>
                  </div>
              }
              {product.category && <div className="detail-cat-badge">{product.category}</div>}
            </div>

            <div className="detail-title-row">
              <h1 className="detail-title">{product.name}</h1>
              <button
                className={`btn-save-detail ${favorited ? 'active' : ''}`}
                onClick={handleFavorite}
                disabled={favoriteBusy}
                title={favorited ? 'Убрать из избранного' : 'Добавить в избранное'}
                aria-label={favorited ? 'Убрать из избранного' : 'Добавить в избранное'}
              >
                <svg width="17" height="17" viewBox="0 0 24 24" fill={favorited ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2.4">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                </svg>
              </button>
              <button className="btn-share-detail" onClick={handleShare} title="Поделиться">
                {copied && <span className="share-copied-detail">Скопировано!</span>}
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
              </button>
            </div>

            {product.avg_rating != null && product.avg_rating > 0 && (
              <div className="detail-rating">
                <Stars rating={product.avg_rating} />
                <span className="detail-rating-val">{product.avg_rating.toFixed(1)}</span>
                {product.review_count != null && product.review_count > 0 && (
                  <span className="detail-rating-cnt">{product.review_count} {product.review_count === 1 ? 'отзыв' : product.review_count < 5 ? 'отзыва' : 'отзывов'}</span>
                )}
              </div>
            )}

            <div className="detail-price">{fmt(product.price)}</div>
            {product.unit && <div className="detail-unit">за {product.unit}</div>}

            <div className="detail-meta">
              {product.category && <span className="meta-chip">📦 {product.category}</span>}
              {product.unit && <span className="meta-chip">📏 {product.unit}</span>}
              {likes > 0 && <span className="meta-chip">♥ {likes} сохранили</span>}
            </div>

            {product.description && (
              <div className="detail-desc">{product.description}</div>
            )}
          </div>

          {/* Right: seller card */}
          <div>
            <div className="seller-card">
              <h3>Поставщик</h3>
              <div className="seller-row">
                <div className="seller-big-avatar">
                  {(product.supplier_name || 'П')[0].toUpperCase()}
                </div>
                <div>
                  <Link to={`/seller/${product.supplier_id || product.id}`} style={{ textDecoration: 'none' }}>
                    <div className="seller-nm">{product.supplier_name || 'Продавец'}</div>
                  </Link>
                  <div className="seller-sub">Медицинский поставщик</div>
                </div>
              </div>

              {showPhone && product.supplier_phone ? (
                <div className="phone-reveal">
                  <div className="ph-label">Телефон поставщика</div>
                  <div className="ph">{product.supplier_phone}</div>
                </div>
              ) : (
                <button
                  className={`btn-contact ${user ? 'btn-phone-full' : 'btn-phone-locked'}`}
                  onClick={handlePhone}
                >
                  {user ? (
                    <>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13.5a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 2.8h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.71 2.81a2 2 0 0 1-.45 2.11L7.91 10.4a16 16 0 0 0 5.68 5.68l.96-.96a2 2 0 0 1 2.11-.45c.9.35 1.85.58 2.81.71A2 2 0 0 1 22 17v-.08z"/>
                      </svg>
                      Показать телефон
                    </>
                  ) : (
                    <>
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                        <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                      </svg>
                      Войдите, чтобы увидеть номер
                    </>
                  )}
                </button>
              )}

              <button className="btn-contact btn-cart-detail" onClick={handleCart} disabled={cartBusy}>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/>
                </svg>
                {cartBusy ? 'Добавляем...' : 'В корзину'}
              </button>

              <button className="btn-contact btn-msg" onClick={handleMsg}>
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
                Написать поставщику
              </button>

              <div style={{ fontSize: 12, color: '#94A3B8', textAlign: 'center', marginTop: 12 }}>
                Безопасная сделка через marqet.kz
              </div>
              {(product as any).supplier_city && <SellerMap city={(product as any).supplier_city} />}
            </div>
          </div>
        </div>

        {/* Related products */}
        {related.length > 0 && (
          <div className="related-section">
            <h2>Похожие товары</h2>
            <div className="related-grid">
              {related.map(p => (
                <Link key={p.id} to={`/product/${p.id}`} style={{ textDecoration: 'none' }}>
                  <div className="rel-card">
                    {p.image_url
                      ? <img src={p.image_url} alt={p.name} loading="lazy" />
                      : <div style={{ aspectRatio: '4/3', background: '#F1F5F9', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#CBD5E1' }}>
                          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
                        </div>
                    }
                    <div className="rel-card-body">
                      <div className="rel-card-name">{p.name}</div>
                      <div className="rel-card-price">{p.price !== null ? p.price.toLocaleString('ru-KZ') + ' ₸' : 'По запросу'}</div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>

      {showContact && (
        <ContactSellerModal
          itemId={product.id}
          productName={product.name}
          sellerName={product.supplier_name || 'Поставщик'}
          onClose={() => setShowContact(false)}
        />
      )}
    </>
  )
}
