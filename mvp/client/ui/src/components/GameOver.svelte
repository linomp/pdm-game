<script lang="ts">
  import {gameOver, gameOverReason, gameSession} from "src/stores/stores";

  let nickName = "";

    function onSubmit() {
        // TODO: generate the models for the score post endpoint
        // TODO: fastapi validation for nickname, has to contain at least 1 character and value saved to db trimmed.
        // TODO: decide what to do after: 1) update the store so that you would emulate home page. 2) show a toast as well maybe if easy
        gameSession.saveScore(nickName);
    }
</script>

{#if $gameOver}
    <h3>Game Over</h3>
    <p>{$gameOverReason}</p>
    <form on:submit|preventDefault={onSubmit}>
        <input bind:value={nickName}/>
        <button type="submit">Save your score</button>
    </form>
{/if}
