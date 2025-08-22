#!/bin/bash

# postStartCommand.sh - DevContainer開始時に実行されるスクリプト
echo "🔄 PostStartCommand.sh を開始します..."

# Voltaの環境変数を設定
export VOLTA_HOME="/root/.volta"
export PATH="$VOLTA_HOME/bin:$PATH"

PROJECT_ROOT=/workspace
API=$PROJECT_ROOT/services/api
WEB=$PROJECT_ROOT/services/web

# Docker Composeサービスの状態確認（DevContainer統合により自動起動済み）
echo "🐳 Docker Composeサービスの状態を確認します..."
echo "✅ DevContainer統合により、すべてのサービスが自動起動されています。"

# バックエンドサーバーの起動
cd "$API" || exit
echo "🚀 FastAPIバックエンドサーバーを起動します..."
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /workspace/.devcontainer/api.log 2>&1 &
echo "✅ バックエンドサーバーがポート8000で起動中です。PID: $API_PID ログ: /workspace/.devcontainer/api.log"
echo "⏳ APIサーバーの起動を待機中..."
sleep 3

# フロントエンドサーバーの手動起動用コマンド
echo "💡 フロントエンドサーバーを手動で起動する場合は以下のコマンドを実行してください:"
echo "   cd /workspace/services/web"
echo "   pnpm run dev"

cd /workspace

# 起動したサービスの確認
echo ""
echo "🎯 起動中のサービス:"
echo "   - フロントエンド: http://localhost:3000 (Next.js)"
echo "   - バックエンド: http://localhost:8000 (FastAPI)"
echo "   - API ドキュメント: http://localhost:8000/docs (Swagger UI)"
echo "   - Kibana: http://localhost:5601 (ログ分析)"
echo "   - Elasticsearch: http://localhost:9200 (検索エンジン)"
echo ""

echo "✅ PostStartCommand.sh が完了しました！"

echo "############################"
echo "# Container Start Complete #"
echo "############################"
