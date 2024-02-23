<script lang="ts">
  import { isUndefinedOrNull } from "src/shared/utils";
  import { PlayerActionsService } from "src/api/generated";
  import {
    dayInProgress,
    gameOver,
    gameSession,
    globalSettings,
    predictionPurchaseButtonDisabled,
    sensorPurchaseButtonDisabled,
  } from "src/stores/stores";
  import Sensor from "src/components/Sensor.svelte";

  $: {
    sensorPurchaseButtonDisabled.set(
      $dayInProgress ||
        ($gameSession?.available_funds ?? 0) <
          ($globalSettings?.sensor_cost ?? Infinity),
    );

    predictionPurchaseButtonDisabled.set(
      $dayInProgress ||
        ($gameSession?.available_funds ?? 0) <
          ($globalSettings?.prediction_model_cost ?? Infinity),
    );
  }

  const purchaseSensor = async (sensorName: string) => {
    if ($gameOver) {
      return;
    }

    try {
      const result =
        await PlayerActionsService.purchaseSensorPlayerActionsPurchasesSensorsPost(
          sensorName,
          $gameSession?.id!,
        );
      gameSession.set(result);
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to buy the sensor!");
      } else {
        console.error("Error buying sensor:", error);
      }
    }
  };

  const purchaseRulPredictionModel = async () => {
    if ($gameOver) {
      return;
    }

    try {
      const result =
        await PlayerActionsService.purchasePredictionPlayerActionsPurchasesPredictionModelsPost(
          "predicted_rul",
          $gameSession?.id!,
        );
      gameSession.set(result);
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to buy the prediction model!");
      } else {
        console.error("Error buying prediction model:", error);
      }
    }
  };
</script>

{#if !isUndefinedOrNull($gameSession)}
  <div class="machine-data">
    <h3>Operational Parameters</h3>
    {#each Object.entries($gameSession?.machine_state?.operational_parameters ?? {}) as [parameter, value]}
      <Sensor
        sensorCost={$globalSettings?.sensor_cost ?? 0}
        sensorPurchaseButtonDisabled={$sensorPurchaseButtonDisabled}
        {parameter}
        {value}
        {purchaseSensor}
      />
    {/each}
    <p>
      {"Remaining Useful Life"}: {$gameSession?.machine_state?.predicted_rul
        ? `${$gameSession.machine_state?.predicted_rul} steps`
        : "???"}
      <span
        hidden={!isUndefinedOrNull($gameSession?.machine_state?.predicted_rul)}
      >
        <button
          disabled={$predictionPurchaseButtonDisabled}
          on:click={() => purchaseRulPredictionModel()}
        >
          Buy (${$globalSettings?.prediction_model_cost})
        </button>
      </span>
    </p>
  </div>
{/if}