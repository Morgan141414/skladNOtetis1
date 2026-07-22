import { useStore } from './store'

export type Locale = 'ru' | 'kz'

export const LOCALES: { id: Locale; label: string; htmlLang: string }[] = [
  { id: 'kz', label: 'ҚАЗ', htmlLang: 'kk' },
  { id: 'ru', label: 'РУС', htmlLang: 'ru' },
]

type Dict = Record<string, string>

// Russian is the source of truth: any key missing from kz falls back to ru, so a
// half-translated key never renders as a raw dotted identifier to a visitor.
const ru: Dict = {
  'header.search': 'Поиск товаров...',
  'header.post': 'Подать объявление',
  'header.favorites': 'Избранное',
  'header.cart': 'Корзина',
  'header.account': 'Личный кабинет',
  'header.orders': 'Заказы',
  'header.paymentMethods': 'Способы оплаты',
  'header.loyalty': 'Бонусы',
  'header.sellerOrders': 'Заказы продавца',
  'header.sellerWallet': 'Кошелек продавца',
  'header.myListings': 'Мои объявления',
  'header.messages': 'Сообщения',
  'header.verifyIin': 'Подтвердить ИИН (ЭЦП)',
  'header.profile': 'Профиль',
  'header.logout': 'Выйти',
  'header.login': 'Войти',
  'header.register': 'Регистрация',
  'header.iin': 'ИИН',

  'footer.tagline': 'ВСЁ, ЧТО НУЖНО. В ОДНОМ МЕСТЕ.',
  'footer.catalog': 'Каталог',
  'footer.post': 'Подать объявление',
  'footer.favorites': 'Избранное',
  'footer.cart': 'Корзина',
  'footer.account': 'Личный кабинет',
  'footer.rights': '© 2026 marqet.kz — Маркетплейс Казахстана',

  'catalog.heroTitle': 'Маркетплейс для покупок, поставок и прямых заказов по Казахстану',
  'catalog.heroSubtitle': 'Каталог товаров, проверенные продавцы, быстрые заявки, корзина и прозрачные условия покупки в одном рабочем пространстве.',
  'catalog.heroToProducts': 'Перейти к товарам',
  'catalog.heroBecomeSeller': 'Стать продавцом',
  'catalog.statsAria': 'Показатели marketplace',
  'catalog.statProducts': 'Активных товаров',
  'catalog.statCategories': 'Категорий',
  'catalog.statScenarios': 'Сценарии',
  'catalog.statGeography': 'География',
  'catalog.statCountry': 'Казахстан',
  'catalog.trustAria': 'Преимущества marqet.kz',
  'catalog.trustSellers': 'Проверенные продавцы и профили',
  'catalog.trustCart': 'Корзина, заявки и сообщения',
  'catalog.trustInstallment': 'Рассрочный сценарий готов к подключению',
  'catalog.trustIntegration': 'Интеграция с qpartner складом',
  'catalog.all': 'Все',
  'catalog.minPrice': 'от ₸',
  'catalog.maxPrice': 'до ₸',
  'catalog.sortName': 'По названию',
  'catalog.sortCheap': 'Сначала дешевле',
  'catalog.sortExpensive': 'Сначала дороже',
  'catalog.empty': 'Ничего не найдено',
  'catalog.emptyQuery': 'По запросу «{query}» нет товаров',
  'catalog.emptyCategory': 'В этой категории пока нет товаров',
  'catalog.resetFilter': 'Сбросить фильтр',
  'catalog.noPhone': 'Номер не указан',
  'catalog.seller': 'Продавец',

  'common.close': 'Закрыть',
}

