from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path: Path):
    app = create_app(tmp_path / "test.db")
    with TestClient(app) as test_client:
        yield test_client


def test_health_and_empty_list(client: TestClient):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/tasks").json() == []


def test_task_crud(client: TestClient):
    created = client.post("/api/tasks", json={"text": "  買牛奶  "})
    assert created.status_code == 201
    task = created.json()
    assert task == {"id": 1, "text": "買牛奶", "done": False}

    assert client.get("/api/tasks/1").json() == task
    assert client.get("/api/tasks").json() == [task]

    replaced = client.put(
        "/api/tasks/1",
        json={"text": "完整替換任務", "done": True},
    )
    assert replaced.status_code == 200
    assert replaced.json() == {
        "id": 1,
        "text": "完整替換任務",
        "done": True,
    }

    updated_done = client.patch("/api/tasks/1", json={"done": False})
    assert updated_done.status_code == 200
    assert updated_done.json() == {
        "id": 1,
        "text": "完整替換任務",
        "done": False,
    }

    updated_text = client.patch("/api/tasks/1", json={"text": "買鮮奶"})
    assert updated_text.status_code == 200
    assert updated_text.json() == {"id": 1, "text": "買鮮奶", "done": False}

    deleted = client.delete("/api/tasks/1")
    assert deleted.status_code == 204
    assert client.get("/api/tasks").json() == []


@pytest.mark.parametrize(
    "payload",
    [
        {"text": ""},
        {"text": "   "},
        {"text": "x" * 201},
        {"text": 123},
    ],
)
def test_create_rejects_invalid_text(client: TestClient, payload: dict):
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 422


def test_patch_rejects_empty_or_invalid_payload(client: TestClient):
    client.post("/api/tasks", json={"text": "任務"})

    assert client.patch("/api/tasks/1", json={}).status_code == 422
    assert client.patch("/api/tasks/1", json={"text": "   "}).status_code == 422
    assert client.patch("/api/tasks/1", json={"done": None}).status_code == 422
    assert client.patch("/api/tasks/1", json={"done": "yes"}).status_code == 422


def test_put_requires_complete_valid_payload(client: TestClient):
    client.post("/api/tasks", json={"text": "任務"})

    assert client.put("/api/tasks/1", json={"text": "新任務"}).status_code == 422
    assert client.put("/api/tasks/1", json={"done": True}).status_code == 422
    assert client.put(
        "/api/tasks/1",
        json={"text": "   ", "done": True},
    ).status_code == 422
    assert client.put(
        "/api/tasks/1",
        json={"text": "新任務", "done": "yes"},
    ).status_code == 422


def test_put_is_idempotent(client: TestClient):
    client.post("/api/tasks", json={"text": "可重複更新"})
    payload = {"text": "可重複更新", "done": True}

    first = client.put("/api/tasks/1", json=payload)
    second = client.put("/api/tasks/1", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json() == first.json()


def test_missing_tasks_return_not_found(client: TestClient):
    assert client.get("/api/tasks/999").status_code == 404
    assert client.put(
        "/api/tasks/999",
        json={"text": "不存在", "done": False},
    ).status_code == 404
    assert client.patch("/api/tasks/999", json={"done": True}).status_code == 404
    assert client.delete("/api/tasks/999").status_code == 404


def test_tasks_are_persisted_in_sqlite(client: TestClient, tmp_path: Path):
    database_path = tmp_path / "persistent.db"
    first_client = TestClient(create_app(database_path))
    with first_client:
        first_client.post("/api/tasks", json={"text": "持久化任務"})

    second_client = TestClient(create_app(database_path))
    with second_client:
        assert second_client.get("/api/tasks").json() == [
            {"id": 1, "text": "持久化任務", "done": False}
        ]


def test_cors_allows_frontend_origin(client: TestClient):
    response = client.options(
        "/api/tasks",
        headers={
            "Origin": "http://localhost:5500",
            "Access-Control-Request-Method": "PUT",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5500"
