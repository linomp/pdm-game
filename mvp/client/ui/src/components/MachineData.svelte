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

  export let updateGameSession: (newGameSessionDto: GameSessionDTO) => void;

  $: {
    sensorPurchaseButtonDisabled.set(
      $gameSession?.is_game_over ||
        $dayInProgress ||
        ($gameSession?.available_funds ?? 0) < $globalSettings.sensor_cost,
    );

    predictionPurchaseButtonDisabled.set(
      $gameSession?.is_game_over ||
        $dayInProgress ||
        ($gameSession?.available_funds ?? 0) <
          $globalSettings.prediction_model_cost,
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

{#if isNotUndefinedNorNull($gameSession)}
  <div class="machine-data">
    <div class="sensors-display">
      {#each Object.entries($gameSession?.machine_state?.operational_parameters ?? {}) as [parameter, value]}
        <Sensor
          sensorCost={$globalSettings.sensor_cost}
          sensorPurchaseButtonDisabled={$sensorPurchaseButtonDisabled}
          {parameter}
          {value}
          {purchaseSensor}
          data={$gameSession?.formattedTimeseries[parameter] ?? []}
          warningLevel={$globalSettings.warning_levels[parameter]}
        />
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
          Buy (${$globalSettings.prediction_model_cost})
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
