<script lang="ts">
  import { PlayerActionsService, SessionsService } from "src/api/generated";
  import { isUndefinedOrNull } from "src/shared/utils";
  import {
    dayInProgress,
    gameOver,
    gameSession,
    globalSettings,
    machineStateSnapshots,
    maintenanceButtonDisabled,
    performedMaintenanceInThisTurn,
  } from "src/stores/stores";

  export let maintenanceCost: number;
  export let fetchExistingSession: () => Promise<void>;

  $: {
    maintenanceButtonDisabled.set(
      $performedMaintenanceInThisTurn ||
        $dayInProgress ||
        ($gameSession?.available_funds ?? 0) <
          ($globalSettings?.maintenance_cost ?? Infinity),
    );
  }

  const advanceToNextDay = async () => {
    if (isUndefinedOrNull($gameSession) || $gameOver) {
      return;
    }
    // TODO: migrate this polling strategy to a websocket connection
    // start fetching machine health every second while the day is advancing
    const intervalId = setInterval(
      fetchExistingSession,
      $globalSettings?.game_tick_interval! * 1000 * 0.5,
    );
    dayInProgress.set(true);

    try {
      // TODO repeated code, maybe refactor?
      let result = await SessionsService.advanceSessionsTurnsPut(
        $gameSession?.id!,
      );
      gameSession.set(result);
      machineStateSnapshots.update((snapshots) => {
        snapshots[result.current_step!] = result.machine_state!;
        return snapshots;
      });
    } catch (error) {
      console.error("Error advancing day:", error);
    } finally {
      await fetchExistingSession();
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
      const result =
        await PlayerActionsService.doMaintenancePlayerActionsMaintenanceInterventionsPost(
          $gameSession!.id,
        );
      gameSession.set(result);
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

{#if !isUndefinedOrNull($gameSession)}
  <div class="session-data">
    <h3>Game Session Details</h3>
    <p>Current Step: {$gameSession?.current_step}</p>
    <p>Available Funds: {$gameSession?.available_funds}</p>
    <div class="session-commands">
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
  .session-commands {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
</style>
