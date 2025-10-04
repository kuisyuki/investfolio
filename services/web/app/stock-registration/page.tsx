'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import Link from 'next/link';

// 検索結果の型定義
interface StockSearchResult {
  code: string;
  name: string;
}

const StockRegistrationPage = () => {
  const [tickerSymbol, setTickerSymbol] = useState('');
  const [quantity, setQuantity] = useState('');
  const [acquisitionPrice, setAcquisitionPrice] = useState('');
  const [error, setError] = useState<string | null>(null);
  const { token } = useAuth();
  const router = useRouter();

  // 銘柄検索用のstate
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchResults, setSearchResults] = useState<StockSearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  // デバウンスuseEffect
  useEffect(() => {
    if (searchKeyword.trim() === '') {
      setSearchResults([]);
      return;
    }

    const debounceTimer = setTimeout(async () => {
      setIsSearching(true);
      try {
        const response = await fetch(`/api/stocks/search?keyword=${encodeURIComponent(searchKeyword)}`);
        if (!response.ok) {
          throw new Error('銘柄の検索に失敗しました。');
        }
        const data: StockSearchResult[] = await response.json();
        setSearchResults(data);
      } catch (error: any) {
        console.error(error);
        setSearchResults([]);
      } finally {
        setIsSearching(false);
      }
    }, 300); // 300msのデバウンス

    return () => clearTimeout(debounceTimer);
  }, [searchKeyword]);

  // 検索結果クリック時のハンドラ
  const handleSearchResultClick = (stock: StockSearchResult) => {
    setTickerSymbol(stock.code);
    setSearchKeyword('');
    setSearchResults([]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!token) {
      setError('認証が必要です。再度ログインしてください。');
      return;
    }

    try {
      const response = await fetch('/api/user-stocks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ticker_symbol: tickerSymbol,
          quantity: parseInt(quantity, 10),
          acquisition_price: parseFloat(acquisitionPrice),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '登録に失敗しました。');
      }

      alert('銘柄を登録しました。');
      router.push('/portfolio');

    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center text-gray-900">
          銘柄登録
        </h2>
        {error && (
          <div className="p-4 text-sm text-red-700 bg-red-100 rounded-lg" role="alert">
            {error}
          </div>
        )}
        <form className="space-y-6" onSubmit={handleSubmit}>
          
          {/* 銘柄名で検索 */}
          <div className="relative">
            <label
              htmlFor="search"
              className="block text-sm font-medium text-gray-700"
            >
              銘柄名で検索
            </label>
            <input
              id="search"
              type="text"
              placeholder="例: トヨタ"
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              onBlur={() => setTimeout(() => setSearchResults([]), 150)}
            />
            {isSearching && <div className="absolute right-2 top-9 text-xs text-gray-500">検索中...</div>}
            {searchResults.length > 0 && (
              <ul className="absolute z-10 w-full mt-1 overflow-auto bg-white border border-gray-300 rounded-md shadow-lg max-h-60">
                {searchResults.map((stock) => (
                  <li
                    key={stock.code}
                    className="px-4 py-2 text-sm text-gray-800 cursor-pointer hover:bg-indigo-50"
                    onMouseDown={() => handleSearchResultClick(stock)}
                  >
                    {stock.code} {stock.name}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* 銘柄コード */}
          <div>
            <label
              htmlFor="tickerSymbol"
              className="block text-sm font-medium text-gray-700"
            >
              銘柄コード
            </label>
            <input
              id="tickerSymbol"
              name="tickerSymbol"
              type="text"
              required
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-gray-50"
              value={tickerSymbol}
              onChange={(e) => setTickerSymbol(e.target.value)}
              readOnly // 検索結果から入力されるため読み取り専用に
            />
          </div>

          {/* 株数 */}
          <div>
            <label
              htmlFor="quantity"
              className="block text-sm font-medium text-gray-700"
            >
              株数
            </label>
            <input
              id="quantity"
              name="quantity"
              type="number"
              required
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />
          </div>

          {/* 取得単価 */}
          <div>
            <label
              htmlFor="acquisitionPrice"
              className="block text-sm font-medium text-gray-700"
            >
              取得単価
            </label>
            <input
              id="acquisitionPrice"
              name="acquisitionPrice"
              type="number"
              step="any"
              required
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              value={acquisitionPrice}
              onChange={(e) => setAcquisitionPrice(e.target.value)}
            />
          </div>

          <div>
            <button
              type="submit"
              className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              登録
            </button>
          </div>
        </form>
        <div className="text-center">
          <Link href="/" className="inline-block w-full px-4 py-2 mt-4 text-sm font-medium text-center text-indigo-600 bg-white border border-indigo-600 rounded-md shadow-sm hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            戻る
          </Link>
        </div>
      </div>
    </div>
  );
};

export default StockRegistrationPage;
