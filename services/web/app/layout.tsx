import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from './contexts/AuthContext'
import UserMenu from './components/UserMenu'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '資産管理システム - InvestFolio',
  description: 'あなたの資産を効率的に管理する投資ポートフォリオ管理システム',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                  {/* Logo */}
                  <div className="flex items-center">
                    <Link href="/" className="text-xl font-bold text-indigo-600">
                      InvestFolio
                    </Link>
                  </div>

                  {/* User Menu */}
                  <UserMenu />
                </div>
              </div>
            </header>

            {/* Main Content */}
            <main>{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}