<script lang="ts">
  import {
    PlayerActionsService,
    SessionsService,
    type GameSessionDTO,
  } from "src/api/generated";
  import { SAMPLE_INTERVAL_MS } from "src/shared/types";
  import {
    formatNumber,
    isNotUndefinedNorNull,
    isUndefinedOrNull,
  } from "src/shared/utils";
  import {
    dayInProgress,
    gameOver,
    gameSession,
    globalSettings,
    maintenanceButtonDisabled,
    performedMaintenanceInThisTurn,
  } from "src/stores/stores";

  export let maintenanceCost: number;
  export let pollGameSession: () => Promise<void>;
  export let updateGameSession: (newGameSessionDto: GameSessionDTO) => void;

  $: {
    maintenanceButtonDisabled.set(
      $performedMaintenanceInThisTurn ||
        $dayInProgress ||
        ($gameSession?.available_funds ?? 0) < $globalSettings.maintenance_cost,
    );
  }

  const advanceToNextDay = async () => {
    if (isUndefinedOrNull($gameSession) || $gameOver) {
      return;
    }
    // TODO: migrate this polling strategy to websockets / MQTT
    // start fetching machine health every second while the day is advancing
    const intervalId = setInterval(pollGameSession, SAMPLE_INTERVAL_MS);
    dayInProgress.set(true);

    try {
      let newGameSessionDto = await SessionsService.advanceSessionsTurnsPut(
        $gameSession?.id!,
      );
      updateGameSession(newGameSessionDto);
    } catch (error) {
      console.error("Error advancing day:", error);
    } finally {
      await pollGameSession();
      // stop fetching machine health until the player advances to next day again
      clearInterval(intervalId);
      dayInProgress.set(false);
      performedMaintenanceInThisTurn.set(false);
    }
  };

  const doMaintenance = async () => {
    if ($gameOver || isUndefinedOrNull($gameSession)) {
      return;
    }

    try {
      const newGameSessionDto =
        await PlayerActionsService.doMaintenancePlayerActionsMaintenanceInterventionsPost(
          $gameSession!.id,
        );
      updateGameSession(newGameSessionDto);
      performedMaintenanceInThisTurn.set(true);
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to perform maintenance!");
      } else {
        console.error("Error performing maintenance:", error);
      }
    }
  };
</script>

{#if isNotUndefinedNorNull($gameSession) && !$gameOver}
  <div class="session-data">
    <p>Current Step: {$gameSession?.current_step}</p>
    <p>Available Funds: {formatNumber($gameSession?.available_funds)}</p>
    <div class="session-controls">
      <button on:click={advanceToNextDay} disabled={$dayInProgress}>
        Advance to next day
      </button>
      <button on:click={doMaintenance} disabled={$maintenanceButtonDisabled}>
        Perform Maintenance (${maintenanceCost})
      </button>
    </div>
  </div>
{/if}

<style>
  .session-data {
    margin: 1em;
  }

  .session-controls {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
</style>
