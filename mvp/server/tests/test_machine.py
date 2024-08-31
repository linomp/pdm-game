from mvp.server.core.Machine import Machine
from mvp.server.core.constants import TIMESTEPS_PER_MOVE


def test_temperature_grows_monotonically():
    machine = Machine.new_machine()

    for i in range(0, TIMESTEPS_PER_MOVE - 1):
        current_temp = machine.compute_machine_temperature(i)
        next_temp = machine.compute_machine_temperature(i + 1)
        assert current_temp <= next_temp


def test_temperature_is_periodic():
    machine = Machine.new_machine()

    for i in range(0, 40):
        current_temp = machine.compute_machine_temperature(i)
        future_temp = machine.compute_machine_temperature(i + TIMESTEPS_PER_MOVE)
        assert round(current_temp, 10) == round(future_temp, 10)


def test_oil_age_grows_monotonically():
    machine = Machine.new_machine()
    machine.temperature = 0

    for i in range(0, TIMESTEPS_PER_MOVE - 1):
        current_oil_age = machine.compute_oil_age(i)
        next_oil_age = machine.compute_oil_age(i + 1)
        assert current_oil_age <= next_oil_age


def test_mechanical_wear_grows_monotonically():
    machine = Machine.new_machine()

    for i in range(0, TIMESTEPS_PER_MOVE - 1):
        current_mechanical_wear = machine.compute_mechanical_wear(i)
        next_mechanical_wear = machine.compute_mechanical_wear(i + 1)
        assert current_mechanical_wear <= next_mechanical_wear
