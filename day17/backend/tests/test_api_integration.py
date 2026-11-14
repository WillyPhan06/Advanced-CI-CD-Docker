import uuid

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)

    # Create the database table if it does not exist.
    app_module.initialize_database()

    return app_module.app.test_client()


def test_health_endpoint_checks_database(client):
    response = client.get("/health")

    assert response.status_code == 200

    assert response.get_json() == {
        "status": "healthy",
        "database": "reachable",
    }


def test_task_is_persisted_and_retrievable(client):
    title = f"CI integration test {uuid.uuid4().hex}"

    try:
        create_response = client.post(
            "/tasks",
            json={"title": title},
        )

        assert create_response.status_code == 201

        created_task = create_response.get_json()

        assert created_task["title"] == title
        assert created_task["id"] is not None

        list_response = client.get("/tasks")

        assert list_response.status_code == 200

        tasks = list_response.get_json()

        assert any(
            task["title"] == title
            for task in tasks
        )

    finally:
        # Remove the test record so repeated local runs stay clean.
        with app_module.get_connection() as conn:
            conn.execute(
                "DELETE FROM tasks WHERE title = %s",
                (title,),
            )