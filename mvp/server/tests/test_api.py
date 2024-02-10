import pytest
from fastapi.testclient import TestClient

from mvp.server.api import app
from mvp.server.core.constants import INITIAL_CASH, MAINTENANCE_COST, SENSOR_COST, PREDICTION_MODEL_COST

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


def test_purchase_sensor(session_id):
    available_funds = INITIAL_CASH

    for sensor in ["temperature", "oil_age", "mechanical_wear"]:
        while available_funds < SENSOR_COST:
            response = client.post(f"/player-actions/purchases/sensors?session_id={session_id}&sensor=temperature")
            assert response.status_code == 400

            response = client.put(f"/sessions/turns?session_id={session_id}")
            available_funds = response.json()["available_funds"]

        response = client.post(f"/player-actions/purchases/sensors?session_id={session_id}&sensor={sensor}")

        assert response.status_code == 200
        assert response.json()["available_funds"] == available_funds - SENSOR_COST
        assert response.json()["machine_state"]["operational_parameters"][sensor] is not None

        available_funds = response.json()["available_funds"]


def test_purchase_sensor_not_found(session_id):
    response = client.post(f"/player-actions/purchases/sensors?session_id={session_id}&sensor=nonexistent_sensor")
    assert response.status_code == 404
    assert "message" in response.json()


def test_purchase_sensor_insufficient_funds(session_id):
    response = client.post(f"/player-actions/purchases/sensors?session_id={session_id}&sensor=temperature")
    assert response.status_code == 400
    assert "message" in response.json()


def test_purchase_prediction(session_id):
    available_funds = INITIAL_CASH

    for prediction in ["predicted_rul"]:
        while available_funds < PREDICTION_MODEL_COST:
            response = client.post(
                f"/player-actions/purchases/prediction-models?session_id={session_id}&prediction={prediction}")
            assert response.status_code == 400

            response = client.put(f"/sessions/turns?session_id={session_id}")
            available_funds = response.json()["available_funds"]

        response = client.post(
            f"/player-actions/purchases/prediction-models?session_id={session_id}&prediction={prediction}")

        assert response.status_code == 200
        assert response.json()["available_funds"] == available_funds - PREDICTION_MODEL_COST
        assert response.json()["machine_state"][prediction] is not None

        available_funds = response.json()["available_funds"]


def test_purchase_prediction_not_found(session_id):
    response = client.post(
        f"/player-actions/purchases/prediction-models?session_id={session_id}&prediction=nonexistent_prediction")
    assert response.status_code == 404
    assert "message" in response.json()


def test_purchase_prediction_insufficient_funds(session_id):
    response = client.post(
        f"/player-actions/purchases/prediction-models?session_id={session_id}&prediction=predicted_rul")
    assert response.status_code == 400
    assert "message" in response.json()
