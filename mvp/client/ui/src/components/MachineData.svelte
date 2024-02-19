<script lang="ts">
  import { isUndefinedOrNull } from "src/shared/utils";
  import Sensor from "src/components/Sensor.svelte";
  import {
    PlayerActionsService,
    type GameParametersDTO,
    type GameSessionDTO,
  } from "src/api/generated";

  export let globalSettings: GameParametersDTO;
  export let gameSession: GameSessionDTO;
  export let sensorPurchaseButtonDisabled: boolean;
  export let predictionPurchaseButtonDisabled: boolean;
  export let gameOver: boolean;
  export let updateGameSession: (newObj: GameSessionDTO) => void;

  const purchaseSensor = async (sensorName: string) => {
    if (gameOver) {
      return;
    }

    try {
      const result =
        await PlayerActionsService.purchaseSensorPlayerActionsPurchasesSensorsPost(
          sensorName,
          gameSession?.id,
        );
      updateGameSession(result);
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to buy the sensor!");
      } else {
        console.error("Error buying sensor:", error);
      }
    }
  };

  const purchaseRulPredictionModel = async () => {
    if (gameOver) {
      return;
    }

    try {
      gameSession =
        await PlayerActionsService.purchasePredictionPlayerActionsPurchasesPredictionModelsPost(
          "predicted_rul",
          gameSession?.id,
        );
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to buy the prediction model!");
      } else {
        console.error("Error buying prediction model:", error);
      }
    }
  };
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
