<script lang="ts">
  import { SessionsService } from "../api/generated";
  import { isUndefinedOrNull } from "src/shared/utils";
  import GameOver from "src/components/GameOver.svelte";
  import MachineView from "src/components/MachineView.svelte";
  import SessionData from "src/components/SessionData.svelte";
  import MachineData from "src/components/MachineData.svelte";
  import {
    gameOver,
    gameOverReason,
    gameSession,
    globalSettings,
    machineStateSnapshots,
  } from "src/stores/stores";

  const startSession = async () => {
    try {
      const result = await SessionsService.createSessionSessionsPost();
      gameSession.set(result);
    } catch (error) {
      console.error("Error fetching session:", error);
    }
  };

  const fetchExistingSession = async () => {
    if (isUndefinedOrNull($gameSession) || $gameOver) {
      return;
    }

    try {
      // TODO repeated code, maybe refactor?
      let result = await SessionsService.getSessionSessionsGet(
        $gameSession?.id!,
      );
      gameSession.set(result);
      machineStateSnapshots.update((snapshots) => {
        snapshots[result.current_step!] = result.machine_state!;
        return snapshots;
      });
      checkForGameOver();
    } catch (error) {
      console.error("Error fetching session:", error);
    }
  };

  const checkForGameOver = () => {
    if (isUndefinedOrNull($gameSession)) {
      return;
    }

    gameOver.set($gameSession?.is_game_over ?? false);
    gameOverReason.set($gameSession?.game_over_reason ?? null);
  };
</script>

<div>
  <h2>The Predictive Maintenance Game</h2>
  <div class="game-area">
    <MachineView />
    {#if $gameOver}
      <GameOver />
    {:else if isUndefinedOrNull($gameSession)}
      <button class="start-session-btn" on:click={startSession}>
        Start Session
      </button>
    {:else}
      <div class="game-data">
        <SessionData
          maintenanceCost={$globalSettings?.maintenance_cost ?? 0}
          {fetchExistingSession}
        />
        <MachineData />
      </div>
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
