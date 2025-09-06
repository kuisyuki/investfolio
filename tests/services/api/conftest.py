import pytest
import sys
import os
from fastapi.testclient import TestClient

# services/apiディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../services/api'))

from main import app


@pytest.fixture
def client():
    """テスト用のFastAPIクライアントを提供"""
    return TestClient(app)


@pytest.fixture
def test_base_url():
    """テスト用のベースURL"""
    return "http://testserver"