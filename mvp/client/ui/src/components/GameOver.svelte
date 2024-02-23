<script lang="ts">
  import { gameOverReason, gameSession } from "src/stores/stores";
</script>

<h3>Game Over</h3>
<pre>{JSON.stringify($gameSession, null, 2)}</pre>
<p>{$gameOverReason}</p>
