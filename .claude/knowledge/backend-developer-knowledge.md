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
- 2025-09-30: User Stock APIエンドポイント実装を追加
- 2025-09-30: UserResponse Validation Errorの解決方法を追加

---

## 2025-09-30 - User Stock API実装

### Context
InvestFolioプロジェクトで持ち株管理機能の実装

### Problem
- ユーザーの持ち株を登録・取得するAPIが必要
- フロントエンドとバックエンドの統合

### Solution

#### 1. バックエンドAPI実装

**リポジトリインターフェース拡張** (`domain/repositories/user_stock_repository.py`):
```python
from typing import List

@abstractmethod
async def get_by_user_id(self, user_id: str) -> List[UserStock]:
    """ユーザーIDで保有株リストを取得する"""
    raise NotImplementedError
```

**リポジトリ実装** (`infrastructure/repositories/user_stock_repository_impl.py`):
```python
async def get_by_user_id(self, user_id: str) -> List[UserStock]:
    """ユーザーIDで保有株リストを取得"""
    user_stocks = self.db.query(UserStockModel).filter(
        UserStockModel.user_id == user_id
    ).order_by(UserStockModel.created_at.desc()).all()

    return [self._model_to_entity(stock) for stock in user_stocks]
```

**APIエンドポイント追加** (`presentation/routes/user_stock.py`):
```python
from typing import List

@router.get("/", response_model=List[UserStockResponse])
async def get_user_stocks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    ログインユーザーの保有株一覧を取得する
    """
    try:
        repository = SQLUserStockRepository(db)
        user_stocks = await repository.get_by_user_id(str(current_user.id))
        return user_stocks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保有株リストの取得に失敗しました: {str(e)}",
        )
```

#### 2. フロントエンド実装

**API クライアント** (`app/utils/api.ts`):
```typescript
export interface UserStock {
  id: string
  user_id: string
  ticker_symbol: string
  quantity: number
  acquisition_price: number
  created_at: string
  updated_at: string
}

export const userStocksAPI = {
  getAll: async (): Promise<UserStock[]> => {
    return apiCall<UserStock[]>('/api/user-stocks/', {
      method: 'GET',
      requireAuth: true,
    })
  },

  create: async (data: CreateUserStockRequest): Promise<UserStock> => {
    return apiCall<UserStock>('/api/user-stocks/', {
      method: 'POST',
      body: JSON.stringify(data),
      requireAuth: true,
    })
  },
}
```

### Prevention
- APIエンドポイント作成時は必ずGETとPOSTの両方を考慮
- リポジトリパターンを使用して実装の詳細を隠蔽
- フロントエンドでは適切なエラーハンドリングとローディング状態の管理

### Related Knowledge
- Clean Architecture構造での実装パターン
- FastAPI実装パターン

---

## 2025-09-30 - Database ID Column Migration from String to Integer

### Context
InvestFolioプロジェクトでデータベーススキーマ変更に伴うバックエンドコードの修正

### Problem
usersテーブルとuser_stocksテーブルのIDカラムがString(UUID)からINT AUTO_INCREMENTに変更され、以下のエラーが発生:
```
(pymysql.err.DataError) (1265, "Data truncated for column 'id' at row 1")
```

### Root Cause
- コードがUUID(文字列)を生成しているが、データベースはINT型を期待
- 全体的にID型の不一致が発生

### Solution

#### 1. SQLAlchemyモデルの修正
**infrastructure/models/user.py**:
```python
from sqlalchemy import Boolean, Column, DateTime, Integer, String
# ...
class UserModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)  # String(36)から変更
```

**infrastructure/models/user_stock.py**:
```python
class UserStockModel(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)  # String(36)から変更
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # String(36)から変更
```

#### 2. ドメインエンティティの修正
**domain/entities/auth.py**:
```python
@dataclass
class User:
    id: Optional[int]  # strからOptional[int]に変更
```

**domain/entities/user_stock.py**:
```python
@dataclass
class UserStock:
    id: Optional[int]  # 重複フィールドを削除し、Optional[int]に変更
    user_id: int  # strからintに変更
```

#### 3. リポジトリの修正
**infrastructure/repositories/user_repository.py**:
```python
# uuidのimportを削除
async def create(self, user: User) -> User:
    user_model = UserModel(
        # id=str(uuid.uuid4())を削除 - AUTO_INCREMENTに任せる
        username=user.username,
        # ...
    )

async def get_by_id(self, user_id: int) -> Optional[User]:  # 引数の型をstrからintに変更
```

