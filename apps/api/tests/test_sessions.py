import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.config import settings
from app.main import app

client = TestClient(app)
sync_engine = create_engine(settings.database_url_sync, pool_pre_ping=True)


@pytest.fixture(autouse=True)
def clean_db():
    with sync_engine.begin() as conn:
        conn.execute(text("TRUNCATE interview_sessions CASCADE"))
    yield
    with sync_engine.begin() as conn:
        conn.execute(text("TRUNCATE interview_sessions CASCADE"))


def test_create_session_success():
    resp = client.post(
        "/api/sessions",
        json={"target_role": "Backend Engineer", "job_description": "Build APIs", "language": "id"},
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["status"] == "draft"
    assert data["target_role"] == "Backend Engineer"
    assert data["language"] == "id"
    assert data["current_question_index"] == 0
    assert "id" in data
    assert "created_at" in data


def test_create_session_validation_empty_role():
    resp = client.post("/api/sessions", json={"target_role": "", "job_description": "x", "language": "id"})
    assert resp.status_code == 422
    body = resp.json()
    assert body["error"]["code"] == "validation_error"


def test_create_session_validation_language():
    resp = client.post("/api/sessions", json={"target_role": "A", "job_description": "B", "language": "fr"})
    assert resp.status_code == 422


def test_get_session_not_found():
    resp = client.get(f"/api/sessions/{uuid.uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "not_found"


def test_get_session_success():
    created = client.post(
        "/api/sessions", json={"target_role": "FE", "job_description": "Build UI", "language": "en"}
    ).json()
    sid = created["id"]
    resp = client.get(f"/api/sessions/{sid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == sid
    assert data["status"] == "draft"


def test_list_sessions_pagination_and_order():
    for role in ["A", "B", "C"]:
        client.post("/api/sessions", json={"target_role": role, "job_description": "JD", "language": "id"})
    resp = client.get("/api/sessions?page=1&page_size=2")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2
    assert body["page"] == 1
    assert body["page_size"] == 2
    assert body["items"][0]["target_role"] == "C"


def test_list_sessions_filter_status():
    client.post("/api/sessions", json={"target_role": "X", "job_description": "JD", "language": "id"})
    resp = client.get("/api/sessions?status=draft")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
    resp2 = client.get("/api/sessions?status=ready")
    assert resp2.status_code == 200
    assert resp2.json()["total"] == 0


def test_delete_draft_success():
    created = client.post(
        "/api/sessions", json={"target_role": "Del", "job_description": "JD", "language": "id"}
    ).json()
    sid = created["id"]
    del_resp = client.delete(f"/api/sessions/{sid}")
    assert del_resp.status_code == 204
    get_resp = client.get(f"/api/sessions/{sid}")
    assert get_resp.status_code == 404


def test_delete_non_draft_rejected_409():
    created = client.post(
        "/api/sessions", json={"target_role": "NoDel", "job_description": "JD", "language": "id"}
    ).json()
    sid = created["id"]
    with sync_engine.begin() as conn:
        conn.execute(text("UPDATE interview_sessions SET status='ready' WHERE id=:id"), {"id": str(sid)})
    resp = client.delete(f"/api/sessions/{sid}")
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "conflict"


def test_delete_not_found():
    resp = client.delete(f"/api/sessions/{uuid.uuid4()}")
    assert resp.status_code == 404


def test_openapi_has_session_endpoints():
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    paths = resp.json()["paths"]
    assert "/api/sessions" in paths
    assert "/api/sessions/{session_id}" in paths


def test_status_transition_invalid_delete_after_ready():
    sid = client.post(
        "/api/sessions", json={"target_role": "T", "job_description": "JD", "language": "id"}
    ).json()["id"]
    with sync_engine.begin() as conn:
        conn.execute(
            text("UPDATE interview_sessions SET status='in_progress' WHERE id=:id"), {"id": str(sid)}
        )
    resp = client.delete(f"/api/sessions/{sid}")
    assert resp.status_code == 409
