import { BrowserRouter, Link, Navigate, Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import { useStore } from './store'
import { apiMe } from './api'
import Header from './components/Header'
import AuthModal from './components/AuthModal'
import NCAVerifyModal from './components/NCAVerifyModal'
import OfertaModal from './components/OfertaModal'
import SupportWidget from './components/SupportWidget'
import { ToastProvider } from './components/Toast'
import CatalogPage from './pages/CatalogPage'
import ProductDetailPage from './pages/ProductDetailPage'
import PostListingPage from './pages/PostListingPage'
import AccountPage from './pages/AccountPage'
import SellerPage from './pages/SellerPage'
import MessagesPage from './pages/MessagesPage'
import CartPage from './components/CartPage'
import FavoritesPage from './pages/FavoritesPage'
import CheckoutPage from './pages/CheckoutPage'
import AccountHubPage from './pages/account/AccountHubPage'
import OrdersPage from './pages/account/OrdersPage'
import OrderDetailPage from './pages/account/OrderDetailPage'
import PaymentMethodsPage from './pages/account/PaymentMethodsPage'
import LoyaltyPage from './pages/account/LoyaltyPage'
import SellerOrdersPage from './pages/seller/SellerOrdersPage'
import SellerWalletPage from './pages/seller/SellerWalletPage'

const css = `
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --brand:#5B4FE8;--brand2:#3B82F6;--brand-dark:#4338CA;
  --brand-light:#EEF2FF;--brand-grad:linear-gradient(135deg,#5B4FE8 0%,#3B82F6 100%);
  --dark:#1E1B4B;
}
body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#F5F5FA; color:#1E293B; }
a { color:inherit; text-decoration:none; }
button { cursor:pointer; font-family:inherit; }
input, select, textarea { font-family:inherit; }
.footer { background:#1E1B4B; color:#94A3B8; text-align:center; padding:28px 20px; font-size:13px; margin-top:48px; line-height:2; }
.footer-brand { font-size:16px; font-weight:800; background:var(--brand-grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.footer a { color:#818CF8; }
.footer-links { display:flex; justify-content:center; gap:20px; margin-top:8px; flex-wrap:wrap; }
`

function OfertaWithRefresh() {
  const { setUser, token } = useStore()
  async function handleSigned() {
    if (!token) return
    try { const me = await apiMe(token); setUser(me) } catch {}
  }
  return <OfertaModal onSigned={handleSigned} />
}

export default function App() {
  const { authOpen, ncaOpen, ofertaOpen } = useStore()

  useEffect(() => {
    function preventBackspace(e: KeyboardEvent) {
      if (e.key !== 'Backspace') return
      const target = e.target as HTMLElement
      const tag = target.tagName
      if (tag === 'INPUT' || tag === 'TEXTAREA' || target.isContentEditable) return
      e.preventDefault()
    }
    document.addEventListener('keydown', preventBackspace)
    return () => document.removeEventListener('keydown', preventBackspace)
  }, [])

  return (
    <ToastProvider>
      <style>{css}</style>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<CatalogPage />} />
          <Route path="/product/:id" element={<ProductDetailPage />} />
          <Route path="/seller/:id" element={<SellerPage />} />
          <Route path="/post" element={<PostListingPage />} />
          <Route path="/account" element={<Navigate to="/account/hub" replace />} />
          <Route path="/account/listings" element={<AccountPage />} />
          <Route path="/account/hub" element={<AccountHubPage />} />
          <Route path="/account/orders" element={<OrdersPage />} />
          <Route path="/account/orders/:id" element={<OrderDetailPage />} />
          <Route path="/account/payment-methods" element={<PaymentMethodsPage />} />
          <Route path="/account/loyalty" element={<LoyaltyPage />} />
          <Route path="/seller/orders" element={<SellerOrdersPage />} />
          <Route path="/seller/wallet" element={<SellerWalletPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="/messages/:id" element={<MessagesPage />} />
          <Route path="*" element={<CatalogPage />} />
        </Routes>
        <footer className="footer">
          <div className="footer-brand">marqet.kz</div>
          <div style={{marginTop:6,opacity:.7}}>ВСЁ, ЧТО НУЖНО. В ОДНОМ МЕСТЕ.</div>
          <div className="footer-links">
            <a href="mailto:info@marqet.kz">info@marqet.kz</a>
            <Link to="/">Каталог</Link>
            <Link to="/post">Подать объявление</Link>
            <Link to="/favorites">Избранное</Link>
            <Link to="/cart">Корзина</Link>
            <Link to="/account/hub">Личный кабинет</Link>
          </div>
          <div style={{marginTop:12,opacity:.4,fontSize:11}}>© 2026 marqet.kz — Маркетплейс Казахстана</div>
        </footer>
        <SupportWidget />
        {authOpen && <AuthModal />}
        {ncaOpen && <NCAVerifyModal />}
        {ofertaOpen && <OfertaWithRefresh />}
      </BrowserRouter>
    </ToastProvider>
  )
}
