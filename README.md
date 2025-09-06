# InvestFolio - 資産管理システム学習プロジェクト

## 概要
InvestFolioは、クリーンアーキテクチャを採用した学習用の資産管理システムプロジェクトです。FastAPIによるバックエンドとNext.jsによるフロントエンドで構成され、実践的な金融ポートフォリオ管理機能の実装を通じて、モダンなWeb開発技術を学習することを目的としています。

## 開発環境

### Docker Desktop (推奨)
このプロジェクトはDev Containerで開発することを推奨しています。以下が必要です：
- Docker Desktop (Windows/Mac/Linux)
- Visual Studio Code
- Remote - Containers extension

### Dev Container起動方法
1. Docker Desktopを起動
2. VSCodeでプロジェクトを開く
3. コマンドパレット（F1）から「Dev Containers: Reopen in Container」を選択
4. 自動的に開発環境が構築されます

### 自動セットアップ内容
Dev Container起動時に以下が自動的に実行されます：
- Python/Node.js環境のセットアップ
- 依存パッケージのインストール
- データベースの初期化
- Claude Codeのインストール（`/workspace/.devcontainer/postCreateCommand.sh`で設定）

## プロジェクト設計

### Kiroによる要件定義・設計
`.kiro/specs/stock-portfolio-manager/`ディレクトリに、Kiroで生成された設計ドキュメントが格納されています：
- `requirements.md` - 機能要件と非機能要件の定義
- `design.md` - システム設計とアーキテクチャ
- `tech-stack.md` - 技術スタックの選定理由
- `tasks.md` - 実装タスクの詳細

### Claude Code設定
`CLAUDE.md`ファイルにClaude Code用のプロジェクト固有のガイダンスが記載されています：
- プロジェクト概要と構造
- 開発コマンド一覧
- アーキテクチャの説明
- 実装状況と今後の計画

## ディレクトリ構成

```
investfolio/
├── services/
│   ├── api/                     # バックエンドAPI
│   │   ├── application/         # アプリケーション層
│   │   │   ├── use_cases/       # ユースケース
│   │   │   └── dto/             # データ転送オブジェクト
│   │   ├── domain/              # ドメイン層
│   │   │   ├── entities/        # エンティティ
│   │   │   ├── repositories/    # リポジトリインターフェース
│   │   │   ├── services/        # ドメインサービス
│   │   │   ├── exceptions/      # ドメイン例外
│   │   │   └── value_objects/   # 値オブジェクト
│   │   ├── infrastructure/      # インフラストラクチャ層
│   │   │   ├── database/        # データベース関連
│   │   │   ├── repositories/    # リポジトリ実装
│   │   │   ├── external/        # 外部サービス連携
│   │   │   ├── models/          # データベースモデル
│   │   │   └── config/          # 設定
│   │   ├── presentation/        # プレゼンテーション層
│   │   │   ├── routes/          # APIルート
│   │   │   ├── schemas/         # リクエスト/レスポンススキーマ
│   │   │   └── middlewares/     # ミドルウェア
│   │   ├── main.py              # アプリケーションエントリポイント
│   │   └── requirements.txt     # Python依存関係
│   └── web/                     # フロントエンド
│       └── app/                 # Next.js App Router
│           ├── components/      # 共通コンポーネント
│           ├── contexts/        # Reactコンテキスト
│           ├── login/           # ログインページ
│           ├── register/        # ユーザー登録ページ
│           ├── portfolio/       # ポートフォリオページ
│           ├── transactions/    # 取引履歴ページ
│           └── analysis/        # 分析ページ
├── tests/                       # テストファイル
├── docker/                      # Docker設定（ELKスタック等）
└── CLAUDE.md                    # Claude Code用のガイダンス

```

### 開発サーバーの起動方法

#### 1. バックエンド（FastAPI）
```bash
cd services/api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 2. フロントエンド（Next.js）
```bash
cd services/web
pnpm install
pnpm dev
```

### アクセスURL
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 開発用コマンド

#### バックエンド
```bash
# コードフォーマット
cd services/api
black .
isort .

# リント
ruff .

# テスト実行
pytest tests/services/api
```

#### フロントエンド
```bash
cd services/web
pnpm lint     # ESLintの実行
pnpm build    # プロダクションビルド
```

## 技術スタック

### バックエンド
- Python 3.12
- FastAPI
- SQLAlchemy
- MySQL
- クリーンアーキテクチャ

### フロントエンド
- Next.js 14（App Router）
- TypeScript
- Tailwind CSS
- React 18
- TanStack Query（データフェッチング）
- Zustand（状態管理）
- Zod（スキーマバリデーション）

### 追加ツール・ライブラリ
- Recharts（チャート表示）
- Axios（HTTP クライアント）
- pytest（Python テスト）
- ESLint（JavaScript/TypeScript リント）

## 学習ポイント

このプロジェクトでは以下の概念を学習できます：

- **クリーンアーキテクチャ**: ドメイン駆動設計による階層分離
- **依存性注入**: リポジトリパターンとDI
- **ユースケース駆動開発**: ビジネスロジックの分離
- **モダンフロントエンド**: Next.js App Router、React Hooks、状態管理
- **TypeScript**: 型安全性とスケーラビリティ
- **テスト駆動開発**: pytest を使った単体テスト
- **Dev Container**: 再現可能な開発環境の構築

## プロジェクトドキュメント

| ドキュメント | 説明 | パス |
|------------|------|------|
| 要件定義 | Kiroによる機能要件と非機能要件 | `.kiro/specs/stock-portfolio-manager/requirements.md` |
| システム設計 | アーキテクチャとコンポーネント設計 | `.kiro/specs/stock-portfolio-manager/design.md` |
| 技術スタック | 使用技術の選定理由 | `.kiro/specs/stock-portfolio-manager/tech-stack.md` |
| タスク管理 | 実装タスクの詳細 | `.kiro/specs/stock-portfolio-manager/tasks.md` |
| Claude設定 | Claude Code用ガイダンス | `CLAUDE.md` |
| 開発環境設定 | Dev Container設定 | `.devcontainer/devcontainer.json` |

## 開発に参加する

1. リポジトリをクローン
2. Docker Desktopを起動
3. VSCodeでDev Containerを開く
4. 自動セットアップ完了後、開発開始

詳細は各ドキュメントを参照してください。