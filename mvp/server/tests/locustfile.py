import os

from locust import HttpUser, task

from mvp.server.core.constants import PREDICTION_MODEL_COST, SENSOR_COST


class ApiUser(HttpUser):
    host = os.getenv("LOADTEST_HOST", "http://localhost:8000")
    session_id = None
    is_game_over = False
    sensors_to_purchase = {"temperature": False, "oil_age": False, "mechanical_wear": False}
    predictions_to_purchase = {"predicted_rul": False}

    @task
    def play_game(self):
        if self.is_game_over:
            self.stop()
            return

        if self.session_id is None:
            with self.client.get(f"/leaderboard/", catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Failed loading leaderboard: {response.status_code}")

            with self.client.post("/sessions/", catch_response=True) as response:
                if response.status_code == 200:
                    self.session_id = response.json()["id"]
                    response.success()
                else:
                    response.failure(f"Failed loading leaderboard: {response.status_code}")

        with self.client.put(f"/sessions/turns?session_id={self.session_id}", catch_response=True) as response:
            try:
                json_response = response.json()

                if ("is_game_over" in json_response) and (json_response["is_game_over"]):
                    self.is_game_over = True
                    self.client.post(f"/leaderboard/score?session_id={self.session_id}",
                                     json={"nickname": "LOCUST"}, catch_response=False)
                    response.success()
                    print(f"Game Over for {self.session_id}")
                    return
                elif ("id" in json_response) and ("current_step" in json_response):
                    funds = json_response["available_funds"]
                    self.purchase_sensors(funds)
                    self.purchase_predictions(funds)
                    response.success()
                else:
                    response.failure(f"Error advancing turn for {self.session_id}")
            except Exception as e:
                response.failure(f"Error advancing turn for {self.session_id}: {e}")

    def purchase_sensors(self, funds):
        for sensor, purchased in self.sensors_to_purchase.items():
            if (not purchased) and (
                    funds >= SENSOR_COST):
                with self.client.post(
                        f"/player-actions/purchases/sensors?session_id={self.session_id}&sensor={sensor}",
                        catch_response=True) as response:
                    if response.status_code == 200:
                        self.sensors_to_purchase[sensor] = True
                        funds -= SENSOR_COST
                        response.success()
                    else:
                        response.failure(f"failed {sensor} purchase for {self.session_id}")

    def purchase_predictions(self, funds):
        for prediction, purchased in self.predictions_to_purchase.items():
            if (not purchased) and (
                    funds >= PREDICTION_MODEL_COST):
                with self.client.post(
                        f"/player-actions/purchases/prediction-models?session_id={self.session_id}&prediction={prediction}",
                        catch_response=True) as response:
                    if response.status_code == 200:
                        self.predictions_to_purchase[prediction] = True
                        funds -= PREDICTION_MODEL_COST
                        response.success()
                    else:
                        response.failure(f"failed {prediction} purchase for {self.session_id}")


if __name__ == "__main__":
    from locust.main import main

    main()
