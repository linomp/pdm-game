<script lang="ts">
  import type { GameSessionDTO } from "src/api/generated";

  export let gameSession: GameSessionDTO;
  export let gameOverReason: string;
</script>

<h3>Game Over</h3>
<pre>{JSON.stringify(gameSession, null, 2)}</pre>
<p>{gameOverReason}</p>
