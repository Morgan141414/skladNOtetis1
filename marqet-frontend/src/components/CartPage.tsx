import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useStore } from '../store'
import { apiGetCart, apiRemoveCartItem, apiUpdateCartItem, type Cart, type CartItem } from '../api'
import { useToast } from './Toast'

const css = `
.cart-wrap { max-width:900px; margin:0 auto; padding:32px 20px 60px; }
.cart-title { font-size:26px; font-weight:900; color:#1E1B4B; margin-bottom:24px; display:flex; align-items:center; gap:10px; }
.cart-empty { text-align:center; padding:80px 0; }
.cart-empty h3 { font-size:20px; font-weight:700; color:#475569; margin-bottom:8px; }
.cart-empty p { font-size:14px; color:#94A3B8; margin-bottom:24px; }
.cart-notice { display:flex; justify-content:space-between; align-items:center; gap:12px; border:1px solid #FCA5A5; background:#FEF2F2; color:#991B1B; border-radius:16px; padding:14px 16px; margin-bottom:18px; font-size:14px; font-weight:800; }
.cart-grid { display:grid; grid-template-columns:1fr 320px; gap:24px; align-items:start; }
.cart-items { display:flex; flex-direction:column; gap:10px; }
.ci-row { background:#fff; border:1px solid #E2E8F0; border-radius:14px; padding:14px 16px; display:flex; gap:14px; align-items:center; transition:all .18s; }
.ci-row:hover { border-color:#C7D2FE; }
.ci-img { width:72px; height:72px; border-radius:10px; background:#F1F5F9; overflow:hidden; flex-shrink:0; display:flex; align-items:center; justify-content:center; }
.ci-img img { width:100%; height:100%; object-fit:cover; }
.ci-info { flex:1; min-width:0; }
.ci-name { font-size:15px; font-weight:700; color:#1E1B4B; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:4px; }
.ci-seller { font-size:12px; color:#94A3B8; margin-bottom:8px; }
.ci-price { font-size:17px; font-weight:800; color:#5B4FE8; }
.ci-qty { display:flex; align-items:center; gap:8px; }
.qty-btn { width:44px; height:44px; border-radius:12px; border:1.5px solid #E2E8F0; background:#fff; font-size:18px; font-weight:700; color:#475569; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:all .15s; }
.qty-btn:hover { border-color:#5B4FE8; color:#5B4FE8; }
.qty-val { font-size:14px; font-weight:700; color:#1E1B4B; min-width:24px; text-align:center; }
.ci-del { width:44px; height:44px; border:none; background:#FEF2F2; color:#EF4444; border-radius:12px; cursor:pointer; display:flex; align-items:center; justify-content:center; flex-shrink:0; transition:all .15s; }
.ci-del:hover { background:#FEE2E2; }
.cart-summary { background:#fff; border:1.5px solid #E2E8F0; border-radius:16px; padding:24px; position:sticky; top:80px; }
.cs-title { font-size:16px; font-weight:800; color:#1E1B4B; margin-bottom:16px; }
.cs-row { display:flex; justify-content:space-between; font-size:14px; color:#475569; margin-bottom:10px; }
.cs-total { display:flex; justify-content:space-between; font-size:18px; font-weight:900; color:#1E1B4B; padding-top:12px; border-top:2px solid #F1F5F9; margin-top:4px; }
.btn-checkout { width:100%; height:50px; border-radius:14px; background:var(--brand-grad); color:#fff; font-size:15px; font-weight:700; border:none; margin-top:16px; cursor:pointer; transition:opacity .18s; }
.btn-checkout:hover { opacity:.9; }
.btn-checkout:disabled { opacity:.5; }
.cart-secondary { min-height:40px; border-radius:12px; padding:0 14px; font-weight:900; font-size:14px; border:1.5px solid #E2E8F0; background:#fff; color:#334155; display:inline-flex; align-items:center; justify-content:center; }
@media(max-width:768px) { .cart-grid{grid-template-columns:1fr} .cart-summary{position:static} .cart-notice{align-items:flex-start; flex-direction:column} }
`

