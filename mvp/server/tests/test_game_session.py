from unittest.mock import MagicMock

import pytest

from mvp.server.core.constants import TIMESTEPS_PER_MOVE
from mvp.server.core.game.GameSession import GameSession
from mvp.server.core.machine.MachineState import MachineState


@pytest.fixture
def game_session():
    fake_publish_function = MagicMock(name='state_publish_function')
    session = GameSession.new_game_session(_id="test_session", _state_publish_function=fake_publish_function)
    session._log = MagicMock(name='log')
    return session


def test_game_session_initialization(game_session):
    assert game_session.id == "test_session"
    assert game_session.current_step == 0
    assert game_session.machine_state is not None
    assert game_session.machine_state.operational_parameters is not None


@pytest.mark.asyncio
async def test_game_session_advance_one_turn(game_session):
    initial_health = game_session.machine_state.health_percentage
    initial_step = game_session.current_step

    total_turns_to_simulate = 5
    collected_stats = []
    for i in range(total_turns_to_simulate):
        collected_stats.extend(await game_session.advance_one_turn())

    assert len(collected_stats) == total_turns_to_simulate * TIMESTEPS_PER_MOVE
    assert game_session.current_step == initial_step + total_turns_to_simulate * TIMESTEPS_PER_MOVE

    assert len(game_session.machine_state_history) == total_turns_to_simulate * TIMESTEPS_PER_MOVE
    for i in range(TIMESTEPS_PER_MOVE):
        assert game_session.machine_state_history[i][0] == i
        assert isinstance(game_session.machine_state_history[i][1], MachineState)

    assert game_session.state_publish_function.call_count == total_turns_to_simulate * TIMESTEPS_PER_MOVE

    final_health = game_session.machine_state.health_percentage
    assert final_health < initial_health


@pytest.mark.asyncio
async def test_game_session_machine_breakdown(game_session):
    game_session.machine_state.health_percentage = 0
    assert game_session.machine_state.is_broken() is True

    game_session.machine_state.health_percentage = -1
    assert game_session.machine_state.is_broken() is True

    game_session.machine_state.health_percentage = 50
    game_session.machine_state.predicted_rul = 10
    assert game_session.machine_state.is_broken() is False
