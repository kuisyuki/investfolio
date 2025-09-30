'use client'

import { useAuth } from '../contexts/AuthContext'
import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'

export default function UserMenu() {
  const { user, isAuthenticated, isLoading, logout } = useAuth()
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false)
      }
    }

    if (isDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isDropdownOpen])

  const handleLogout = async () => {
    setIsDropdownOpen(false)
    await logout()
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center space-x-2">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-gray-300 border-t-indigo-600"></div>
      </div>
    )
  }

  // Not authenticated - show login/register buttons
  if (!isAuthenticated) {
    return (
      <div className="flex items-center space-x-4">
        <Link
          href="/login"
          className="text-gray-700 hover:text-indigo-600 transition-colors font-medium"
        >
          ログイン
        </Link>
        <Link
          href="/register"
          className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors font-medium"
        >
          新規登録
        </Link>
      </div>
    )
  }

  // Authenticated - show user menu dropdown
  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
        className="flex items-center space-x-2 text-gray-700 hover:text-indigo-600 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 rounded-md px-3 py-2"
      >
        <div className="flex items-center space-x-2">
          {/* User Avatar */}
          <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white font-semibold">
            {user?.email?.[0]?.toUpperCase() || 'U'}
          </div>
          {/* User Info */}
          <div className="hidden sm:block text-left">
            <div className="text-sm font-medium">
              {user?.full_name || user?.username || 'ユーザー'}
            </div>
            <div className="text-xs text-gray-500">{user?.email}</div>
          </div>
          {/* Dropdown Arrow */}
          <svg
            className={`w-4 h-4 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {/* Dropdown Menu */}
      {isDropdownOpen && (
        <div className="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
          <div className="py-1">
            {/* User Info in Dropdown */}
            <div className="px-4 py-3 border-b">
              <div className="text-sm font-medium text-gray-900">
                {user?.full_name || user?.username || 'ユーザー'}
              </div>
              <div className="text-xs text-gray-500">{user?.email}</div>
            </div>

            {/* Menu Items */}
            <Link
              href="/portfolio"
              onClick={() => setIsDropdownOpen(false)}
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
            >
              ポートフォリオ
            </Link>
            <Link
              href="/transactions"
              onClick={() => setIsDropdownOpen(false)}
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
            >
              取引履歴
            </Link>
            <Link
              href="/analysis"
              onClick={() => setIsDropdownOpen(false)}
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
            >
              分析
            </Link>

            <div className="border-t my-1"></div>

            <Link
              href="/settings"
              onClick={() => setIsDropdownOpen(false)}
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
            >
              設定
            </Link>

            <div className="border-t my-1"></div>

            <button
              onClick={handleLogout}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
            >
              ログアウト
            </button>
          </div>
        </div>
      )}
    </div>
  )
}