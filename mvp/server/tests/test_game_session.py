import pytest

from mvp.server.constants import TIMESTEPS_PER_MOVE
from mvp.server.data_models.GameSession import GameSession


@pytest.fixture
def game_session():
    return GameSession.new_game_session(_id="test_session")


def test_game_session_initialization(game_session):
    assert game_session.id == "test_session"
    assert game_session.current_step == 0
    assert game_session.machine_stats is not None
    assert game_session.machine_stats.operational_parameters is not None


@pytest.mark.asyncio
async def test_game_session_advance_one_turn(game_session):
    initial_health = game_session.machine_stats.health_percentage
    initial_step = game_session.current_step

    collected_stats = await game_session.advance_one_turn()
    assert len(collected_stats) == TIMESTEPS_PER_MOVE

    # Checking if current_step increases correctly after each turn
    assert game_session.current_step == initial_step + TIMESTEPS_PER_MOVE

    # Checking if health decreases after each turn
    final_health = game_session.machine_stats.health_percentage
    assert final_health < initial_health


@pytest.mark.asyncio
async def test_game_session_machine_breakdown(game_session):
    game_session.machine_stats.health_percentage = 0
    assert game_session.machine_stats.is_broken() is True

    game_session.machine_stats.health_percentage = -1
    assert game_session.machine_stats.is_broken() is True

    game_session.machine_stats.health_percentage = 50
    game_session.machine_stats.predicted_rul = 10
    assert game_session.machine_stats.is_broken() is False
