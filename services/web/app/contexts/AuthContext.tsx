'use client'

import { usePathname, useRouter } from 'next/navigation'
import { createContext, ReactNode, useContext, useEffect, useState, useCallback } from 'react'
import { authAPI, User, setToken, removeToken, getToken } from '../utils/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  register: (userData: {
    username: string
    email: string
    password: string
    full_name: string
  }) => Promise<void>
  checkAuth: () => Promise<void>
  clearError: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()
  const pathname = usePathname()

  // Check authentication status on mount
  const checkAuth = useCallback(async () => {
    const token = getToken()
    if (!token) {
      setIsLoading(false)
      setIsAuthenticated(false)
      setUser(null)
      return
    }

    try {
      const userData = await authAPI.me()
      setUser(userData)
      setIsAuthenticated(true)
    } catch (error) {
      console.error('Auth check failed:', error)
      setIsAuthenticated(false)
      setUser(null)
      removeToken()
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  // Protected route handling
  useEffect(() => {
    const publicPaths = ['/login', '/register']
    const isPublicPath = publicPaths.includes(pathname)

    if (!isLoading && !isAuthenticated && !isPublicPath) {
      router.push('/login')
    }
  }, [isAuthenticated, isLoading, pathname, router])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true)
    setError(null)

    try {
      // Call actual API
      const response = await authAPI.login(email, password)
      setToken(response.access_token)
      setUser(response.user)
      setIsAuthenticated(true)

      // Redirect to top page after successful login
      router.push('/')
    } catch (error) {
      const message = error instanceof Error ? error.message : 'メールアドレスまたはパスワードが正しくありません'
      setError(message)
      setIsAuthenticated(false)
      setUser(null)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [router])

  const register = useCallback(async (userData: {
    username: string
    email: string
    password: string
    full_name: string
  }) => {
    setIsLoading(true)
    setError(null)

    try {
      // Register the user
      await authAPI.register(userData)

      // After successful registration, automatically log in
      const loginResponse = await authAPI.login(userData.email, userData.password)
      setToken(loginResponse.access_token)
      setUser(loginResponse.user)
      setIsAuthenticated(true)

      // Redirect to top page
      router.push('/')
    } catch (error) {
      const message = error instanceof Error ? error.message : '登録に失敗しました'
      setError(message)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [router])

  const logout = useCallback(async () => {
    setIsLoading(true)

    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      removeToken()
      setUser(null)
      setIsAuthenticated(false)
      setIsLoading(false)
      router.push('/login')
    }
  }, [router])

  // Show loading only for protected routes
  const publicPaths = ['/login', '/register']
  const isPublicPath = publicPaths.includes(pathname)
  const shouldShowLoading = isLoading && !isPublicPath

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated,
      isLoading,
      error,
      login,
      logout,
      register,
      checkAuth,
      clearError
    }}>
      {shouldShowLoading ? (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            <p className="mt-4 text-gray-600">読み込み中...</p>
          </div>
        </div>
      ) : (
        children
      )}
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