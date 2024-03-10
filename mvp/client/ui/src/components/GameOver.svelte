<script lang="ts">
  import type { GameSessionWithTimeSeries } from "src/shared/types";
  import { gameOver, gameOverReason, gameSession } from "src/stores/stores";

  const formatSessionData = (session: GameSessionWithTimeSeries | null) =>
    JSON.stringify(
      {
        ...session,
        formattedTimeSeries: undefined,
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
