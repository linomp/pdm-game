import os

from locust import HttpUser, task, between


class ApiUser(HttpUser):
    host = os.getenv("LOADTEST_HOST", "http://localhost:8000")
    wait_time = between(1, 5)  # Simulate user waiting time between tasks
    session_id = None
    is_game_over = False

    @task
    def advance_turn(self):
        if self.is_game_over:
            self.stop()
            return

        if self.session_id is None:
            # Create a session
            with self.client.post("/sessions/", catch_response=True) as response:
                try:
                    self.session_id = response.json()["id"]
                except Exception:
                    response.failure("Failed to create session")
                    print(str(response.content))
                    return

        # Advance the turn
        with self.client.put(f"/sessions/turns?session_id={self.session_id}", catch_response=True) as response:
            try:
                json_response = response.json()
                if "is_game_over" in json_response and json_response["is_game_over"]:
                    self.is_game_over = True
                    print(f"Reached game over for session {self.session_id}")
                    self.client.post(f"/leaderboard/score?session_id={self.session_id}",
                                     json={"nickname": "testLocust"}, catch_response=False)
                    response.success()
                    self.stop()
                elif "id" in json_response and "current_step" in json_response:
                    response.success()
                else:
                    raise Exception
            except Exception as e:
                response.failure("Failed to advance turn")
                print(f"{str(response.content)} {e}")


if __name__ == "__main__":
    from locust.main import main

    main()
