"""ヘルスチェックルートの詳細テスト"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from fastapi.testclient import TestClient


class TestHealthRoute:
    """ヘルスチェックルートのテストクラス"""

    def test_health_endpoint_path(self, client: TestClient):
        """ヘルスチェックエンドポイントのパスが正しいことを確認"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_schema(self, client: TestClient):
        """ヘルスチェックレスポンスのスキーマ検証"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        
        # 必須フィールドの存在確認
        required_fields = ["status", "timestamp", "service"]
        for field in required_fields:
            assert field in data, f"Required field '{field}' missing from response"
        
        # フィールドの型確認
        assert isinstance(data["status"], str), "status should be string"
        assert isinstance(data["timestamp"], str), "timestamp should be string"
        assert isinstance(data["service"], str), "service should be string"

    def test_health_status_value(self, client: TestClient):
        """ヘルスチェックのステータス値が正しいことを確認"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_service_name(self, client: TestClient):
        """サービス名が正しいことを確認"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "investfolio-api"

    def test_health_timestamp_recent(self, client: TestClient):
        """タイムスタンプが現在時刻に近いことを確認"""
        before_request = datetime.now()
        response = client.get("/health")
        after_request = datetime.now()
        
        assert response.status_code == 200
        
        data = response.json()
        response_timestamp = datetime.fromisoformat(data["timestamp"])
        
        # レスポンスのタイムスタンプがリクエスト前後の時刻内にあることを確認
        assert before_request <= response_timestamp <= after_request

    @patch('presentation.routes.health.datetime')
    def test_health_timestamp_mocked(self, mock_datetime, client: TestClient):
        """モックを使用したタイムスタンプテスト"""
        # 固定の日時を設定
        fixed_datetime = datetime(2023, 12, 25, 10, 30, 45, 123456)
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["timestamp"] == fixed_datetime.isoformat()

    def test_health_concurrent_requests(self, client: TestClient):
        """並行リクエストのテスト"""
        import concurrent.futures
        import time
        
        def make_request():
            return client.get("/health")
        
        # 複数のリクエストを並行実行
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [future.result() for future in futures]
        
        # すべてのレスポンスが成功していることを確認
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["service"] == "investfolio-api"

    def test_health_load_test(self, client: TestClient):
        """負荷テスト（簡易版）"""
        # 連続で100回リクエスト
        for i in range(100):
            response = client.get("/health")
            assert response.status_code == 200
            
            # 10回ごとにデータの整合性を確認
            if i % 10 == 0:
                data = response.json()
                assert data["status"] == "healthy"
                assert data["service"] == "investfolio-api"

    def test_health_with_query_parameters(self, client: TestClient):
        """クエリパラメータ付きリクエストのテスト"""
        # ヘルスチェックはクエリパラメータを無視するべき
        response = client.get("/health?param=value&another=test")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "investfolio-api"

    def test_health_response_time(self, client: TestClient):
        """レスポンス時間のテスト"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        # ヘルスチェックは1秒以内に完了するべき
        assert response_time < 1.0, f"Health check took {response_time:.3f} seconds, should be under 1 second"