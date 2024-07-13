<script lang="ts">
  import {type GameSessionDTO, PlayerActionsService, SessionsService} from "src/api/generated";
  import {formatNumber, isNotUndefinedNorNull, isUndefinedOrNull} from "src/shared/utils";
  import {
    dayInProgress,
    gameOver,
    gameSession,
    globalSettings,
    isOnNarrowScreen,
    maintenanceButtonDisabled,
    performedMaintenanceInThisTurn,
  } from "src/stores/stores";

  export let maintenanceCost: number;
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

    dayInProgress.set(true);

    try {
      let newGameSessionDto = await SessionsService.advanceSessionsTurnsPut(
        $gameSession?.id!,
      );
      updateGameSession(newGameSessionDto);
    } catch (error) {
      console.error("Error advancing day:", error);
    } finally {
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
        alert(error.body.message);
      } else {
        console.error("Error performing maintenance:", error);
      }
    }
  };
</script>

{#if isNotUndefinedNorNull($gameSession) && !$gameOver}
  <div class="session-data">
    <p>Current Step: {$gameSession?.current_step}</p>
    <p>
      Available Funds:
      <span
        class:rainbow-funds={($gameSession?.cash_multiplier??0) > 1}>{formatNumber($gameSession?.available_funds)}</span>
      <span
        hidden={($gameSession?.cash_multiplier??0) <= 1}>🔥 (3x !!)
      </span>
    </p>
    <div class={`session-controls ${$isOnNarrowScreen ? "flex-row" : "flex-col"}`}>
      <button on:mousedown={advanceToNextDay} disabled={$dayInProgress}>
        Advance to next day
      </button>
      <button on:mousedown={doMaintenance} disabled={$maintenanceButtonDisabled}>
        Perform Maintenance (${maintenanceCost})
      </button>
    </div>
  </div>
{/if}

<style>
  .session-data {
    margin-top: 1em;
    margin-right: 1em;
  }

  .session-controls {
    display: flex;
    gap: 0.75rem;
  }

  .flex-row {
    flex-direction: row;
  }

  .flex-col {
    flex-direction: column;
  }

  .rainbow-funds {
    background-image: linear-gradient(to right, red, orange, #f3bd5a, green, cadetblue, dodgerblue);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-weight: bold;
    animation: rainbow-animation 5s linear infinite;
  }

  @keyframes rainbow-animation {
    0% {
      background-position: 0% 50%;
    }
    100% {
      background-position: 100% 50%;
    }
  }
</style>
