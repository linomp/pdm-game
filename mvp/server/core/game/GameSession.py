import asyncio
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.core.analysis.rul_prediction import default_rul_prediction_fn
from mvp.server.core.constants import TIMESTEPS_PER_MOVE, INITIAL_CASH, MAINTENANCE_COST, REVENUE_PER_DAY
from mvp.server.core.machine.MachineState import MachineState


class GameSession(BaseModel):
    id: str
    current_step: int = 0
    machine_state: MachineState
    available_funds: float = 0.
    is_game_over: bool = False

    # TODO: Update this function in-game, to simulate a change in the model (an "upgrade" for the player)
    rul_predictor: Callable[[int], int | None] = default_rul_prediction_fn

    @staticmethod
    def new_game_session(_id: str):
        return GameSession(
            id=_id,
            current_step=0,
            machine_state=MachineState.new_machine_state(),
            available_funds=INITIAL_CASH,
        )

    def check_if_game_over(self):
        if self.machine_state.is_broken():
            print(f"GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_state}")
            self.is_game_over = True
            return

        # TODO: decide if < 0 or <= 0
        if self.available_funds < 0:
            print(
                f"GameSession '{self.id}' - player ran out of money at step {self.current_step} - {self.machine_state}")
            self.is_game_over = True
            return

        self.is_game_over = False

    async def advance_one_turn(self) -> list[MachineState]:
        collected_machine_states_during_turn = []

        for _ in range(TIMESTEPS_PER_MOVE):
            # collect stats
            collected_machine_states_during_turn.append(self.machine_state)

            self.check_if_game_over()
            if self.is_game_over:
                break

            self.current_step += 1
            self.machine_state.update(self.current_step, self.rul_predictor)
            # Player earns money for the production at every timestep
            self.available_funds += REVENUE_PER_DAY / TIMESTEPS_PER_MOVE
            self._log()

            await asyncio.sleep(0.5)

        return collected_machine_states_during_turn

    def do_maintenance(self) -> bool:
        if self.available_funds < MAINTENANCE_COST:
            return False

        self.available_funds -= MAINTENANCE_COST
        self.machine_state.do_maintenance()
        return True

    def _log(self, multiple=5):
        if self.current_step % multiple == 0:
            print(f"GameSession '{self.id}' - step: {self.current_step} - {self.machine_state}")


class GameSessionDTO(BaseModel):
    id: str
    current_step: int
    machine_state: MachineState | None = None
    available_funds: float = 0.
    is_game_over: bool = False
    game_over_reason: str | None = None

    # TODO: define MachineStateDTO to hide some fields from the player, e.g. health_percentage

    @staticmethod
    def from_session(session: 'GameSession'):
        dto = GameSessionDTO(
            id=session.id,
            current_step=session.current_step,
            machine_state=session.machine_state,
            available_funds=session.available_funds,
            is_game_over=session.is_game_over,
        )

        if session.is_game_over:
            dto.game_over_reason = "Machine health has reached 0%" if session.machine_state.is_broken() else "Player ran out of money"

        return dto

    @staticmethod
    def from_dict(json: dict[str, Any]):
        return GameSessionDTO(
            id=json.get("id", ""),
            current_step=json.get("current_step", 0),
            machine_state=MachineState.from_dict(json.get("machine_state", {})),
            available_funds=json.get("available_funds", 0.),
            is_game_over=json.get("is_game_over", False),
        )
