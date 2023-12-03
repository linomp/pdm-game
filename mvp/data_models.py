from threading import Timer
from typing import Any, Callable

from pydantic import BaseModel

from mvp.analysis import get_health_percentage, default_rul_prediction_fn


class MachineStats(BaseModel):
    rul: int | None = None
    health_percentage: int

    @staticmethod
    def from_json(json: dict[str, Any]):
        return MachineStats(rul=json.get("rul", None), health_percentage=json.get("health_percentage", 0))

    def is_broken(self) -> bool:
        if self.health_percentage <= 0:
            return True

        if self.rul is not None and self.rul <= 0:
            return True

        return False

    def __str__(self):
        return f"MachineStats(rul={self.rul}, health_percentage={self.health_percentage})"


class GameSession(BaseModel):
    id: str
    current_step: int = 0
    machine_stats: MachineStats | None = None

    # This function can be updated in-game, to simulate a change in the model (an "upgrade" for the player)
    rul_predictor: Callable[[int], int | None] = default_rul_prediction_fn

    def __init__(self, id: str, current_step: int = 0):
        super().__init__(id=id, current_step=current_step)

        # init player's machine
        self.machine_stats = MachineStats(
            rul=None,
            health_percentage=get_health_percentage(self.current_step)
        )

        self._stop_event = False
        self._timer = None
        self._start_incrementing()

    def _start_incrementing(self):
        if not self._stop_event:
            # increment game counter (app tick)
            self.current_step += 1

            # update machine stats
            self.machine_stats.health_percentage = get_health_percentage(self.current_step)
            self.machine_stats.rul = self.rul_predictor(self.current_step)

            # check if game over
            if self.machine_stats.is_broken():
                print(f"GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_stats}")
                self.stop_incrementing()
                return

            # log every 5 steps
            if self.current_step % 5 == 0:
                print(f"GameSession '{self.id}' - step: {self.current_step} - {self.machine_stats}")

            self._timer = Timer(0.1, self._start_incrementing)
            self._timer.start()

    def stop_incrementing(self):
        self._stop_event = True
        if self._timer:
            self._timer.cancel()
