<script lang="ts">
  import type { GameSessionWithStateSnapshots } from "src/shared/types";
  import { gameOver, gameOverReason, gameSession } from "src/stores/stores";

  const formatSessionData = (session: GameSessionWithStateSnapshots | null) =>
    JSON.stringify(
      {
        ...session,
        machineStateSnapshots: undefined,
        formattedTimeseries: undefined,
      },
      null,
      2,
    );
</script>

{#if $gameOver}
  <h3>Game Over</h3>
  <pre>{formatSessionData($gameSession)}</pre>
  <p>{$gameOverReason}</p>
{/if}
