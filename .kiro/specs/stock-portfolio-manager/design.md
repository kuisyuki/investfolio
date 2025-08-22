# 設計書

## 概要

株式資産管理Webサービスは、個人投資家が保有株式と配当を効率的に管理できるシステムです。マイクロサービスアーキテクチャを採用し、フロントエンド（Next.js）、バックエンド（FastAPI）、データベース（MySQL）、監視システム（ELK Stack）で構成されます。

## アーキテクチャ

### システム構成図

```mermaid
graph TB
    subgraph "開発環境"
        subgraph "DevContainer (Ubuntu)"
            FE[Next.js Frontend<br/>TypeScript + pnpm]
            BE[FastAPI Backend<br/>Python + uvicorn]
            GEMINI[GEMINI CLI]
            MCP[MCP + Serena]
        end
        
        subgraph "Docker Compose Services"
            DB[(MySQL Database)]
            NGINX[Nginx<br/>Reverse Proxy]
            ES[(Elasticsearch)]
            KB[Kibana]
            FB[Filebeat]
        end
    end
    
    subgraph "外部サービス"
        STOCK_API[株価API<br/>yfinance/Alpha Vantage]
        NGROK[Ngrok<br/>一時公開]
    end
    
    FE --> NGINX
    NGINX --> BE
    BE --> DB
    BE --> STOCK_API
    BE --> ES
    FB --> ES
    ES --> KB
    NGINX --> NGROK
    
    style FE fill:#e1f5fe
    style BE fill:#f3e5f5
    style DB fill:#fff3e0
    style ES fill:#e8f5e8
```

### 技術スタック

**フロントエンド:**
- TypeScript + Next.js (App Router)
- TailwindCSS (スタイリング)
- React Hook Form (フォーム管理)
- Chart.js/Recharts (グラフ表示)
- pnpm (パッケージ管理)
- Volta (Node.jsバージョン管理)

**バックエンド:**
- Python + FastAPI
- uvicorn (ASGIサーバー)
- SQLAlchemy 2.0+ (ORM)
- sql-migrate (Go製マイグレーションツール)
- Pydantic v2 (データバリデーション)
- yfinance (株価取得)
- APScheduler (定期実行)

**インフラ:**
- MySQL (メインDB)
- Nginx (リバースプロキシ)
- Elasticsearch (ログ保存)
- Kibana (可視化)
- Filebeat (ログ収集)

## コンポーネントと インターフェース

### フロントエンド コンポーネント

```mermaid
graph TD
    APP[App Layout]
    
    subgraph "Pages"
        DASH[Dashboard]
        PORT[Portfolio]
        DIV[Dividends]
        ANAL[Analytics]
    end
    
    subgraph "Components"
        STOCK_FORM[StockForm]
        STOCK_LIST[StockList]
        DIV_FORM[DividendForm]
        DIV_LIST[DividendList]
        CHART[Charts]
        PRICE_UPDATE[PriceUpdateButton]
    end
    
    subgraph "Services"
        API_CLIENT[API Client]
        STOCK_SERVICE[Stock Service]
        DIV_SERVICE[Dividend Service]
    end
    
    APP --> DASH
    APP --> PORT
    APP --> DIV
    APP --> ANAL
    
    PORT --> STOCK_FORM
    PORT --> STOCK_LIST
    PORT --> PRICE_UPDATE
    
    DIV --> DIV_FORM
    DIV --> DIV_LIST
    
    ANAL --> CHART
    
    STOCK_FORM --> API_CLIENT
    STOCK_LIST --> API_CLIENT
    DIV_FORM --> API_CLIENT
    DIV_LIST --> API_CLIENT
    CHART --> API_CLIENT
    PRICE_UPDATE --> API_CLIENT
    
    API_CLIENT --> STOCK_SERVICE
    API_CLIENT --> DIV_SERVICE
```

### バックエンド コンポーネント

