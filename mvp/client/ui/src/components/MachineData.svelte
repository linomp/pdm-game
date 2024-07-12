<script lang="ts">
  import {isNotUndefinedNorNull} from "src/shared/utils";
  import {type GameSessionDTO, PlayerActionsService} from "src/api/generated";
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
        alert(error.body.message);
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
        alert(error.body.message);
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
        />
      {/each}
    </div>
    <div class="rul-display">
      <span> {"Remaining Useful Life"}: </span>
      <span>{$gameSession?.machine_state?.predicted_rul
        ? `${$gameSession.machine_state?.predicted_rul} steps`
        : "???"}
      </span>
      <span
        hidden={isNotUndefinedNorNull(
          $gameSession?.machine_state?.predicted_rul,
        )}
      >
        <button
          disabled={$predictionPurchaseButtonDisabled}
          on:mousedown={() => purchaseRulPredictionModel()}
        >
          Buy Predictive Model (${$globalSettings.prediction_model_cost})
        </button>
      </span>
    </div>
    <div class="user-messages">
      {#each Object.entries($gameSession?.user_messages ?? {}) as [key, message]}
        <div class="message-card {message.type}">
          <span>{message.content}</span>
        </div>
      {/each}
    </div>
  </div>
{/if}

<style>
  .machine-data {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 2em;
    position: relative;
  }

  .sensors-display {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
  }

  .rul-display {
    margin-top: 1em;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: center;
  }

  .user-messages {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 2em;
    align-items: center;
    width: 80%;
  }

  .message-card {
    border-radius: 8px;
    padding: 1em;
    width: 100%;
    text-align: center;
    border: 1px solid #ccc;
    transition: opacity 0.3s;
    font-size: smaller;
  }

  .message-card.WARNING {
    background-color: #ffffe0;
    color: #000000;
  }

  .message-card.INFO {
    background-color: rgba(129, 248, 94, 0.86);
    color: #000000;
  }
</style>
