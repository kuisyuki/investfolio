'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter, usePathname } from 'next/navigation'

interface AuthContextType {
  isAuthenticated: boolean
  login: (email: string, password: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    // セッションストレージから認証状態を確認
    const authStatus = sessionStorage.getItem('isAuthenticated')
    if (authStatus === 'true') {
      setIsAuthenticated(true)
    }
  }, [])

  useEffect(() => {
    // 未認証時のリダイレクト処理
    const publicPaths = ['/login', '/register']
    if (!isAuthenticated && !publicPaths.includes(pathname)) {
      router.push('/login')
    }
  }, [isAuthenticated, pathname, router])

  const login = (email: string, password: string) => {
    // 仮のログイン処理（生徒が実装する部分）
    console.log('ログイン処理（未実装）:', { email, password })
    
    // デモ用：任意の入力でログイン成功とする
    setIsAuthenticated(true)
    sessionStorage.setItem('isAuthenticated', 'true')
    router.push('/')
  }

  const logout = () => {
    setIsAuthenticated(false)
    sessionStorage.removeItem('isAuthenticated')
    router.push('/login')
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}