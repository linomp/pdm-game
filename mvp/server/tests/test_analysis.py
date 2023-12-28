import pytest

from mvp.server.analysis import get_machine_temperature
from mvp.server.constants import TIMESTEPS_PER_MOVE


def test_temperature_grows_monotonically():
    # check that it grows monotonically until the last timestep of the move
    assert all(
        get_machine_temperature(i) <= get_machine_temperature(i + 1)
        for i in range(0, TIMESTEPS_PER_MOVE - 1)
    )


def test_temperature_is_periodic():
    # check that it resets after the last timestep of the move
    assert all(
        pytest.approx(
            get_machine_temperature(i), 10) == pytest.approx(get_machine_temperature(i + TIMESTEPS_PER_MOVE),
                                                             10)
        for i in range(0, 40)
    )
