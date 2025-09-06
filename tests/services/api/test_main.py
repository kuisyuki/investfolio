import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "InvestFolio API is running"
    assert data["version"] == "1.0.0"


def test_root_endpoint_structure(client: TestClient):
    """ルートエンドポイントのレスポンス構造を検証"""
    response = client.get("/")
    
    assert response.status_code == 200
    
    data = response.json()
    expected_keys = {"message", "version"}
    actual_keys = set(data.keys())
    
    assert actual_keys == expected_keys, f"Expected keys {expected_keys}, but got {actual_keys}"


def test_docs_endpoint_accessible(client: TestClient):
    """Swagger UIドキュメントエンドポイントがアクセス可能であることを確認"""
    response = client.get("/docs")
    
    # Swagger UIはHTMLを返すので200を確認
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_openapi_json_accessible(client: TestClient):
    """OpenAPI JSONスキーマがアクセス可能であることを確認"""
    response = client.get("/openapi.json")
    
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    
    data = response.json()
    # OpenAPIスキーマの基本構造を確認
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "InvestFolio API"
    assert data["info"]["version"] == "1.0.0"


def test_nonexistent_endpoint(client: TestClient):
    """存在しないエンドポイントへのアクセスで404が返されることを確認"""
    response = client.get("/nonexistent")
    
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not Found"


def test_cors_headers_present(client: TestClient):
    """CORSヘッダーが適切に設定されていることを確認"""
    # プリフライトリクエストをシミュレート
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    
    # CORSヘッダーの存在を確認
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers