<script lang="ts">
  import {
    getUpdatedTimeseries,
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
    mqttClientUnsubscribe,
  } from "src/stores/stores";
  import type { GameSessionWithTimeSeries } from "src/shared/types";
  import type { GameSessionDTO } from "src/api/generated";

  const updateGameSession = async (newGameSessionDto: GameSessionDTO) => {
    // TODO: this is a workaround to prevent the game from updating the game session if it receives an outdated one
    //        e.g. if an MQTT message arrives after the last POST request is resolved
    if (
      $gameSession &&
      ($gameSession?.is_game_over ||
        (newGameSessionDto.current_step < $gameSession?.current_step ?? 0))
    ) {
      return;
    }

    gameOver.set(newGameSessionDto.is_game_over);
    gameOverReason.set(newGameSessionDto.game_over_reason ?? null);

    if (newGameSessionDto.is_game_over) {
      if (import.meta.env.VITE_DEBUG) {
        console.log("Game over. Last known GameSessionDTO:", newGameSessionDto);
      }

      $mqttClientUnsubscribe?.();
    }

    gameSession.update(
      (
        previousGameSession: GameSessionWithTimeSeries | null,
      ): GameSessionWithTimeSeries => {
        const previousTimeSeries =
          previousGameSession?.formattedTimeSeries ?? {};

        return {
          ...newGameSessionDto,
          formattedTimeSeries: getUpdatedTimeseries(
            newGameSessionDto,
            previousTimeSeries,
          ),
        };
      },
    );
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
  }

  .title {
    margin-bottom: 1em;
    text-align: center;
  }

  .game-area {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5em;
    flex-wrap: wrap;
  }

  .basic-controls {
    display: flex;
    flex-direction: column;
    max-width: fit-content;
  }
</style>
