# Tests

InvestFolioプロジェクト全体のテストコードをここに配置します。

## 構造

```
tests/
├── README.md
├── services/
│   ├── api/                    # APIサービスのテスト
│   │   ├── conftest.py        # API共通テスト設定
│   │   ├── test_health.py     # ヘルスチェックテスト
│   │   ├── test_main.py       # メインアプリテスト
│   │   └── test_routes/       # ルート別テスト
│   └── web/                   # Webサービスのテスト（今後追加予定）
└── integration/               # 統合テスト（今後追加予定）
```

## テスト実行

### APIテスト
```bash
cd services/api
pytest
```

### 全テスト実行（今後）
```bash
cd /workspace
pytest tests/
```

## 各サービスのテスト詳細

- **API**: `services/api/README.md`を参照
- **Web**: 今後追加予定

## テスト方針

1. **単体テスト**: 各サービス内でそれぞれ実装
2. **統合テスト**: `tests/integration/`で実装
3. **E2Eテスト**: 今後検討