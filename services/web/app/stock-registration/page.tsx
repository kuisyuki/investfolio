export default function StockRegistrationPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">持ち株の登録</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <form>
          <div className="mb-4">
            <label htmlFor="stock-code" className="block text-gray-700 font-bold mb-2">銘柄コード</label>
            <input type="text" id="stock-code" name="stock-code" className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
          </div>
          <div className="mb-4">
            <label htmlFor="quantity" className="block text-gray-700 font-bold mb-2">株数</label>
            <input type="number" id="quantity" name="quantity" className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
          </div>
          <div className="mb-4">
            <label htmlFor="acquisition-price" className="block text-gray-700 font-bold mb-2">取得単価</label>
            <input type="number" id="acquisition-price" name="acquisition-price" className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
          </div>
          <div className="flex items-center justify-between">
            <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
              登録
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}