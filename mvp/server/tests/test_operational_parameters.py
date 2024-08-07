from mvp.server.core.constants import TIMESTEPS_PER_MOVE
from mvp.server.core.machine.MachineState import OperationalParameters


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


def test_oil_age_grows_monotonically():
    operational_parameters = OperationalParameters(temperature=0, oil_age=0, mechanical_wear=0)

    for i in range(0, TIMESTEPS_PER_MOVE - 1):
        current_oil_age = operational_parameters.compute_oil_age(i)
        next_oil_age = operational_parameters.compute_oil_age(i + 1)
        assert current_oil_age <= next_oil_age


def test_mechanical_wear_grows_monotonically():
    operational_parameters = OperationalParameters(temperature=0, oil_age=0, mechanical_wear=0)

    for i in range(0, TIMESTEPS_PER_MOVE - 1):
        current_mechanical_wear = operational_parameters.compute_mechanical_wear(i)
        next_mechanical_wear = operational_parameters.compute_mechanical_wear(i + 1)
        assert current_mechanical_wear <= next_mechanical_wear
