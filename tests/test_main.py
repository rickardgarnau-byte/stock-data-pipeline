from fastapi.testclient import TestClient
from src.main import app, get_conn


from unittest.mock import MagicMock

def override_get_conn():
    fake_conn = MagicMock()
    fake_conn.execute.return_value.fetchall.return_value = [{"ticker": "AAPL"}]
    yield fake_conn

app.dependency_overrides[get_conn] = override_get_conn

client = TestClient(app)

def test_get_stocks():
    response = client.get("/stocks")
    assert response.status_code == 200
    assert response.json() == [{"ticker": "AAPL"}]