```mermaid
graph TD
    subgraph "API Layer"
        STOCK_API[Stock API Router]
        DIV_API[Dividend API Router]
        PRICE_API[Price API Router]
        AUTH_API[Auth API Router]
    end
    
    subgraph "Service Layer"
        STOCK_SVC[Stock Service]
        DIV_SVC[Dividend Service]
        PRICE_SVC[Price Service]
        AUTH_SVC[Auth Service]
    end
    
    subgraph "Repository Layer"
        STOCK_REPO[Stock Repository]
        DIV_REPO[Dividend Repository]
        PRICE_REPO[Price Repository]
        USER_REPO[User Repository]
    end
    
    subgraph "External"
        YFINANCE[yfinance API]
        SCHEDULER[APScheduler]
    end
    
    subgraph "Database"
        MYSQL[(MySQL)]
    end
    
    STOCK_API --> STOCK_SVC
    DIV_API --> DIV_SVC
    PRICE_API --> PRICE_SVC
    AUTH_API --> AUTH_SVC
    
    STOCK_SVC --> STOCK_REPO
    DIV_SVC --> DIV_REPO
    PRICE_SVC --> PRICE_REPO
    AUTH_SVC --> USER_REPO
    
    STOCK_REPO --> MYSQL
    DIV_REPO --> MYSQL
    PRICE_REPO --> MYSQL
    USER_REPO --> MYSQL
    
    PRICE_SVC --> YFINANCE
    SCHEDULER --> PRICE_SVC
```

### API エンドポイント設計

**株式管理 API:**
```
GET    /api/stocks          - 保有株式一覧取得
POST   /api/stocks          - 新規株式追加
PUT    /api/stocks/{id}     - 株式情報更新
DELETE /api/stocks/{id}     - 株式削除
POST   /api/stocks/prices   - 株価一括更新
```

**配当管理 API:**
```
GET    /api/dividends       - 配当履歴取得
POST   /api/dividends       - 配当記録追加
PUT    /api/dividends/{id}  - 配当記録更新
DELETE /api/dividends/{id}  - 配当記録削除
GET    /api/dividends/stats - 配当統計取得
```

**分析 API:**
```
GET    /api/analytics/portfolio    - ポートフォリオ分析
GET    /api/analytics/performance  - パフォーマンス分析
GET    /api/analytics/dividends    - 配当分析
```

## データモデル

### データベース設計

```mermaid
erDiagram
    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
    }
    
    STOCKS {
        int id PK
        int user_id FK
        string symbol UK "銘柄コード"
        string name "銘柄名"
        int shares "保有株数"
        decimal purchase_price "取得価格"
        decimal current_price "現在価格"
        datetime purchase_date "取得日"
        datetime price_updated_at "価格更新日時"
        datetime created_at
        datetime updated_at
    }
    
    DIVIDENDS {
        int id PK
        int stock_id FK
        decimal amount "配当金額"
        date dividend_date "配当受取日"
        string dividend_type "配当種別"
        datetime created_at
        datetime updated_at
    }
    
    PRICE_HISTORY {
        int id PK
        string symbol FK
        decimal price "株価"
        date price_date "価格日付"
        datetime created_at
    }
    
    USERS ||--o{ STOCKS : "owns"
    STOCKS ||--o{ DIVIDENDS : "receives"
    STOCKS ||--o{ PRICE_HISTORY : "has_history"
```

### データモデル定義

**Stock Model:**
```python
class Stock(BaseModel):
    id: int
    user_id: int
    symbol: str  # 銘柄コード (例: "7203.T")
    name: str    # 銘柄名 (例: "トヨタ自動車")
    shares: int  # 保有株数
    purchase_price: Decimal  # 取得価格
    current_price: Optional[Decimal]  # 現在価格
    purchase_date: date
    price_updated_at: Optional[datetime]
    
    @property
    def market_value(self) -> Decimal:
        return self.current_price * self.shares if self.current_price else Decimal(0)
    
    @property
    def unrealized_gain_loss(self) -> Decimal:
        return self.market_value - (self.purchase_price * self.shares)
```

**Dividend Model:**
```python
class Dividend(BaseModel):
    id: int
    stock_id: int
    amount: Decimal  # 配当金額
    dividend_date: date  # 配当受取日
    dividend_type: str  # "regular", "special", "interim"
```

## エラーハンドリング

### エラー分類と対応

**1. バリデーションエラー (400 Bad Request)**
```python
class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
```

**2. 認証エラー (401 Unauthorized)**
```python
class AuthenticationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="認証が必要です")
```

**3. 外部API エラー (503 Service Unavailable)**
```python
class ExternalAPIError(HTTPException):
    def __init__(self, service: str):
        super().__init__(
            status_code=503, 
            detail=f"{service}サービスが利用できません"
        )
```

**4. データベースエラー (500 Internal Server Error)**
```python
class DatabaseError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=500, 
            detail="データベースエラーが発生しました"
        )
```

