<script lang="ts">
  import { SessionsService, type GameSessionDTO } from "../api/generated";
  import {
    getFormattedTimeseriesForParameters,
    isNotUndefinedNorNull,
    isUndefinedOrNull,
  } from "src/shared/utils";
  import GameOver from "src/components/GameOver.svelte";
  import MachineView from "src/components/graphical/MachineView.svelte";
  import SessionData from "src/components/SessionData.svelte";
  import MachineData from "src/components/MachineData.svelte";
  import StartSessionButton from "src/components/StartSessionButton.svelte";
  import {
    gameOver,
    gameOverReason,
    gameSession,
    globalSettings,
  } from "src/stores/stores";
  import type { GameSessionWithStateSnapshots } from "src/shared/types";

  const updateGameSession = (newGameSessionDto: GameSessionDTO) => {
    gameSession.update(
      (
        previousGameSession: GameSessionWithStateSnapshots | null,
      ): GameSessionWithStateSnapshots => {
        if (isNotUndefinedNorNull(previousGameSession)) {
          previousGameSession!.machineStateSnapshots[
            newGameSessionDto.current_step
          ] = newGameSessionDto.machine_state!;
        }

        return {
          ...newGameSessionDto,
          machineStateSnapshots:
            previousGameSession?.machineStateSnapshots ?? {},
          // formattedTimeseries: getFormattedTimeseriesForParameters(
          //   ["temperature", "oil_age", "mechanical_wear"],
          //   previousGameSession,
          // ),
          formattedTimeseries: getFormattedTimeseriesForParameters(
            ["temperature", "oil_age", "mechanical_wear"],
            previousGameSession?.machineStateSnapshots,
          ),
        };
      },
    );
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

<div class="homepage">
  <h2 class="title">The Predictive Maintenance Game</h2>
  <div class={isNotUndefinedNorNull($gameSession) ? "game-area" : ""}>
    <div class="basic-controls">
      <MachineView />
      <GameOver />
      <StartSessionButton {updateGameSession} />
      <SessionData
        maintenanceCost={$globalSettings.maintenance_cost}
        {pollGameSession}
        {updateGameSession}
      />
    </div>
    <div class="monitoring-controls">
      <MachineData {updateGameSession} />
    </div>
  </div>
</div>

<style>
  .homepage {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-left: 2em;
    padding-right: 2em;
  }

  .title {
    margin-bottom: 1em;
    text-align: center;
  }

  .game-area {
    display: flex;
    flex-direction: row;
    align-items: center; /* Align children (including title) to center */
    gap: 5em;
    flex-wrap: wrap;
  }

  .basic-controls {
    display: flex;
    flex-direction: column;
    max-width: fit-content;
  }
</style>
