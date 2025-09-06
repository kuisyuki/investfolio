# Docker Services Configuration

InvestFolioプロジェクトで使用するDockerサービスの設定ファイル群です。

## ディレクトリ構成

```
docker/
├── README.md
├── mysql/
│   ├── init/           # 初期化スクリプト
│   └── logs/           # MySQLログ
├── elasticsearch/
│   └── logs/           # Elasticsearchログ
├── kibana/
│   └── logs/           # Kibanaログ
├── filebeat/
│   ├── filebeat.yml    # Filebeat設定
│   └── logs/           # Filebeatログ
├── redis/
│   └── logs/           # Redisログ
└── nginx/
    ├── nginx.conf      # Nginx設定
    ├── conf.d/         # サイト別設定
    └── logs/           # Nginxログ
```

## ログの確認方法

### 各サービスのログ

```bash
# MySQL
tail -f docker/mysql/logs/error.log

# Elasticsearch
tail -f docker/elasticsearch/logs/*.log

# Kibana
tail -f docker/kibana/logs/kibana.log

# Filebeat
tail -f docker/filebeat/logs/filebeat.log

# Redis
tail -f docker/redis/logs/redis.log

# Nginx
tail -f docker/nginx/logs/access.log
tail -f docker/nginx/logs/error.log
```

### 全ログの一括確認

```bash
# 全サービスのログディレクトリを確認
find docker/ -name "logs" -type d

# 各ログディレクトリの内容確認
for dir in docker/*/logs; do
    echo "=== $dir ==="
    ls -la "$dir"
    echo
done
```

## 設定ファイル

- `docker-compose.yml`: 各サービスでログディレクトリをバインドマウント
- 各サービス固有の設定は対応するディレクトリに配置

## 注意事項

- ログファイルは永続化されるため、定期的なログローテーションを検討
- 本番環境では機密情報がログに含まれないよう注意
- ディスク容量の監視が必要