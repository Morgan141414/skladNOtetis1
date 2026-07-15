import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import { useStore } from './store'
import { apiMe } from './api'
import { useT } from './i18n'
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

function Footer() {
  const t = useT()
  return (
    <footer className="footer">
      <div className="footer-brand">marqet.kz</div>
      <div style={{marginTop:6,opacity:.7}}>{t('footer.tagline')}</div>
      <div className="footer-links">
        <a href="mailto:info@marqet.kz">info@marqet.kz</a>
        <a href="/">{t('footer.catalog')}</a>
        <a href="/post">{t('footer.post')}</a>
        <a href="/favorites">{t('footer.favorites')}</a>
        <a href="/cart">{t('footer.cart')}</a>
        <a href="/account">{t('footer.account')}</a>
      </div>
      <div style={{marginTop:12,opacity:.4,fontSize:11}}>{t('footer.rights')}</div>
    </footer>
  )
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
          <Route path="/account" element={<AccountPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="/messages/:id" element={<MessagesPage />} />
          <Route path="*" element={<CatalogPage />} />
        </Routes>
        <Footer />
        <SupportWidget />
        {authOpen && <AuthModal />}
        {ncaOpen && <NCAVerifyModal />}
        {ofertaOpen && <OfertaWithRefresh />}
      </BrowserRouter>
    </ToastProvider>
  )
}
