from unittest.mock import MagicMock

import pytest

from mvp.server.core.constants import TIMESTEPS_PER_MOVE
from mvp.server.core.game.GameSession import GameSession


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
    collected_states = []
    for i in range(total_turns_to_simulate):
        last_state, _ = await game_session.advance_one_turn()
        collected_states.append(last_state)

    assert len(collected_states) == total_turns_to_simulate
    assert game_session.current_step == initial_step + total_turns_to_simulate * TIMESTEPS_PER_MOVE

    # noinspection PyUnresolvedReferences
    assert game_session.state_publish_function.call_count >= total_turns_to_simulate

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
