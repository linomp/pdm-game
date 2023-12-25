import pytest

from mvp.server.analysis import get_machine_temperature
from mvp.server.constants import TIMESTEPS_PER_MOVE


def test_get_machine_temperature():
    for i in range(0, 40):
        # check that it grows monotonically until the last timestep of the move
        if i % TIMESTEPS_PER_MOVE != TIMESTEPS_PER_MOVE - 1:
            assert get_machine_temperature(i) <= get_machine_temperature(i + 1)

        # check that it resets after the last timestep of the move
        assert pytest.approx(get_machine_temperature(i), 10) == pytest.approx(
            get_machine_temperature(i + TIMESTEPS_PER_MOVE), 10)
