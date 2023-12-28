import asyncio
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.analysis import get_health_percentage, default_rul_prediction_fn, get_parameter_values
from mvp.server.constants import TIMESTEPS_PER_MOVE


class OperationalParameters(BaseModel):
    temperature: float
    oil_age: float
    mechanical_wear: float

    @staticmethod
    def from_dict(json: dict[str, float]) -> 'OperationalParameters':
        return OperationalParameters(
            temperature=json.get("temperature", 0),
            oil_age=json.get("oil_age", 0),
            mechanical_wear=json.get("mechanical_wear", 0)
        )


class MachineStats(BaseModel):
    predicted_rul: int | None = None
    health_percentage: int
    operational_parameters: OperationalParameters

    def is_broken(self) -> bool:
        if self.health_percentage <= 0:
            return True

        if self.predicted_rul is not None and self.predicted_rul <= 0:
            return True

        return False

    @staticmethod
    def from_dict(json: dict[str, Any]):
        return MachineStats(
            predicted_rul=json.get("predicted_rul", None),
            health_percentage=json.get("health_percentage", 0),
            operational_parameters=OperationalParameters.from_dict(
                json.get("operational_parameters", {})
            )
        )

    def __str__(self):
        return (f"MachineStats(predicted_rul={self.predicted_rul}, health_percentage={self.health_percentage}), "
                f"operational_parameters={self.operational_parameters})")


class GameSession(BaseModel):
    id: str
    current_step: int = 0
    machine_stats: MachineStats

    # TODO: Update this function in-game, to simulate a change in the model (an "upgrade" for the player)
    rul_predictor: Callable[[int], int | None] = default_rul_prediction_fn

    @staticmethod
    def new_game_session(id: str, current_step: int = 0):
        return GameSession(
            id=id,
            current_step=0,
            machine_stats=MachineStats(
                predicted_rul=None,
                health_percentage=get_health_percentage(current_step),
                operational_parameters=OperationalParameters.from_dict(get_parameter_values(current_step))
            )
        )

    async def advance_one_turn(self) -> list[MachineStats]:
        collected_machine_stats_during_turn = []

        for _ in range(TIMESTEPS_PER_MOVE):
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
        self.machine_stats.health_percentage = get_health_percentage(self.current_step,
                                                                     initial_value=self.machine_stats.health_percentage)
        self.machine_stats.operational_parameters = get_parameter_values(self.current_step)
        self.machine_stats.predicted_rul = self.rul_predictor(self.current_step)

    def _log(self, multiple=1):
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
            machine_stats=session.machine_stats,
        )

    @staticmethod
    def from_dict(json: dict[str, Any]):
        return GameSessionDTO(
            id=json.get("id", ""),
            current_step=json.get("current_step", 0),
            machine_stats=MachineStats.from_dict(json.get("machine_stats", {}))
        )
