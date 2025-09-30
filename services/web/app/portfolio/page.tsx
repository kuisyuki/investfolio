'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '../contexts/AuthContext'
import { userStocksAPI, UserStock, CreateUserStockRequest } from '../utils/api'

export default function PortfolioPage() {
  const router = useRouter()
  const { isAuthenticated, isLoading: authLoading } = useAuth()

  // Form states
  const [formData, setFormData] = useState<CreateUserStockRequest>({
    ticker_symbol: '',
    quantity: 0,
    acquisition_price: 0,
  })

  // UI states
  const [stocks, setStocks] = useState<UserStock[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isLoadingStocks, setIsLoadingStocks] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, authLoading, router])

  // Fetch user stocks on component mount
  useEffect(() => {
    if (isAuthenticated) {
      fetchUserStocks()
    }
  }, [isAuthenticated])

  const fetchUserStocks = async () => {
    setIsLoadingStocks(true)
    try {
      const userStocks = await userStocksAPI.getAll()
      setStocks(userStocks)
    } catch (error) {
      console.error('Failed to fetch stocks:', error)
      // If the API is not yet implemented, just set empty array
      setStocks([])
    } finally {
      setIsLoadingStocks(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? Number(value) : value,
    }))
  }

  const validateForm = (): boolean => {
    if (!formData.ticker_symbol.trim()) {
      setError('銘柄コードを入力してください')
      return false
    }
    if (formData.quantity <= 0) {
      setError('数量は1以上の値を入力してください')
      return false
    }
    if (formData.acquisition_price <= 0) {
      setError('取得単価は0より大きい値を入力してください')
      return false
    }
    return true
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setSuccessMessage(null)

    if (!validateForm()) {
      return
    }

    setIsSubmitting(true)
    try {
      await userStocksAPI.create(formData)

      // Clear form
      setFormData({
        ticker_symbol: '',
        quantity: 0,
        acquisition_price: 0,
      })

      setSuccessMessage('持ち株を登録しました')

      // Refresh stock list
      await fetchUserStocks()

      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null)
      }, 3000)
    } catch (error) {
      const message = error instanceof Error ? error.message : '登録に失敗しました'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center items-center h-64">
          <div className="text-gray-500">読み込み中...</div>
        </div>
      </div>
    )
  }

  // Don't render anything if not authenticated (will redirect)
  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">ポートフォリオ</h1>

      {/* Registration Form */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4">持ち株登録</h2>

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Success Message */}
        {successMessage && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {successMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label htmlFor="ticker_symbol" className="block text-sm font-medium text-gray-700 mb-2">
                銘柄コード
              </label>
              <input
                type="text"
                id="ticker_symbol"
                name="ticker_symbol"
                value={formData.ticker_symbol}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="例: 7974"
                required
              />
            </div>

            <div>
              <label htmlFor="quantity" className="block text-sm font-medium text-gray-700 mb-2">
                数量
              </label>
              <input
                type="number"
                id="quantity"
                name="quantity"
                value={formData.quantity || ''}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="100"
                min="1"
                required
              />
            </div>

            <div>
              <label htmlFor="acquisition_price" className="block text-sm font-medium text-gray-700 mb-2">
                取得単価 (円)
              </label>
              <input
                type="number"
                id="acquisition_price"
                name="acquisition_price"
                value={formData.acquisition_price || ''}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="1000"
                min="0.01"
                step="0.01"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className={`px-6 py-2 rounded-md text-white font-medium transition-colors ${
              isSubmitting
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            }`}
          >
            {isSubmitting ? '登録中...' : '登録'}
          </button>
        </form>
      </div>

      {/* Stock List */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">登録済み持ち株一覧</h2>

        {isLoadingStocks ? (
          <div className="text-center py-8 text-gray-500">
            読み込み中...
          </div>
        ) : stocks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            まだ持ち株が登録されていません
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    銘柄コード
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    数量
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    取得単価
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    取得金額
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    登録日時
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stocks.map((stock) => (
                  <tr key={stock.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {stock.ticker_symbol}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stock.quantity.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ¥{stock.acquisition_price.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ¥{(stock.quantity * stock.acquisition_price).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(stock.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Back Button */}
      <div className="mt-6">
        <Link
          href="/"
          className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline inline-block"
        >
          戻る
        </Link>
      </div>
    </div>
  )
}