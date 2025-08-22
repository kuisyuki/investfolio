# 技術スタック一覧

## フロントエンド

| 技術 | バージョン | 用途 |
|------|------------|------|
| Node.js | LTS (Volta管理) | JavaScript実行環境 |
| TypeScript | ^5.0 | 型安全なJavaScript |
| Next.js | 14.2.5 | Reactフレームワーク |
| React | ^18.3.1 | UIライブラリ |
| React DOM | ^18.3.1 | React DOM操作 |
| TailwindCSS | ^3.4.7 | CSSフレームワーク |
| Tailwind Merge | ^2.4.0 | Tailwindクラス結合 |
| Recharts | ^2.12.7 | React用チャートライブラリ |
| TanStack React Query | ^5.51.1 | サーバー状態管理 |
| Zustand | ^4.5.4 | クライアント状態管理 |
| Axios | ^1.6.7 | HTTP クライアント |
| Zod | ^3.23.8 | スキーマバリデーション |
| date-fns | ^3.6.0 | 日付操作ライブラリ |
| clsx | ^2.1.1 | 条件付きクラス名 |
| pnpm | 最新 | パッケージマネージャー |
| Volta | 最新 | Node.jsバージョン管理 |

## バックエンド

| 技術 | バージョン | 用途 |
|------|------------|------|
| Python | 3.12+ | プログラミング言語 |
| FastAPI | 0.116.1 | WebAPIフレームワーク |
| uvicorn | 0.35.0 | ASGIサーバー |
| SQLAlchemy | 2.0.43 | ORM |
| PyMySQL | 1.1.1 | MySQL ドライバー |
| Pydantic | 2.11.7 | データバリデーション |
| Pydantic Settings | 2.10.1 | 設定管理 |
| yfinance | 0.2.65 | 株価データ取得 |
| APScheduler | 3.11.0 | タスクスケジューラー |
| python-jose | 3.5.0 | JWT処理 |
| passlib | 1.7.4 | パスワードハッシュ化 |
| python-multipart | 0.0.20 | マルチパートフォーム処理 |
| httpx | 0.28.1 | 非同期HTTPクライアント |
| requests | 2.32.5 | HTTPクライアント |
| redis | 6.4.0 | Redisクライアント |
| structlog | 25.4.0 | 構造化ログ |
| python-json-logger | 3.3.0 | JSONログフォーマッター |
| python-dotenv | 1.1.1 | 環境変数管理 |
| fastapi-cors | 0.0.6 | CORS処理 |
| cryptography | 41.0.7 | 暗号化ライブラリ |

## テスト・品質管理

| 技術 | バージョン | 用途 |
|------|------------|------|
| pytest | 8.4.1 | Pythonテストフレームワーク |
| pytest-asyncio | 1.1.0 | 非同期テスト |
| pytest-mock | 3.14.1 | モックテスト |
| Black | 25.1.0 | Pythonコードフォーマッター |
| isort | 6.0.1 | import文整理 |
| Ruff | 0.12.10 | 高速Python リンター |
| ESLint | ^8.0 | JavaScript/TypeScriptリンター |
| ESLint Config Next | 14.2.5 | Next.js用ESLint設定 |

## データベース・インフラ

| 技術 | バージョン | 用途 |
|------|------------|------|
| MySQL | 8.0 | メインデータベース |
| Redis | 7-alpine | キャッシュ・セッション管理 |
| sql-migrate | 最新 | DBマイグレーション（Go製） |
| Nginx | alpine | リバースプロキシ |
| Docker | 最新 | コンテナ化 |
| Docker Compose | 最新 | マルチコンテナ管理 |

## 監視・ログ（ELK Stack）

| 技術 | バージョン | 用途 |
|------|------------|------|
| Elasticsearch | 8.11.0 | ログ保存・検索 |
| Kibana | 8.11.0 | データ可視化 |
| Filebeat | 8.11.0 | ログ収集 |

## 開発環境・ツール

| 技術 | バージョン | 用途 |
|------|------------|------|
| Ubuntu | 24.04 | 開発コンテナOS |
| VS Code | 最新 | IDE |
| DevContainer | 最新 | 開発環境コンテナ化 |
| uv | 最新 | Python パッケージマネージャー |
| uvx | 最新 | Python ツール実行環境 |
| PostCSS | ^8.4.40 | CSS後処理 |
| Autoprefixer | ^10.4.19 | CSSベンダープレフィックス |

## 外部サービス・API

| サービス | バージョン/プラン | 用途 |
|----------|-------------------|------|
| Yahoo Finance API | - | 株価データ取得（yfinance 0.2.65経由） |
| Alpha Vantage | 無料プラン | 株価データ取得（バックアップ） |

## 開発支援ツール

| 技術 | バージョン | 用途 |
|------|------------|------|
| @types/node | ^20 | Node.js型定義 |
| @types/react | ^18 | React型定義 |
| @types/react-dom | ^18 | React DOM型定義 |

## バージョン管理・更新ポリシー

### 更新頻度
- **セキュリティアップデート**: 即座に適用
- **マイナーアップデート**: 月次で検討
- **メジャーアップデート**: 四半期で検討・テスト後適用

### 固定バージョン vs 最新追従
- **固定**: MySQL 8.0, ELK Stack 8.11.0, Redis 7（安定性重視）
- **セマンティックバージョニング**: FastAPI, SQLAlchemy, Pydantic（メジャーバージョン固定）
- **最新追従**: 開発ツール、リンター、フォーマッター（機能改善重視）
- **LTS追従**: Node.js, Ubuntu（長期サポート重視）

### 互換性確認
- FastAPI 0.116.1 + SQLAlchemy 2.0.43の互換性
- Next.js 14.2.5 + React 18.3.1の互換性
- ELK Stack 8.11.0の各コンポーネント間互換性
- Python 3.12 + 各ライブラリの互換性
- Pydantic v2 + FastAPI の互換性

## 開発環境セットアップ順序

1. **基盤環境**
   - Docker, Docker Compose
   - VS Code + DevContainer

2. **言語・ランタイム**
   - Python 3.12
   - Node.js (Volta管理)
   - Go (sql-migrate用)

3. **パッケージマネージャー**
   - pip (Python)
   - pnpm (Node.js)

4. **開発ツール**
   - uv, uvx (Python)
   - Volta (Node.js管理)
   - sql-migrate (DB マイグレーション)

5. **インフラサービス**
   - MySQL 8.0
   - Redis 7
   - ELK Stack 8.11.0
   - Nginx (alpine)

この技術スタック一覧は、プロジェクトの技術的な基盤を明確にし、新しい開発者のオンボーディングや技術選定の参考資料として活用できます。