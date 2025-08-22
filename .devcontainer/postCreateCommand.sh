#!/bin/bash

# postCreateCommand.sh - DevContainer作成後に実行されるスクリプト
echo "🚀 PostCreateCommand.sh を開始します..."

# スクリプトの実行権限を付与
chmod +x /workspace/.devcontainer/postStartCommand.sh

PROJECT_ROOT=/workspace
API=$PROJECT_ROOT/services/api
WEB=$PROJECT_ROOT/services/web

# Voltaの環境変数を正しく設定
export VOLTA_HOME="/root/.volta"
export PATH="$VOLTA_HOME/bin:$PATH"

# Node.jsとpnpmが正しくインストールされているか確認
echo "📦 Node.js バージョン確認:"
node --version || echo "Node.js not found in PATH"

echo "📦 pnpm バージョン確認:"
pnpm --version || echo "pnpm not found in PATH"

# Pythonの確認
echo "🐍 Python バージョン確認:"
python --version

# Docker Composeの確認
echo "🐳 Docker Compose バージョン確認:"
docker-compose --version

# uvとuvxの確認
echo "📦 uv バージョン確認:"
uv --version || echo "uv not installed"
echo "📦 uvx バージョン確認:"
uvx --version || echo "uvx not installed"

# FastAPI用のPython環境設定
echo "🐍 FastAPI用のPythonパッケージをインストールします..."

# FastAPIプロジェクトの依存関係をインストール
cd "$API" || exit
echo "📦 Installing FastAPI dependencies..."
pip install --break-system-packages -r requirements.txt
echo "✅ FastAPI dependencies installed successfully"

# Next.jsの依存関係をインストール
cd "$WEB" || exit
echo "📦 Installing Next.js dependencies..."
pnpm install
echo "✅ Next.js dependencies installed successfully"

# GEMINI CLIのインストール
echo "📦 Installing GEMINI CLI..."
npm install -g @google/gemini-cli
echo "✅ GEMINI CLI installed successfully"

# Claude Codeのインストール
echo "📦 Installing Claude Code..."
npm install -g @anthropic-ai/claude-code
echo "✅ Claude Code installed successfully"

# Codex CLIのインストール
echo "📦 Installing Codex CLI..."
npm install -g @openai/codex
echo "✅ Codex CLI installed successfully"

echo "✅ PostCreateCommand.sh が完了しました！"
echo ""
echo "🎉 開発環境の準備が整いました。"
echo ""

echo "#######################"
echo "# Init Setup Complete #"
echo "#######################"
