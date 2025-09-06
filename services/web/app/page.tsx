import AuthenticatedLayout from './components/AuthenticatedLayout'

export default function Home() {

  return (
    <AuthenticatedLayout>
      <div className="container mx-auto px-4 py-8">

      <div className="bg-gradient-to-r from-primary-500 to-primary-700 text-white p-8 rounded-lg mb-8">
        <h1 className="text-4xl font-bold mb-4">資産管理システム</h1>
        <p className="text-xl">InvestFolioで賢く資産を管理しましょう</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-primary-600">ポートフォリオ管理</h2>
          <p className="text-gray-600 mb-4">
            複数の投資商品を一元管理し、資産配分を最適化します。
          </p>
          <a href="/portfolio" className="text-primary-500 hover:underline">詳細を見る →</a>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-primary-600">取引履歴</h2>
          <p className="text-gray-600 mb-4">
            すべての取引を記録し、パフォーマンスを追跡します。
          </p>
          <a href="/transactions" className="text-primary-500 hover:underline">詳細を見る →</a>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4 text-primary-600">パフォーマンス分析</h2>
          <p className="text-gray-600 mb-4">
            詳細な分析とレポートで投資判断をサポートします。
          </p>
          <a href="/analysis" className="text-primary-500 hover:underline">詳細を見る →</a>
        </div>
      </div>
      
      <div className="mt-12 bg-gray-50 p-8 rounded-lg">
        <h2 className="text-3xl font-bold mb-6">主な機能</h2>
        <ul className="space-y-3">
          <li className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            リアルタイム株価取得
          </li>
          <li className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            ポートフォリオ最適化提案
          </li>
          <li className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            税務レポート自動生成
          </li>
          <li className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            リスク管理ツール
          </li>
          <li className="flex items-center">
            <span className="text-green-500 mr-2">✓</span>
            複数通貨対応
          </li>
        </ul>
      </div>
    </div>
    </AuthenticatedLayout>
  )
}