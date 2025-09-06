# Backend Developer Knowledge Base

## 概要
このドキュメントはbackend-developerエージェントが蓄積した実装ナレッジを記録します。
エラー解決、実装パターン、ベストプラクティスなどを体系的に管理します。

---

## データベース接続エラー

### MySQLdb Module Not Found Error
**発生日**: 2025-08-24  
**プロジェクト**: InvestFolio  
**エラー内容**:
```
ModuleNotFoundError: No module named 'MySQLdb'
```

**根本原因**:
- SQLAlchemyがMySQLに接続する際、デフォルトでMySQLdbドライバーを使用しようとする
- MySQLdb（MySQL-python）はPython 3.xでメンテナンスされていない
- 環境変数`DATABASE_URL`が`mysql://`で始まる場合、自動的にMySQLdbを探す

**解決方法**:
1. **pymysqlを使用する（推奨）**
   ```python
   # infrastructure/database.py
   import os
   from sqlalchemy import create_engine
   
   # DATABASE_URLを取得
   raw_database_url = os.getenv("DATABASE_URL", "default_url")
   
   # mysql://をmysql+pymysql://に変換
   if raw_database_url.startswith("mysql://"):
       DATABASE_URL = raw_database_url.replace("mysql://", "mysql+pymysql://", 1)
       # charsetが無い場合は追加
       if "charset=" not in DATABASE_URL:
           DATABASE_URL += "?charset=utf8mb4" if "?" not in DATABASE_URL else "&charset=utf8mb4"
   else:
       DATABASE_URL = raw_database_url
   ```

2. **requirements.txtに追加**
   ```
   pymysql==1.1.1
   cryptography==41.0.7  # MySQL認証に必要
   ```

**予防策**:
- 新規プロジェクトでは最初から`mysql+pymysql://`形式でDATABASE_URLを設定
- Docker環境変数の設定時に正しいドライバーを指定
- requirements.txtに必要なパッケージを事前に記載

**関連ファイル**:
- `/workspace/services/api/infrastructure/database.py`
- `/workspace/services/api/requirements.txt`
- `/workspace/.devcontainer/docker-compose.yml`

---

## FastAPI実装パターン

### Clean Architecture構造での実装
**適用プロジェクト**: InvestFolio

**ディレクトリ構造**:
```
services/api/
├── domain/           # ビジネスロジック層
│   ├── entities/     # ビジネスエンティティ
│   └── repositories/ # リポジトリインターフェース
├── application/      # アプリケーション層
│   └── use_cases/    # ユースケース
├── infrastructure/   # インフラ層
│   ├── database.py   # DB接続設定
│   ├── models/       # SQLAlchemyモデル
│   └── repositories/ # リポジトリ実装
└── presentation/     # プレゼンテーション層
    ├── routes/       # APIルート
    └── schemas/      # Pydanticスキーマ
```

**実装の順序**:
1. Domain Entityを定義
2. Repository Interfaceを定義
3. Pydantic Schemaを作成
4. Use Caseを実装
5. Repository実装を作成
6. Routeを実装

---

## Python依存関係管理

### 一般的な問題と解決策

**問題**: ImportError / ModuleNotFoundError
**チェックリスト**:
1. `requirements.txt`に記載されているか確認
2. `pip list`で実際にインストールされているか確認
3. 仮想環境が正しく有効化されているか確認
4. Dockerコンテナ内の場合、コンテナを再ビルドが必要か確認

**デバッグコマンド**:
```bash
# インストール済みパッケージ確認
pip list | grep package_name

# 特定のパッケージの詳細確認
pip show package_name

# requirements.txtから再インストール
pip install -r requirements.txt

# キャッシュをクリアして再インストール
pip install --no-cache-dir -r requirements.txt
```

---

## SQLAlchemy Tips

### セッション管理
**ベストプラクティス**:
```python
# セッションファクトリーの作成
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依存性注入での使用
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### マイグレーション
**sql-migrateの使用**:
- 必ず`sql-migrate new`コマンドでファイル生成
- MySQLとPostgreSQLで構文が異なることに注意
- updated_atカラムの自動更新はDBにより実装が異なる

---

## テスト実装

### pytest設定
**基本構成**:
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### モックとフィクスチャ
**データベーステストのパターン**:
```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def test_db():
    # テスト用DBセットアップ
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
```

---

## エラーハンドリング

### FastAPIでの例外処理
**カスタム例外ハンドラー**:
```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

---

## パフォーマンス最適化

### N+1問題の解決
**SQLAlchemyでの対策**:
```python
# joinedloadを使用
from sqlalchemy.orm import joinedload

users = db.query(User).options(joinedload(User.posts)).all()
```

---

## セキュリティ

### パスワードハッシュ化
**bcryptの使用**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

---

## 更新履歴
- 2025-08-24: MySQLdb Module Not Found Errorの解決方法を追加
- 2025-08-24: Clean Architecture構造での実装パターンを追加