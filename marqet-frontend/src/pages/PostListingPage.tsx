import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useStore } from '../store'
import { apiCreateListing, apiOfertaStatus } from '../api'
import { useToast } from '../components/Toast'
import ImageUpload from '../components/ImageUpload'

const CATEGORIES = [
  'Диагностическое оборудование',
  'Хирургический инструментарий',
  'Расходные материалы',
  'Лабораторное оборудование',
  'Мониторинг и жизнеобеспечение',
  'Реабилитация и ортопедия',
  'Стоматология',
  'Дезинфекция и стерилизация',
  'Медицинская мебель',
  'СИЗ и защита',
  'Рентгенология',
  'Физиотерапия',
  'Другое',
]

const css = `
.post-wrap { max-width:680px; margin:0 auto; padding:32px 20px 60px; }
.post-wrap h1 { font-size:28px; font-weight:900; color:#1E1B4B; margin-bottom:4px; }
.post-wrap .sub { font-size:15px; color:#64748B; margin-bottom:28px; }
.form-section { background:#fff; border-radius:16px; border:1px solid #E2E8F0; padding:22px; margin-bottom:14px; }
.form-section h2 { font-size:14px; font-weight:800; color:#475569; text-transform:uppercase; letter-spacing:.5px; margin-bottom:18px; padding-bottom:10px; border-bottom:1px solid #F1F5F9; }
.field { margin-bottom:14px; }
.field label { display:block; font-size:13px; font-weight:700; color:#475569; margin-bottom:5px; }
.field label span { color:#EF4444; }
.field input, .field textarea, .field select { width:100%; padding:10px 13px; border:1.5px solid #E2E8F0; border-radius:10px; font-size:14px; font-family:inherit; outline:none; transition:all .2s; background:#FAFAFA; box-sizing:border-box; }
.field input:focus, .field textarea:focus, .field select:focus { border-color:#5B4FE8; background:#fff; box-shadow:0 0 0 3px rgba(91,79,232,.1); }
.field textarea { min-height:100px; resize:vertical; line-height:1.6; }
.field-row { display:grid; grid-template-columns:2fr 1fr; gap:12px; }
.hint { font-size:11px; color:#94A3B8; margin-top:4px; }
.char-count { font-size:11px; color:#CBD5E1; float:right; }
.btn-submit { width:100%; height:52px; border-radius:14px; background:var(--brand-grad); color:#fff; font-size:16px; font-weight:800; border:none; cursor:pointer; transition:opacity .2s; }
.btn-submit:hover:not(:disabled) { opacity:.9; }
.btn-submit:disabled { opacity:.6; }
.success-card { background:#fff; border-radius:20px; border:1px solid #E2E8F0; padding:40px 24px; text-align:center; }
.success-card .check { width:64px; height:64px; background:#D1FAE5; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 16px; font-size:28px; }
.success-card h2 { font-size:22px; font-weight:800; color:#1E1B4B; margin-bottom:8px; }
.success-card p { font-size:14px; color:#64748B; margin-bottom:24px; }
.success-btns { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; }
`

