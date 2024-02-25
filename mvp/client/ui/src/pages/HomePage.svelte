<script lang="ts">
  import { SessionsService, type GameSessionDTO } from "../api/generated";
  import { isNotUndefinedNorNull, isUndefinedOrNull } from "src/shared/utils";
  import GameOver from "src/components/GameOver.svelte";
  import MachineView from "src/components/MachineView.svelte";
  import SessionData from "src/components/SessionData.svelte";
  import MachineData from "src/components/MachineData.svelte";
  import {
    gameOver,
    gameOverReason,
    gameSession,
    globalSettings,
  } from "src/stores/stores";

  const startSession = async () => {
    try {
      const newGameSessionDto =
        await SessionsService.createSessionSessionsPost();
      updateGameSession(newGameSessionDto);
    } catch (error) {
      console.error("Error fetching session:", error);
    }
  };

  const updateGameSession = (newGameSessionDto: GameSessionDTO) => {
    gameSession.update((previousGameSession) => {
      if (isNotUndefinedNorNull(previousGameSession)) {
        previousGameSession!.machineStateSnapshots[
          newGameSessionDto.current_step
        ] = newGameSessionDto.machine_state!;
      }

      return {
        ...newGameSessionDto,
        machineStateSnapshots: previousGameSession?.machineStateSnapshots ?? {},
      };
    });
  };

  const pollGameSession = async () => {
    if (isUndefinedOrNull($gameSession) || $gameOver) {
      return;
    }

    try {
      let newGameSessionDto = await SessionsService.getSessionSessionsGet(
        $gameSession?.id!,
      );
      updateGameSession(newGameSessionDto);
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
          {pollGameSession}
          {updateGameSession}
        />
        <MachineData {updateGameSession} />
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
