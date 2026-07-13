import type {
  AccountOrdersResponse,
  AccountSummary,
  LoyaltyAccount,
  MarketplaceOrderDetail,
  PaymentMethodsResponse,
} from '../../api'

const now = new Date()
const isoDaysAgo = (days: number) => new Date(now.getTime() - days * 86400000).toISOString()

export const mockAccountSummary: AccountSummary = {
  active_orders: 2,
  delivered_orders: 7,
  bonus_points: 1840,
  saved_payment_methods: 2,
  open_messages: 1,
  seller_listings: 3,
}

export const mockOrders: AccountOrdersResponse = {
  total: 3,
  items: [
    {
      id: 9001,
      number: 'MQ-9001',
      status: 'preparing',
      created_at: isoDaysAgo(1),
      updated_at: isoDaysAgo(0),
      total_amount: 128900,
      currency: 'KZT',
      items_count: 3,
      supplier_id: 12,
      supplier_name: 'QPartner Supply',
      product_name: 'Кассовое оборудование и расходники',
      payment_status: 'paid',
      delivery_status: 'preparing',
    },
    {
      id: 9000,
      number: 'MQ-9000',
      status: 'pending_payment',
      created_at: isoDaysAgo(3),
      updated_at: isoDaysAgo(3),
      total_amount: 45900,
      currency: 'KZT',
      items_count: 1,
      supplier_id: 9,
      supplier_name: 'Almaty Market',
      product_name: 'Терминал сбора данных',
      payment_status: 'pending',
      delivery_status: 'not_started',
    },
    {
      id: 8994,
      number: 'MQ-8994',
      status: 'delivered',
      created_at: isoDaysAgo(14),
      updated_at: isoDaysAgo(8),
      total_amount: 19300,
      currency: 'KZT',
      items_count: 2,
      supplier_id: 7,
      supplier_name: 'Office Pro',
      product_name: 'Бумага и упаковка',
      payment_status: 'paid',
      delivery_status: 'delivered',
    },
  ],
}

export function mockOrderDetail(id: number): MarketplaceOrderDetail {
  const base = mockOrders.items.find(item => item.id === id) ?? mockOrders.items[0]
  return {
    ...base,
    id,
    buyer_name: 'Покупатель marqet.kz',
    buyer_phone: '+7 700 000 00 00',
    delivery_address: 'Казахстан, Алматы, проспект Абая, 10',
    notes: 'Связаться перед доставкой',
    items: [
      {
        id: 1,
        catalog_item_id: 341,
        product_name: base.product_name ?? 'Товар marqet.kz',
        quantity: 1,
        unit: 'шт',
        unit_price: base.total_amount,
        image_url: null,
      },
      {
        id: 2,
        catalog_item_id: 342,
        product_name: 'Доставка и подготовка заказа',
        quantity: 1,
        unit: 'усл',
        unit_price: 0,
        image_url: null,
      },
    ],
    timeline: [
      {
        id: 'created',
        title: 'Заказ создан',
        description: 'Мы приняли заявку и подготовили заказ к оплате.',
        created_at: base.created_at,
        status: 'draft',
      },
      {
        id: 'payment',
        title: base.payment_status === 'paid' ? 'Оплата подтверждена' : 'Ожидается оплата',
        description: base.payment_status === 'paid'
          ? 'Платежная операция подтверждена.'
          : 'После подключения платежного провайдера здесь появится ссылка на оплату.',
        created_at: base.updated_at ?? base.created_at,
        status: base.status,
      },
    ],
  }
}

export const mockPaymentMethods: PaymentMethodsResponse = {
  items: [
    {
      id: 'pm_demo_visa',
      brand: 'visa',
      last4: '4242',
      expiry_month: 12,
      expiry_year: 2029,
      holder_name: 'MARQET USER',
      is_default: true,
      status: 'active',
    },
    {
      id: 'pm_demo_kaspi',
      brand: 'kaspi',
      last4: '7744',
      expiry_month: null,
      expiry_year: null,
      holder_name: 'Kaspi token',
      is_default: false,
      status: 'active',
    },
  ],
}

export const mockLoyaltyAccount: LoyaltyAccount = {
  tier: 'silver',
  points_balance: 1840,
  points_pending: 320,
  next_tier_points: 5000,
  lifetime_spend: 612400,
  currency: 'KZT',
  history: [
    {
      id: 'lh_1',
      type: 'earn',
      title: 'Начисление за заказ MQ-8994',
      points_delta: 193,
      created_at: isoDaysAgo(8),
      order_number: 'MQ-8994',
    },
    {
      id: 'lh_2',
      type: 'redeem',
      title: 'Списание бонусов',
      points_delta: -500,
      created_at: isoDaysAgo(21),
      order_number: 'MQ-8920',
    },
  ],
}
