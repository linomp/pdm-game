import pytest
from fastapi.testclient import TestClient

from mvp.server.api import app
from mvp.server.core.constants import INITIAL_CASH, MAINTENANCE_COST

client = TestClient(app)


@pytest.fixture
def session_id():
    response = client.post("/sessions")
    return response.json()["id"]


def test_get_game_parameters():
    response = client.get("/game-parameters")
    assert response.status_code == 200
    assert "initial_cash" in response.json()
    assert "revenue_per_day" in response.json()
    assert "maintenance_cost" in response.json()
    assert "sensor_cost" in response.json()
    assert "game_tick_interval" in response.json()


def test_create_session():
    response = client.post("/sessions")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "current_step" in response.json()


def test_get_session(session_id):
    response = client.get(f"/sessions?session_id={session_id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "current_step" in response.json()


def test_get_session_not_found():
    response = client.get("/sessions?session_id=nonexistent_id")
    assert response.status_code == 404
    assert "message" in response.json()


def test_advance(session_id):
    response = client.put(f"/sessions/turns?session_id={session_id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "current_step" in response.json()


def test_advance_not_found():
    response = client.put("/sessions/turns?session_id=nonexistent_id")
    assert response.status_code == 404
    assert "message" in response.json()


def test_do_maintenance(session_id):
    available_funds = INITIAL_CASH
    while available_funds < MAINTENANCE_COST:
        response = client.put(f"/sessions/turns?session_id={session_id}")
        available_funds = response.json()["available_funds"]

    response = client.post(f"/player-actions/maintenance-interventions?session_id={session_id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "current_step" in response.json()


def test_do_maintenance_not_found():
    response = client.post("/player-actions/maintenance-interventions?session_id=nonexistent_id")
    assert response.status_code == 404
    assert "message" in response.json()


def test_do_maintenance_insufficient_funds(session_id):
    response = client.post(f"/player-actions/maintenance-interventions?session_id={session_id}")
    assert response.status_code == 400
    assert "message" in response.json()
