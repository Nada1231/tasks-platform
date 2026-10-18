from fastapi.testclient import TestClient

from app.main import app


def test_create_and_list_tasks():
    # "with" déclenche le démarrage de l'app (création des tables)
    with TestClient(app) as client:
        created = client.post("/tasks", json={"title": "Apprendre Docker"})
        assert created.status_code == 201
        assert created.json()["title"] == "Apprendre Docker"
        assert created.json()["done"] is False

        listed = client.get("/tasks")
        assert listed.status_code == 200
        assert any(t["title"] == "Apprendre Docker" for t in listed.json())


def test_create_task_rejects_empty_title():
    with TestClient(app) as client:
        response = client.post("/tasks", json={"title": ""})
        assert response.status_code == 422
