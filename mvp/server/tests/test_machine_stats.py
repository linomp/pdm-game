from mvp.server.constants import TIMESTEPS_PER_MOVE
from mvp.server.data_models.MachineStats import OperationalParameters


def test_temperature_grows_monotonically():
    operational_parameters = OperationalParameters(temperature=0, oil_age=0, mechanical_wear=0)

    for i in range(0, TIMESTEPS_PER_MOVE - 1):
        current_temp = operational_parameters.compute_machine_temperature(i)
        next_temp = operational_parameters.compute_machine_temperature(i + 1)
        assert current_temp <= next_temp


def test_temperature_is_periodic():
    operational_parameters = OperationalParameters(temperature=0, oil_age=0, mechanical_wear=0)

    for i in range(0, 40):
        current_temp = operational_parameters.compute_machine_temperature(i)
        future_temp = operational_parameters.compute_machine_temperature(i + TIMESTEPS_PER_MOVE)
        assert round(current_temp, 10) == round(future_temp, 10)
