from locust import HttpUser, task, between


class ApiUser(HttpUser):
    wait_time = between(1, 5)  # Simulate user waiting time between tasks
    session_id = None
    is_game_over = False

    @task
    def advance_turn(self):
        if self.is_game_over:
            return

        if self.session_id is None:
            # Create a session
            with self.client.post("/sessions/", catch_response=True) as response:
                try:
                    if response.status_code == 200:
                        self.session_id = response.json()["id"]
                    else:
                        raise Exception
                except Exception:
                    response.failure("Failed to create session")
                    print(str(response.content))
                    self.stop()
                    return

        # Advance the turn
        with self.client.put(f"/sessions/turns?session_id={self.session_id}", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if "is_game_over" in json_response and json_response["is_game_over"]:
                        self.is_game_over = True
                        print(f"Reached game over for session {self.session_id}")
                        response.success()
                        self.stop()
                    elif "id" in json_response and "current_step" in json_response:
                        response.success()
                    else:
                        raise Exception
                except Exception:
                    response.failure("Unexpected response structure")
                    print(str(response.content))
                    self.stop()
            else:
                response.failure("Failed to advance turn")
                print(str(response.content))
                self.stop()


if __name__ == "__main__":
    from locust.main import main

    main()
