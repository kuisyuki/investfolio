import Link from "next/link";

export default function PortfolioPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">ポートフォリオ</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <p className="text-gray-600">ポートフォリオの詳細情報がここに表示されます。</p>
      </div>
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