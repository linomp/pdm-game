<script lang="ts">
  import { gameOver, gameOverReason, gameSession } from "src/stores/stores";

  const gameSessionWithoutStateSnapshots = {
    ...$gameSession,
    machineStateSnapshots: undefined,
  };
</script>

{#if $gameOver}
  <h3>Game Over</h3>
  <pre>{JSON.stringify(gameSessionWithoutStateSnapshots, null, 2)}</pre>
  <p>{$gameOverReason}</p>
{/if}