#### 4. プレゼンテーション層の修正
**presentation/schemas/auth.py**:
```python
class UserResponse(BaseModel):
    id: int  # strからintに変更
```

**presentation/routes/user_stock.py**:
```python
class UserStockResponse(BaseModel):
    id: int  # strからintに変更
    user_id: int  # strからintに変更
```

#### 5. JWT関連の修正
**presentation/routes/auth.py**:
```python
# JWTトークン生成時にIDを文字列化
access_token = create_access_token(data={"sub": str(user.id)})
```

**presentation/dependencies/auth.py**:
```python
# トークンからユーザーIDを取得してintに変換
user = await user_repository.get_by_id(int(user_id))
```

### Prevention
1. **データベーススキーマ変更時のチェックリスト**:
   - 全てのSQLAlchemyモデルを確認
   - 全てのドメインエンティティを確認
   - 全てのリポジトリインターフェース・実装を確認
   - 全てのスキーマ(Pydantic)を確認
   - JWT等の文字列化処理を確認

2. **型の一貫性**:
   - IDフィールドは全層で同じ型を使用
   - Optional[int]を使用して新規作成時のNone値を許可
   - JWT等で文字列化が必要な場合は明示的にstr()を使用

3. **AUTO_INCREMENT使用時の注意点**:
   - リポジトリでID生成コードを削除
   - エンティティ作成時はid=Noneを設定
   - DBのrefresh後に生成されたIDが取得可能

### Related Knowledge
- MySQLdb Module Not Found Error
- SQLAlchemy Tips
- Clean Architecture構造での実装パターン

---

## 2025-09-30 - UserResponse Validation Error修正

### Context
InvestFolioプロジェクトでアカウント作成API実行時にPydanticバリデーションエラーが発生

### Problem
`RegisterUserUseCase`でUserエンティティを作成する際、`user_id`フィールドが欠けているため、`UserResponse`のバリデーションエラーが発生:
```
1 validation error for UserResponse
user_id
  Field required [type=missing, input_value={'id': 2, 'username': 'te...}, input_type=dict]
```

### Root Cause
1. `UserResponse`スキーマは`user_id`フィールドを必須として定義
2. `RegisterUserUseCase`でUserエンティティを作成時に`user_id=None`が設定されていなかった
3. APIルートで`UserResponse`を作成する際、`user_id`フィールドが含まれていなかった

### Solution

#### 1. RegisterUserUseCaseの修正
**application/use_cases/register_user.py**:
```python
# ユーザーエンティティを作成
user = User(
    id=None,  # データベースで自動生成される
    user_id=None,  # リポジトリ層でidと同じ値を設定
    username=username,
    email=email,
    password_hash=password_hash,
    full_name=full_name,
    is_active=True,
    is_verified=False,
)
```

#### 2. APIルートでのUserResponse作成修正
**presentation/routes/auth.py**:
```python
# /register エンドポイント
return UserResponse(
    id=user.id,
    user_id=user.user_id,  # 追加
    username=user.username,
    email=user.email,
    full_name=user.full_name,
    is_active=user.is_active,
    is_verified=user.is_verified,
    created_at=user.created_at,
    updated_at=user.updated_at,
)

# /login エンドポイントのuser部分
user=UserResponse(
    id=user.id,
    user_id=user.user_id,  # 追加
    username=user.username,
    # ...
)

# /me エンドポイント
return UserResponse(
    id=current_user.id,
    user_id=current_user.user_id,  # 追加
    username=current_user.username,
    # ...
)
```

### Prevention
1. **Pydanticスキーマの完全性確認**:
   - レスポンススキーマで定義された全フィールドが含まれているか確認
   - 特にIDフィールドが複数ある場合は要注意

2. **エンティティ作成時のチェック**:
   - データクラスの全フィールドに値を設定
   - Optional型でもNoneを明示的に設定

3. **APIレスポンス作成時の注意点**:
   - スキーマで定義された全フィールドを含める
   - 自動変換に頼らず明示的にフィールドを指定

### Related Knowledge
- Database ID Column Migration from String to Integer
- Clean Architecture構造での実装パターン