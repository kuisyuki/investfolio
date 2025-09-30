// API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Token management
const TOKEN_KEY = 'auth_token'

export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY)
  }
  return null
}

export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token)
  }
}

export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY)
  }
}

// Custom fetch wrapper with authentication
interface FetchOptions extends RequestInit {
  requireAuth?: boolean
}

export const apiFetch = async (
  endpoint: string,
  options: FetchOptions = {}
): Promise<Response> => {
  const { requireAuth = true, ...fetchOptions } = options

  const url = `${API_BASE_URL}${endpoint}`
  const token = getToken()

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...fetchOptions.headers,
  }

  // Add authorization header if token exists and auth is required
  if (requireAuth && token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(url, {
    ...fetchOptions,
    headers,
  })

  // Handle 401 unauthorized - clear token and redirect to login
  if (response.status === 401 && requireAuth) {
    removeToken()
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  return response
}

// Auth API functions
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await apiFetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      requireAuth: false,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }))
      throw new Error(error.detail || 'Login failed')
    }

    return response.json()
  },

  register: async (userData: {
    username: string
    email: string
    password: string
    full_name: string
  }) => {
    const response = await apiFetch('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
      requireAuth: false,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Registration failed' }))

      // Handle FastAPI validation errors (422)
      if (response.status === 422 && error.detail && Array.isArray(error.detail)) {
        const messages = error.detail.map((err: any) => {
          const field = err.loc?.join('.') || 'field'
          return `${field}: ${err.msg}`
        }).join(', ')
        throw new Error(messages)
      }

      throw new Error(error.detail || 'Registration failed')
    }

    return response.json()
  },

  me: async () => {
    const response = await apiFetch('/api/auth/me', {
      method: 'GET',
      requireAuth: true,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Failed to get user info' }))
      throw new Error(error.detail || 'Failed to get user info')
    }

    return response.json()
  },

  logout: async () => {
    try {
      await apiFetch('/api/auth/logout', {
        method: 'POST',
        requireAuth: true,
      })
    } catch (error) {
      // Even if logout fails on server, clear local token
      console.error('Logout error:', error)
    } finally {
      removeToken()
    }
  },
}

// User type definition
export interface User {
  id: number
  user_id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at: string
}

// Response types
export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface RegisterResponse extends User {}

// User Stock types
export interface UserStock {
  id: number
  user_stock_id: number
  user_id: number
  ticker_symbol: string
  quantity: number
  acquisition_price: number
  created_at: string
  updated_at: string
}

export interface CreateUserStockRequest {
  ticker_symbol: string
  quantity: number
  acquisition_price: number
}

// Generic API call function
export const apiCall = async <T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> => {
  const response = await apiFetch(endpoint, options)

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || 'Request failed')
  }

  return response.json()
}

// User Stocks API
export const userStocksAPI = {
  // Get all user stocks
  getAll: async (): Promise<UserStock[]> => {
    return apiCall<UserStock[]>('/api/user-stocks/', {
      method: 'GET',
      requireAuth: true,
    })
  },

  // Create a new user stock
  create: async (data: CreateUserStockRequest): Promise<UserStock> => {
    return apiCall<UserStock>('/api/user-stocks/', {
      method: 'POST',
      body: JSON.stringify(data),
      requireAuth: true,
    })
  },
}