export default function PostListingPage() {
  const nav = useNavigate()
  const { user, openAuth, openOferta } = useStore()
  const { show } = useToast()
  const [title, setTitle] = useState('')
  const [desc, setDesc] = useState('')
  const [price, setPrice] = useState('')
  const [unit, setUnit] = useState('шт')
  const [cat, setCat] = useState('')
  const [phone, setPhone] = useState('')
  const [imageUrl, setImageUrl] = useState('')
  const [city, setCity] = useState('')
  const [loading, setLoading] = useState(false)
  const [doneId, setDoneId] = useState<number | null>(null)

  if (!user) {
    setTimeout(() => openAuth('register'), 100)
    return null
  }

  if (doneId !== null) {
    return (
      <>
        <style>{css}</style>
        <div className="post-wrap">
          <div className="success-card">
            <div className="check">✓</div>
            <h2>Объявление опубликовано!</h2>
            <p>Ваш товар уже виден тысячам покупателей на marqet.kz</p>
            <div className="success-btns">
              <button onClick={() => nav(`/product/${doneId}`)} style={{padding:'11px 24px',borderRadius:10,background:'var(--brand-grad)',color:'#fff',fontWeight:700,border:'none',cursor:'pointer'}}>Посмотреть</button>
              <button onClick={() => nav('/account/listings')} style={{padding:'11px 24px',borderRadius:10,background:'#EEF2FF',color:'#5B4FE8',fontWeight:700,border:'none',cursor:'pointer'}}>Мои объявления</button>
              <button onClick={() => { setDoneId(null);setTitle('');setDesc('');setPrice('');setCat('');setPhone('');setImageUrl('') }} style={{padding:'11px 24px',borderRadius:10,background:'#F1F5F9',color:'#475569',fontWeight:700,border:'none',cursor:'pointer'}}>Ещё объявление</button>
            </div>
          </div>
        </div>
      </>
    )
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    try {
      const r = await apiCreateListing({
        title: title.trim(),
        description: desc.trim() || undefined,
        price: price ? parseFloat(price) : undefined,
        unit: unit || 'шт',
        category: cat || undefined,
        phone: phone.trim() || undefined,
        image_url: imageUrl || undefined,
        city: city.trim() || undefined,
      })
      show('Объявление опубликовано!')
      setDoneId(r.id)
    } catch (e: any) {
      show(e?.message || 'Ошибка при публикации', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <style>{css}</style>
      <div className="post-wrap">
        <button onClick={() => nav(-1)} style={{background:'none',border:'none',color:'#5B4FE8',fontWeight:700,fontSize:14,cursor:'pointer',marginBottom:16,display:'flex',alignItems:'center',gap:6}}>← Назад</button>
        <h1>Подать объявление</h1>
        <div className="sub">Расскажите о товаре — покупатели найдут вас</div>

        <form onSubmit={submit}>
          <div className="form-section">
            <h2>📷 Фотография</h2>
            <ImageUpload value={imageUrl} onChange={setImageUrl} />
          </div>

          <div className="form-section">
            <h2>📝 О товаре</h2>
            <div className="field">
              <label>Название <span>*</span><span className="char-count">{title.length}/200</span></label>
              <input placeholder="Например: iPhone 15 Pro 256GB" value={title} onChange={e => setTitle(e.target.value)} maxLength={200} required />
            </div>
            <div className="field">
              <label>Описание<span className="char-count">{desc.length}/2000</span></label>
              <textarea placeholder="Состояние, комплектация, причина продажи, способ доставки..." value={desc} onChange={e => setDesc(e.target.value)} maxLength={2000} />
            </div>
            <div className="field">
              <label>Категория</label>
              <select value={cat} onChange={e => setCat(e.target.value)}>
                <option value="">Выберите категорию</option>
                {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
          </div>

          <div className="form-section">
            <h2>💰 Цена</h2>
            <div className="field-row">
              <div className="field">
                <label>Цена (₸)</label>
                <input type="number" placeholder="0" min="0" step="1" value={price} onChange={e => setPrice(e.target.value)} />
                <div className="hint">Пусто → «Цена по запросу»</div>
              </div>
              <div className="field">
                <label>Единица</label>
                <select value={unit} onChange={e => setUnit(e.target.value)}>
                  <option value="шт">шт</option><option value="кг">кг</option>
                  <option value="л">л</option><option value="м">м</option>
                  <option value="пара">пара</option><option value="комплект">комплект</option>
                </select>
              </div>
            </div>
          </div>

          <div className="form-section">
            <h2>📞 Контакты</h2>
            <div className="field-row">
              <div className="field">
                <label>Телефон</label>
                <input placeholder="+7 777 000 0000" value={phone} onChange={e => setPhone(e.target.value)} />
                <div className="hint">Виден только зарегистрированным</div>
              </div>
              <div className="field">
                <label>Город</label>
                <input placeholder="Алматы" value={city} onChange={e => setCity(e.target.value)} />
              </div>
            </div>
          </div>

          <button className="btn-submit" type="submit" disabled={loading || !title.trim()}>
            {loading ? 'Публикуем...' : '🚀 Опубликовать'}
          </button>
        </form>
      </div>
    </>
  )
}
