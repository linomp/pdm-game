<script lang="ts">
  import {gameOver, gameOverReason, gameSession} from "src/shared/stores";
  import {ApiError, LeaderboardService} from "src/shared/api";

  export let cleanupGameSession: () => void;
    let nickName = "";
    let submitDisabled = false;

    const onSubmit = async () => {
        if (!$gameSession?.id) {
            console.error("Game session id is not defined");
            return;
        }

        try {
            submitDisabled = true;

            await LeaderboardService.postScoreLeaderboardScorePost($gameSession?.id, {
                nickname: nickName,
            });

            if (import.meta.env.VITE_DEBUG) {
                console.log("Score submitted: ", nickName, $gameSession);
            }
            cleanupGameSession();
            nickName = "";
            // TODO: show a toast on success, if easy
        } catch (error) {
            if (error instanceof ApiError && error.status === 422) {
                alert("Nickname cannot not be empty!");
            }
        } finally {
            submitDisabled = false;
        }
    };
</script>

{#if $gameSession && $gameOver}
    <div class="container">
        <h3>Game Over</h3>
        <p>{$gameOverReason}</p>
        <form on:submit|preventDefault={onSubmit}>
            <div class="score-field">
                <label for="score">Your score:</label>
                <input value={$gameSession.final_score} disabled/>
            </div>
            <div class="nickname-field">
                <label for="nickname">Nickname:</label>
                <input bind:value={nickName} maxlength="10"/>
            </div>
            <button type="submit" disabled={submitDisabled}>Save Score</button>
        </form>
    </div>
{/if}

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1em;
    }

    form {
        display: flex;
        flex-direction: column;
    }

    .score-field > input {
        padding: 0.5rem;
        font-size: 1rem;
        border: none;
        font-weight: bold;
        color: black;
        background: white;
    }

    .nickname-field > input {
        padding: 0.5rem;
        font-size: 1rem;
        border: none;
        border-bottom: 1px solid black;
    }

    button {
        padding: 0.5rem;
        font-size: 1rem;
        margin-top: 1.5em;
    }

    .nickname-field {
        display: flex;
        flex-direction: row;
        gap: 0.5rem;
        align-items: center;
    }
</style>
