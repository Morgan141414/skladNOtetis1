import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface User {
  id: number
  name: string
  email: string
  phone?: string
  roles: string[]
  is_nca_verified?: boolean
  iin?: string | null
  oferta_signed?: boolean
}

export type Locale = 'ru' | 'kz'

interface AppState {
  token: string | null
  user: User | null
  locale: Locale
  authOpen: boolean
  authMode: 'login' | 'register'
  ncaOpen: boolean
  ofertaOpen: boolean
  setLocale: (l: Locale) => void
  setToken: (t: string | null) => void
  setUser: (u: User | null) => void
  logout: () => void
  openAuth: (mode?: 'login' | 'register') => void
  closeAuth: () => void
  openNCA: () => void
  closeNCA: () => void
  openOferta: () => void
  closeOferta: () => void
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      locale: 'ru',
      authOpen: false,
      authMode: 'login',
      ncaOpen: false,
      ofertaOpen: false,
      setLocale: (locale) => set({ locale }),
      setToken: (token) => set({ token }),
      setUser: (user) => set({ user }),
      logout: () => set({ token: null, user: null }),
      openAuth: (mode = 'login') => set({ authOpen: true, authMode: mode }),
      closeAuth: () => set({ authOpen: false }),
      openNCA: () => set({ ncaOpen: true }),
      closeNCA: () => set({ ncaOpen: false }),
      openOferta: () => set({ ofertaOpen: true }),
      closeOferta: () => set({ ofertaOpen: false }),
    }),
    { name: 'marqet-auth', partialize: (s) => ({ token: s.token, user: s.user, locale: s.locale }) }
  )
)
