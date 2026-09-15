from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200_with_expected_fields() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "ai-interviewer-api"
    assert "version" in data
    assert "timestamp" in data
