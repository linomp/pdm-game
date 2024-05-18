from matplotlib.pyplot import figure, show

from mvp.server.core.machine.MachineState import MachineState


class MachineWrapperForExperiment:
    current_step: int = 0
    machine_state: MachineState
    machine_state_history: dict[str, list]

    def __init__(self):
        self.current_step = 0
        self.machine_state = MachineState.new_machine_state()
        self.machine_state_history = {
            "time": [],
            "temperature": [],
            "oil_age": [],
            "mechanical_wear": [],
            "health_percentage": [],
            "predicted_rul": []
        }
        self._record_state()

    def _record_state(self):
        self.machine_state_history["time"].append(self.current_step)
        self.machine_state_history["temperature"].append(self.machine_state.operational_parameters.temperature)
        self.machine_state_history["oil_age"].append(self.machine_state.operational_parameters.oil_age)
        self.machine_state_history["mechanical_wear"].append(self.machine_state.operational_parameters.mechanical_wear)
        self.machine_state_history["health_percentage"].append(self.machine_state.health_percentage)
        self.machine_state_history["predicted_rul"].append(self.machine_state.predicted_rul)

    def advance_one_step(self):
        self.current_step += 1
        self.machine_state.update_parameters(self.current_step)
        self._record_state()

    def run_to_failure(self) -> dict[str, list]:
        while not self.machine_state.is_broken():
            self.advance_one_step()
        return self.machine_state_history


if __name__ == "__main__":
    machine = MachineWrapperForExperiment()
    history = machine.run_to_failure()

    fig = figure(figsize=(10, 10))
    ax1 = fig.add_subplot(221)
    ax1.plot(history["time"], history["temperature"])
    ax1.set_title("Temperature")
    ax2 = fig.add_subplot(222)
    ax2.plot(history["time"], history["oil_age"])
    ax2.set_title("Oil Age")
    ax3 = fig.add_subplot(223)
    ax3.plot(history["time"], history["mechanical_wear"])
    ax3.set_title("Mechanical Wear")
    ax4 = fig.add_subplot(224)
    ax4.plot(history["time"], history["health_percentage"])
    ax4.set_title("Health Percentage")
    show()
