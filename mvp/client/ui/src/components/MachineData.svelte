<script lang="ts">
  import { isNotUndefinedNorNull } from "src/shared/utils";
  import { PlayerActionsService, type GameSessionDTO } from "src/api/generated";
  import {
    dayInProgress,
    gameOver,
    gameSession,
    globalSettings,
    predictionPurchaseButtonDisabled,
    sensorPurchaseButtonDisabled,
  } from "src/stores/stores";
  import Sensor from "src/components/Sensor.svelte";
  import type { TimeSeriesPoint } from "src/shared/types";

  export let updateGameSession: (newGameSessionDto: GameSessionDTO) => void;

  let data = {} as { [key: string]: TimeSeriesPoint[] };

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
      const newGameSessionDto =
        await PlayerActionsService.purchaseSensorPlayerActionsPurchasesSensorsPost(
          sensorName,
          $gameSession?.id!,
        );
      updateGameSession(newGameSessionDto);
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
      const newGameSessionDto =
        await PlayerActionsService.purchasePredictionPlayerActionsPurchasesPredictionModelsPost(
          "predicted_rul",
          $gameSession?.id!,
        );
      updateGameSession(newGameSessionDto);
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to buy the prediction model!");
      } else {
        console.error("Error buying prediction model:", error);
      }
    }
  };
</script>

{#if isNotUndefinedNorNull($gameSession) && !$gameOver}
  <div class="machine-data">
    <div class="sensors-display">
      {#each Object.entries($gameSession?.machine_state?.operational_parameters ?? {}) as [parameter, value]}
        <!-- TODO improve this horrible hack.. -->
        {#key $gameSession?.formattedTimeseries[parameter]}
          <Sensor
            sensorCost={$globalSettings?.sensor_cost ?? 0}
            sensorPurchaseButtonDisabled={$sensorPurchaseButtonDisabled}
            {parameter}
            {value}
            {purchaseSensor}
            data={$gameSession?.formattedTimeseries[parameter] ?? []}
          />
        {/key}
      {/each}
    </div>
    <div class="rul-display">
      {"Remaining Useful Life"}: {$gameSession?.machine_state?.predicted_rul
        ? `${$gameSession.machine_state?.predicted_rul} steps`
        : "???"}
      <span
        hidden={isNotUndefinedNorNull(
          $gameSession?.machine_state?.predicted_rul,
        )}
      >
        <button
          disabled={$predictionPurchaseButtonDisabled}
          on:click={() => purchaseRulPredictionModel()}
        >
          Buy (${$globalSettings?.prediction_model_cost})
        </button>
      </span>
    </div>
  </div>
{/if}

<style>
  .machine-data {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .sensors-display {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
</style>