### エラーログ設計

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def log_error(error: Exception, context: dict = None):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {}
    }
    logger.error(json.dumps(log_data))
```

## テスト戦略

### テストピラミッド

```mermaid
graph TD
    subgraph "テストピラミッド"
        E2E[E2E Tests<br/>Playwright]
        INT[Integration Tests<br/>TestClient + TestDB]
        UNIT[Unit Tests<br/>pytest + Mock]
    end
    
    E2E --> INT
    INT --> UNIT
    
    style E2E fill:#ffcdd2
    style INT fill:#fff3e0
    style UNIT fill:#e8f5e8
```

### テスト分類

**1. ユニットテスト (pytest)**
- Service層のビジネスロジック
- Repository層のデータアクセス
- Utility関数
- バリデーション機能

**2. 統合テスト (FastAPI TestClient)**
- API エンドポイント
- データベース連携
- 外部API連携（モック使用）

**3. E2Eテスト (Playwright)**
- ユーザーシナリオ
- フロントエンド・バックエンド連携
- 主要機能の動作確認

### テスト環境設定

```python
# conftest.py
@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///test.db")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def mock_stock_api():
    with patch('services.stock_service.yfinance') as mock:
        mock.download.return_value = pd.DataFrame({
            'Close': [1000.0]
        })
        yield mock
```

## セキュリティ設計

### 認証・認可

**JWT トークン認証:**
```python
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### データ保護

**1. パスワードハッシュ化:**
```python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**2. SQLインジェクション対策:**
- SQLAlchemy ORM使用
- パラメータ化クエリ
- 入力値バリデーション

**3. CORS設定:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 監視・ログ設計

### ログ収集フロー

```mermaid
graph LR
    APP[Application Logs] --> FB[Filebeat]
    NGINX[Nginx Logs] --> FB
    MYSQL[MySQL Logs] --> FB
    FB --> ES[Elasticsearch]
    ES --> KB[Kibana]
    
    style APP fill:#e1f5fe
    style FB fill:#fff3e0
    style ES fill:#e8f5e8
    style KB fill:#f3e5f5
```

### ログ形式

**アプリケーションログ:**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "logger": "stock_service",
  "message": "株価更新完了",
  "user_id": 123,
  "symbol": "7203.T",
  "duration_ms": 150
}
```

**アクセスログ:**
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "method": "GET",
  "path": "/api/stocks",
  "status_code": 200,
  "response_time_ms": 45,
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.100"
}
```

### Kibana ダッシュボード設計

**1. システム監視ダッシュボード:**
- API レスポンス時間
- エラー率
- リクエスト数推移
- システムリソース使用率

**2. ビジネス監視ダッシュボード:**
- ユーザー活動状況
- 株価更新頻度
- 機能利用状況
- 資産推移データ

## 開発環境設計

### DevContainer 設定

**Dockerfile:**
```dockerfile
FROM ubuntu:22.04

# 基本パッケージインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nodejs \
    npm \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Volta インストール
RUN curl https://get.volta.sh | bash

# GEMINI CLI インストール
RUN pip install google-generativeai

# 開発ツール設定
COPY requirements.txt .
RUN pip install -r requirements.txt
```

**devcontainer.json:**
```json
{
  "name": "Stock Portfolio Manager",
  "dockerFile": "Dockerfile",
  "postCreateCommand": "./scripts/PostCreateCommand.sh",
  "postStartCommand": "./scripts/PostStartCommand.sh",
  "forwardPorts": [3000, 8000, 5601, 9200],
  "extensions": [
    "ms-python.python",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

### Docker Compose 設定

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: portfolio_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:latest
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:latest
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:latest
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml
      - /var/log:/var/log:ro
    depends_on:
      - elasticsearch

volumes:
  mysql_data:
  es_data:
```

## デプロイメント設計

### Ngrok 設定

```bash
# Ngrok インストールと設定
ngrok config add-authtoken YOUR_AUTH_TOKEN
ngrok http 80 --domain=your-domain.ngrok.io
```

### 環境変数管理

```python
# .env
DATABASE_URL=mysql://user:password@localhost:3306/portfolio_db
SECRET_KEY=your-secret-key
ELASTICSEARCH_URL=http://localhost:9200
STOCK_API_BASE_URL=https://query1.finance.yahoo.com
NGROK_DOMAIN=your-domain.ngrok.io
```

この設計書は、要件定義書で定義された全ての機能要件と非機能要件を満たすシステムアーキテクチャを提供しています。