const kz: Dict = {
  'header.search': 'Тауарларды іздеу...',
  'header.post': 'Хабарландыру беру',
  'header.favorites': 'Таңдаулылар',
  'header.cart': 'Себет',
  'header.account': 'Жеке кабинет',
  'header.orders': 'Тапсырыстар',
  'header.paymentMethods': 'Төлем тәсілдері',
  'header.loyalty': 'Бонустар',
  'header.sellerOrders': 'Сатушы тапсырыстары',
  'header.sellerWallet': 'Сатушы әмияны',
  'header.myListings': 'Менің хабарландыруларым',
  'header.messages': 'Хабарламалар',
  'header.verifyIin': 'ЖСН растау (ЭЦҚ)',
  'header.profile': 'Профиль',
  'header.logout': 'Шығу',
  'header.login': 'Кіру',
  'header.register': 'Тіркелу',
  'header.iin': 'ЖСН',

  'footer.tagline': 'КЕРЕКТІҢ БӘРІ. БІР ЖЕРДЕ.',
  'footer.catalog': 'Каталог',
  'footer.post': 'Хабарландыру беру',
  'footer.favorites': 'Таңдаулылар',
  'footer.cart': 'Себет',
  'footer.account': 'Жеке кабинет',
  'footer.rights': '© 2026 marqet.kz — Қазақстан маркетплейсі',

  'catalog.heroTitle': 'Қазақстан бойынша сатып алуға, жеткізуге және тікелей тапсырыстарға арналған маркетплейс',
  'catalog.heroSubtitle': 'Тауарлар каталогы, тексерілген сатушылар, жылдам өтінімдер, себет және сатып алудың айқын шарттары — бір жұмыс кеңістігінде.',
  'catalog.heroToProducts': 'Тауарларға өту',
  'catalog.heroBecomeSeller': 'Сатушы болу',
  'catalog.statsAria': 'Marketplace көрсеткіштері',
  'catalog.statProducts': 'Белсенді тауарлар',
  'catalog.statCategories': 'Санаттар',
  'catalog.statScenarios': 'Сценарийлер',
  'catalog.statGeography': 'География',
  'catalog.statCountry': 'Қазақстан',
  'catalog.trustAria': 'marqet.kz артықшылықтары',
  'catalog.trustSellers': 'Тексерілген сатушылар мен профильдер',
  'catalog.trustCart': 'Себет, өтінімдер және хабарламалар',
  'catalog.trustInstallment': 'Бөліп төлеу сценарийі қосуға дайын',
  'catalog.trustIntegration': 'qpartner қоймасымен интеграция',
  'catalog.all': 'Барлығы',
  'catalog.minPrice': '₸ бастап',
  'catalog.maxPrice': '₸ дейін',
  'catalog.sortName': 'Атауы бойынша',
  'catalog.sortCheap': 'Алдымен арзандары',
  'catalog.sortExpensive': 'Алдымен қымбаттары',
  'catalog.empty': 'Ештеңе табылмады',
  'catalog.emptyQuery': '«{query}» сұранысы бойынша тауар жоқ',
  'catalog.emptyCategory': 'Бұл санатта әзірге тауар жоқ',
  'catalog.resetFilter': 'Сүзгіні тазалау',
  'catalog.noPhone': 'Нөмір көрсетілмеген',
  'catalog.seller': 'Сатушы',

  'common.close': 'Жабу',
}

const dicts: Record<Locale, Dict> = { ru, kz }

export function translate(locale: Locale, key: string, vars?: Record<string, string | number>): string {
  let out = dicts[locale]?.[key] ?? ru[key] ?? key
  if (vars) {
    for (const [name, value] of Object.entries(vars)) {
      out = out.split(`{${name}}`).join(String(value))
    }
  }
  return out
}

/** "1 товар / 2 товара / 5 товаров" in Russian; Kazakh does not inflect counted nouns. */
export function formatProductCount(locale: Locale, count: number): string {
  if (locale === 'kz') return `${count} тауар`
  const tens = Math.abs(count) % 100
  const ones = tens % 10
  if (tens > 10 && tens < 20) return `${count} товаров`
  if (ones === 1) return `${count} товар`
  if (ones > 1 && ones < 5) return `${count} товара`
  return `${count} товаров`
}

/** Translation hook. Re-renders the component when the locale changes. */
export function useT() {
  const locale = useStore(s => s.locale)
  return (key: string, vars?: Record<string, string | number>) => translate(locale, key, vars)
}

export function useLocale(): [Locale, (l: Locale) => void] {
  const locale = useStore(s => s.locale)
  const setLocale = useStore(s => s.setLocale)
  return [locale, setLocale]
}
