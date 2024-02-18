<script lang="ts">
  import { onMount } from "svelte";
  import {
    type GameSessionDTO,
    type GameParametersDTO,
    SessionsService,
    PlayerActionsService,
    GameParametersService,
  } from "../api/generated";
  import runningMachineSrc from "/img/healthy.gif";

  const stoppedMachineSrc = new URL("/img/stopped.PNG", import.meta.url).href;

  let gameSession: GameSessionDTO | null;
  let gameOver = false;
  let gameOverReason: string | null = null;
  let maintenanceButtonDisabled = false;
  let sensorPurchaseButtonDisabled = false;
  let predictionPurchaseButtonDisabled = false;
  let dayInProgress = false;
  let stopAnimation = false;
  let globalSettings: GameParametersDTO;

  $: {
    stopAnimation = gameOver || !dayInProgress;
    maintenanceButtonDisabled =
      dayInProgress ||
      (gameSession?.available_funds ?? 0) <
        (globalSettings?.maintenance_cost ?? Infinity);
    sensorPurchaseButtonDisabled =
      dayInProgress ||
      (gameSession?.available_funds ?? 0) <
        (globalSettings?.sensor_cost ?? Infinity);
    predictionPurchaseButtonDisabled =
      dayInProgress ||
      (gameSession?.available_funds ?? 0) <
        (globalSettings?.prediction_model_cost ?? Infinity);
  }

  onMount(async () => {
    try {
      globalSettings =
        await GameParametersService.getParametersGameParametersGet();
    } catch (error) {
      console.error("Error fetching global settings:", error);
    }
  });

  const startSession = async () => {
    try {
      gameSession = await SessionsService.createSessionSessionsPost();
    } catch (error) {
      console.error("Error fetching session:", error);
    }
  };

  const fetchExistingSession = async () => {
    if (!gameSession || gameOver) {
      return;
    }

    try {
      gameSession = await SessionsService.getSessionSessionsGet(
        gameSession?.id,
      );
      checkForGameOver();
    } catch (error) {
      console.error("Error fetching session:", error);
    }
  };

  const advanceToNextDay = async () => {
    if (!gameSession || gameOver) {
      return;
    }

    // TODO: migrate this polling strategy to a websocket connection
    // start fetching machine health every second while the day is advancing
    const intervalId = setInterval(fetchExistingSession, 500);
    dayInProgress = true;

    try {
      gameSession = await SessionsService.advanceSessionsTurnsPut(
        gameSession?.id,
      );
    } catch (error) {
      console.error("Error advancing day:", error);
    } finally {
      await fetchExistingSession();
      // stop fetching machine health until the player advances to next day again
      clearInterval(intervalId);
      dayInProgress = false;
    }
  };

  const doMaintenance = async () => {
    if (!gameSession || gameOver) {
      return;
    }

    try {
      gameSession =
        await PlayerActionsService.doMaintenancePlayerActionsMaintenanceInterventionsPost(
          gameSession?.id,
        );
      await advanceToNextDay();
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to perform maintenance!");
      } else {
        console.error("Error performing maintenance:", error);
      }
    }
  };

  const purchaseSensor = async (sensorName: string) => {
    if (!gameSession || gameOver) {
      return;
    }

    try {
      gameSession =
        await PlayerActionsService.purchaseSensorPlayerActionsPurchasesSensorsPost(
          sensorName,
          gameSession?.id,
        );
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to buy the sensor!");
      } else {
        console.error("Error buying sensor:", error);
      }
    }
  };

  const purchaseRulPredictionModel = async () => {
    if (!gameSession || gameOver) {
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

  const checkForGameOver = () => {
    if (!gameSession) {
      return;
    }

    gameOver = gameSession.is_game_over ?? false;
    gameOverReason = gameSession.game_over_reason ?? null;
  };

  const formatParameterName = (parameter: string) => {
    return parameter
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };
</script>

<div>
  <h2>The Predictive Maintenance Game</h2>
  <div class="game-area">
    <img
      class="machine-view"
      src={stopAnimation ? stoppedMachineSrc : runningMachineSrc}
      alt="..."
      width="369"
      height="276"
      hidden={!gameSession}
    />
    {#if gameOver}
      <h3>Game Over</h3>
      <pre>{JSON.stringify(gameSession, null, 2)}</pre>
      <p>{gameOverReason}</p>
    {:else if gameSession}
      <div class="game-data">
        <div class="session-data">
          <h3>Game Session Details</h3>
          <p>Current Step: {gameSession.current_step}</p>
          <p>Available Funds: {gameSession.available_funds}</p>
          <div class="session-commands">
            <button on:click={advanceToNextDay} disabled={dayInProgress}>
              Advance to next day
            </button>
            <button
              on:click={doMaintenance}
              disabled={maintenanceButtonDisabled}
            >
              Perform Maintenance (${globalSettings?.maintenance_cost ?? 0})
            </button>
          </div>
        </div>
        <div class="machine-data">
          <h3>Operational Parameters</h3>
          <ul>
            {#each Object.entries(gameSession.machine_state?.operational_parameters ?? {}) as [parameter, value]}
              <li>
                <p>
                  {formatParameterName(parameter)}: {value ?? "???"}
                  <span hidden={value != null}>
                    <button
                      disabled={sensorPurchaseButtonDisabled}
                      on:click={() => purchaseSensor(parameter)}
                    >
                      Buy (${globalSettings?.sensor_cost})
                    </button>
                  </span>
                </p>
              </li>
            {/each}
            <li>
              <p>
                {"Remaining Useful Life"}: {gameSession.machine_state
                  ?.predicted_rul
                  ? `${gameSession.machine_state?.predicted_rul} steps`
                  : "???"}
                <span hidden={gameSession.machine_state?.predicted_rul != null}>
                  <button
                    disabled={predictionPurchaseButtonDisabled}
                    on:click={() => purchaseRulPredictionModel()}
                  >
                    Buy (${globalSettings?.prediction_model_cost})
                  </button>
                </span>
              </p>
            </li>
          </ul>
        </div>
      </div>
    {:else}
      <button class="start-session-btn" on:click={startSession}
        >Start Session</button
      >
    {/if}
  </div>
</div>

<style>
  .game-area {
    display: flex;
    flex-direction: column;
  }

  .game-data {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    row-gap: 1rem;
    column-gap: 3rem;
  }

  .session-commands {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  .start-session-btn {
    align-self: flex-start;
    max-width: fit-content;
  }
</style>
