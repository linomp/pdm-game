<script lang="ts">
  import {
    type GameSessionDTO,
    type GameParametersDTO,
    SessionsService,
    PlayerActionsService,
  } from "../api/generated";
  import { isUndefinedOrNull } from "src/shared/utils";
  import GameOver from "src/components/GameOver.svelte";
  import MachineView from "src/components/MachineView.svelte";
  import SessionData from "src/components/SessionData.svelte";
  import MachineData from "src/components/MachineData.svelte";

  export let globalSettings: GameParametersDTO;

  let gameSession: GameSessionDTO;
  let gameOver = false;
  let gameOverReason: string | null = null;
  let maintenanceButtonDisabled = false;
  let sensorPurchaseButtonDisabled = false;
  let predictionPurchaseButtonDisabled = false;
  let dayInProgress = false;
  let stopAnimation = false;

  $: {
    stopAnimation = gameOver || !dayInProgress;
    maintenanceButtonDisabled =
      dayInProgress ||
      (gameSession?.available_funds ?? 0) <
        (globalSettings.maintenance_cost ?? Infinity);
    sensorPurchaseButtonDisabled =
      dayInProgress ||
      (gameSession?.available_funds ?? 0) <
        (globalSettings.sensor_cost ?? Infinity);
    predictionPurchaseButtonDisabled =
      dayInProgress ||
      (gameSession?.available_funds ?? 0) <
        (globalSettings.prediction_model_cost ?? Infinity);
  }

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
</script>

<div>
  <h2>The Predictive Maintenance Game</h2>
  <div class="game-area">
    <MachineView hidden={isUndefinedOrNull(gameSession)} {stopAnimation} />
    {#if gameOver}
      <GameOver gameOverReason={gameOverReason ?? ""} {gameSession} />
    {:else if !isUndefinedOrNull(gameSession)}
      <div class="game-data">
        <SessionData
          currentStep={gameSession.current_step}
          availableFunds={gameSession.available_funds ?? 0}
          maintenanceCost={globalSettings.maintenance_cost ?? 0}
          {dayInProgress}
          {maintenanceButtonDisabled}
          {advanceToNextDay}
          {doMaintenance}
        />
        <MachineData
          {globalSettings}
          {gameSession}
          {sensorPurchaseButtonDisabled}
          {predictionPurchaseButtonDisabled}
          {purchaseSensor}
          {purchaseRulPredictionModel}
        />
      </div>
    {:else}
      <button class="start-session-btn" on:click={startSession}>
        Start Session
      </button>
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

  .start-session-btn {
    align-self: flex-start;
    max-width: fit-content;
  }
</style>
