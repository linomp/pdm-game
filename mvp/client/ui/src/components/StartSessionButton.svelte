<script lang="ts">
  import { SessionsService, type GameSessionDTO } from "../api/generated";
  import { isUndefinedOrNull } from "src/shared/utils";
  import { gameSession } from "src/stores/stores";

  export let updateGameSession: (newGameSessionDto: GameSessionDTO) => void;

  const startSession = async () => {
    try {
      const newGameSessionDto =
        await SessionsService.createSessionSessionsPost();
      updateGameSession(newGameSessionDto);
    } catch (error) {
      console.error("Error fetching session:", error);
    }
  };
</script>

{#if isUndefinedOrNull($gameSession)}
  <button class="start-session-btn" on:click={startSession}>
    Start Session
  </button>
{/if}

<style>
  .start-session-btn {
    max-width: fit-content;
  }
</style>
