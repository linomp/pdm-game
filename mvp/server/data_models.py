import asyncio
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.analysis import get_health_percentage, default_rul_prediction_fn
from mvp.server.constants import STEPS_PER_MOVE


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

    async def advance_one_turn(self) -> list[MachineStats]:
        collected_machine_stats_during_turn = []

        for _ in range(STEPS_PER_MOVE):
            # collect stats
            collected_machine_stats_during_turn.append(self.machine_stats)

            # check if game over
            if self.machine_stats.is_broken():
                print(f"GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_stats}")
                break

            self.current_step += 1
            self._update_machine_stats()
            self._log()

            await asyncio.sleep(0.5)

        return collected_machine_stats_during_turn

    def _update_machine_stats(self):
        self.machine_stats.health_percentage = get_health_percentage(self.current_step)
        self.machine_stats.rul = self.rul_predictor(self.current_step)

    def _log(self, multiple=5):
        if self.current_step % multiple == 0:
            print(f"GameSession '{self.id}' - step: {self.current_step} - {self.machine_stats}")


class GameSessionDTO(BaseModel):
    id: str
    current_step: int
    machine_stats: MachineStats | None = None

    @staticmethod
    def from_session(session: 'GameSession'):
        return GameSessionDTO(
            id=session.id,
            current_step=session.current_step,
            machine_stats=session.machine_stats
        )

    @staticmethod
    def from_json(json: dict[str, Any]):
        return GameSessionDTO(
            id=json.get("id", ""),
            current_step=json.get("current_step", 0),
            machine_stats=MachineStats.from_json(json.get("machine_stats", {}))
        )