export default function CartPage() {
  const { user, openAuth } = useStore()
  const nav = useNavigate()
  const { show } = useToast()
  const [cart, setCart] = useState<Cart | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadCart() {
    if (!user) { openAuth('login'); return }
    setLoading(true)
    setError('')
    try {
      setCart(await apiGetCart())
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Не удалось загрузить корзину')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadCart()
  }, [user])

  async function remove(id: number) {
    const c = await apiRemoveCartItem(id).catch(() => null)
    if (c) {
      setCart(c)
      window.dispatchEvent(new CustomEvent('marqet:cart-updated'))
      show('Удалено из корзины')
    }
  }

  async function changeQty(item: CartItem, delta: number) {
    const newQty = item.quantity + delta
    if (newQty <= 0) { remove(item.id); return }
    const c = await apiUpdateCartItem(item.id, newQty).catch(() => null)
    if (c) {
      setCart(c)
      window.dispatchEvent(new CustomEvent('marqet:cart-updated'))
    }
  }

  const fmt = (n: number | null) => n !== null ? n.toLocaleString('ru-KZ') + ' ₸' : '—'

  if (!user) return null

  return (
    <>
      <style>{css}</style>
      <div className="cart-wrap">
        <h1 className="cart-title">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          Корзина
        </h1>

        {error && (
          <div className="cart-notice">
            <span>{error}</span>
            <button className="cart-secondary" type="button" onClick={loadCart}>Повторить</button>
          </div>
        )}

        {loading ? (
          <div style={{textAlign:'center',padding:'60px 0',color:'#94A3B8'}}>Загрузка...</div>
        ) : !error && (!cart || cart.items.length === 0) ? (
          <div className="cart-empty">
            <div style={{width:56,height:56,margin:'0 auto 12px',borderRadius:18,background:'#EEF2FF',color:'#5B4FE8',display:'flex',alignItems:'center',justifyContent:'center'}}>
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
            </div>
            <h3>Корзина пуста</h3>
            <p>Добавьте товары из каталога</p>
            <Link to="/" style={{display:'inline-flex',alignItems:'center',gap:8,padding:'12px 24px',borderRadius:14,background:'var(--brand-grad)',color:'#fff',fontWeight:700,fontSize:14}}>
              Перейти в каталог
            </Link>
          </div>
        ) : !error && cart ? (
          <div className="cart-grid">
            <div className="cart-items">
              {cart.items.map(item => (
                <div key={item.id} className="ci-row">
                  <Link to={`/product/${item.catalog_item_id}`}>
                    <div className="ci-img">
                      {item.image_url
                        ? <img src={item.image_url} alt={item.product_name} />
                        : <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" strokeWidth="1.5"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>
                      }
                    </div>
                  </Link>
                  <div className="ci-info">
                    <Link to={`/product/${item.catalog_item_id}`} className="ci-name">{item.product_name}</Link>
                    {item.supplier_name && <div className="ci-seller">{item.supplier_name}</div>}
                    <div style={{display:'flex',alignItems:'center',gap:12,flexWrap:'wrap'}}>
                      <div className="ci-price">{fmt(item.unit_price ? item.unit_price * item.quantity : null)}</div>
                      <div className="ci-qty">
                        <button className="qty-btn" onClick={() => changeQty(item, -1)} aria-label={`Уменьшить количество ${item.product_name}`}>−</button>
                        <span className="qty-val">{item.quantity}</span>
                        <button className="qty-btn" onClick={() => changeQty(item, +1)} aria-label={`Увеличить количество ${item.product_name}`}>+</button>
                        <span style={{fontSize:12,color:'#94A3B8'}}>{item.unit}</span>
                      </div>
                    </div>
                  </div>
                  <button className="ci-del" onClick={() => remove(item.id)} aria-label={`Удалить ${item.product_name} из корзины`}>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>
                  </button>
                </div>
              ))}
            </div>

            <div className="cart-summary">
              <div className="cs-title">Итого</div>
              <div className="cs-row"><span>Товаров</span><span>{cart.total_items} шт.</span></div>
              <div className="cs-total"><span>Сумма</span><span>{fmt(cart.total_amount)}</span></div>
              <button className="btn-checkout" onClick={() => nav('/checkout')}>
                Оформить заказ
              </button>
              <Link to="/" style={{display:'block',textAlign:'center',marginTop:12,fontSize:13,color:'#5B4FE8',fontWeight:600}}>
                ← Продолжить покупки
              </Link>
            </div>
          </div>
        ) : null}
      </div>
    </>
  )
}
