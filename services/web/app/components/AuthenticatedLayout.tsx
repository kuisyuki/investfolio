'use client'

import { useAuth } from '../contexts/AuthContext'
import Link from 'next/link'

export default function AuthenticatedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, logout } = useAuth()

  // if (!isAuthenticated) {
  //   return null
  // }

  return (
    <>
      <nav className="bg-primary-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">InvestFolio</h1>
          <div className="flex items-center space-x-4">
            <Link href="/" className="hover:underline">ホーム</Link>
            <Link href="/portfolio" className="hover:underline">ポートフォリオ</Link>
            <Link href="/transactions" className="hover:underline">取引履歴</Link>
            <Link href="/analysis" className="hover:underline">分析</Link>
            <button 
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded"
            >
              ログアウト
            </button>
          </div>
        </div>
      </nav>
      <main className="min-h-screen">{children}</main>
      <footer className="bg-gray-800 text-white p-4 mt-8">
        <div className="container mx-auto text-center">
          <p>&copy; 2024 InvestFolio. All rights reserved.</p>
        </div>
      </footer>
    </>
  )
}