<script lang="ts">
  import { isUndefinedOrNull } from "src/shared/utils";
  import Sensor from "src/components/Sensor.svelte";
  import type { GameParametersDTO, GameSessionDTO } from "src/api/generated";

  export let globalSettings: GameParametersDTO;
  export let gameSession: GameSessionDTO;
  export let sensorPurchaseButtonDisabled: boolean;
  export let predictionPurchaseButtonDisabled: boolean;
  export let purchaseSensor: (parameter: string) => void;
  export let purchaseRulPredictionModel: () => void;
</script>

<div class="machine-data">
  <h3>Operational Parameters</h3>
  {#each Object.entries(gameSession.machine_state?.operational_parameters ?? {}) as [parameter, value]}
    <Sensor
      sensorCost={globalSettings.sensor_cost ?? 0}
      {parameter}
      {value}
      {sensorPurchaseButtonDisabled}
      {purchaseSensor}
    />
  {/each}
  <p>
    {"Remaining Useful Life"}: {gameSession.machine_state?.predicted_rul
      ? `${gameSession.machine_state?.predicted_rul} steps`
      : "???"}
    <span hidden={!isUndefinedOrNull(gameSession.machine_state?.predicted_rul)}>
      <button
        disabled={predictionPurchaseButtonDisabled}
        on:click={() => purchaseRulPredictionModel()}
      >
        Buy (${globalSettings.prediction_model_cost})
      </button>
    </span>
  </p>
</div>
