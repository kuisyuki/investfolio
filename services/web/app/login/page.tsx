'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useAuth } from '../contexts/AuthContext'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPopup, setShowPopup] = useState(false)
  const [healthStatus, setHealthStatus] = useState('')
  const [loading, setLoading] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { login, error, clearError, isAuthenticated } = useAuth()
  const router = useRouter()

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      router.push('/')
    }
  }, [isAuthenticated, router])

  // Clear error when component unmounts or input changes
  useEffect(() => {
    clearError()
  }, [email, password, clearError])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      await login(email, password)
      // Navigation is handled in AuthContext
    } catch (error) {
      console.error('Login failed:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const checkHealth = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/health')
      const data = await response.json()
      setHealthStatus(`API Status: ${data.status}\nService: ${data.service}\nTimestamp: ${data.timestamp}`)
      setShowPopup(true)
    } catch (error) {
      setHealthStatus('APIとの接続に失敗しました')
      setShowPopup(true)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* デバッグ用ツール（左上に配置） */}
      <div className="absolute top-4 left-4 flex gap-2">
        <button
          onClick={checkHealth}
          disabled={loading}
          className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors disabled:opacity-50"
        >
          {loading ? '...' : 'API'}
        </button>
        <a
          href="http://localhost:5601"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-purple-600 text-white px-3 py-1 rounded text-sm hover:bg-purple-700 transition-colors"
        >
          Kibana
        </a>
        <a
          href="http://localhost:9200"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-yellow-600 text-white px-3 py-1 rounded text-sm hover:bg-yellow-700 transition-colors"
        >
          ES
        </a>
      </div>

      <div className="min-h-screen flex items-center justify-center">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              InvestFolio
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              アカウントにログイン
            </p>
          </div>
        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">
                メールアドレス
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="メールアドレス"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                パスワード
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="パスワード"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={isSubmitting}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'ログイン中...' : 'ログイン'}
            </button>
          </div>

          {error && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          <div className="text-center space-y-2">
            <p className="text-sm text-gray-600">
              アカウントをお持ちでない方は
            </p>
            <Link href="/register" className="font-medium text-indigo-600 hover:text-indigo-500">
              新規登録
            </Link>
          </div>
        </form>
      </div>
    </div>

    {showPopup && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-8 rounded-lg shadow-xl max-w-md">
          <h3 className="text-xl font-bold mb-4">API ヘルスチェック</h3>
          <pre className="text-sm mb-6 whitespace-pre-wrap bg-gray-100 p-4 rounded">{healthStatus}</pre>
          <button
            onClick={() => setShowPopup(false)}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors w-full"
          >
            閉じる
          </button>
        </div>
      </div>
    )}
  </div>
  )
}