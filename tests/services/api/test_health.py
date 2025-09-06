import pytest
from datetime import datetime
from fastapi.testclient import TestClient


def test_health_check_success(client: TestClient):
    """ヘルスチェックエンドポイントが正常に動作することをテスト"""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "investfolio-api"
    assert "timestamp" in data
    
    # タイムスタンプがISO形式であることを確認
    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        pytest.fail("Timestamp is not in ISO format")


def test_health_check_response_structure(client: TestClient):
    """ヘルスチェックレスポンスの構造を検証"""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    expected_keys = {"status", "timestamp", "service"}
    actual_keys = set(data.keys())
    
    assert actual_keys == expected_keys, f"Expected keys {expected_keys}, but got {actual_keys}"


def test_health_check_content_type(client: TestClient):
    """ヘルスチェックエンドポイントのContent-Typeを検証"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_health_check_method_not_allowed(client: TestClient):
    """許可されていないHTTPメソッドのテスト"""
    # POSTメソッドはサポートされていないはず
    response = client.post("/health")
    assert response.status_code == 405
    
    # PUTメソッドもサポートされていないはず
    response = client.put("/health")
    assert response.status_code == 405
    
    # DELETEメソッドもサポートされていないはず
    response = client.delete("/health")
    assert response.status_code == 405


def test_health_check_timestamp_format(client: TestClient):
    """タイムスタンプのフォーマットと妥当性を検証"""
    response = client.get("/health")
    
    assert response.status_code == 200
    
    data = response.json()
    timestamp_str = data["timestamp"]
    
    # ISO形式のタイムスタンプをパース
    timestamp = datetime.fromisoformat(timestamp_str)
    
    # タイムスタンプが現在時刻に近いことを確認（5秒以内）
    now = datetime.now()
    time_diff = abs((now - timestamp).total_seconds())
    
    assert time_diff < 5, f"Timestamp {timestamp} is too far from current time {now}"


def test_multiple_health_checks(client: TestClient):
    """複数回のヘルスチェックで異なるタイムスタンプが返されることを確認"""
    response1 = client.get("/health")
    response2 = client.get("/health")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    data1 = response1.json()
    data2 = response2.json()
    
    # ステータスとサービス名は同じであるべき
    assert data1["status"] == data2["status"]
    assert data1["service"] == data2["service"]
    
    # タイムスタンプは異なるはず（同じマイクロ秒に実行される可能性は低い）
    # ただし、非常に高速な環境では同じになる可能性もあるため、この検証は警告のみ
    if data1["timestamp"] == data2["timestamp"]:
        import warnings
        warnings.warn("Two health checks returned the same timestamp - this might happen in very fast environments")