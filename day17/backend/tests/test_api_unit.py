from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": ""},
        {"title": "   "},
        {"title": 123},
    ],
)
def test_create_task_rejects_invalid_title(client, payload):
    response = client.post("/tasks", json=payload)

    assert response.status_code == 400

    assert response.get_json() == {
        "error": "Task title is required"
    }


def test_create_task_returns_created_task(client, monkeypatch):
    fake_connection = MagicMock()

    fake_connection.__enter__.return_value = fake_connection

    fake_connection.execute.return_value.fetchone.return_value = (
        42,
        "Prepare CI tests",
        datetime(2026, 11, 13, tzinfo=timezone.utc),
    )

    monkeypatch.setattr(
        app_module,
        "get_connection",
        lambda: fake_connection,
    )

    response = client.post(
        "/tasks",
        json={"title": "Prepare CI tests"},
    )

    assert response.status_code == 201

    assert response.get_json()["id"] == 42
    assert response.get_json()["title"] == "Prepare CI tests"

    fake_connection.execute.assert_called_once()