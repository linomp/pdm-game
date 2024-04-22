<script lang="ts">
  import {onMount} from "svelte";
  import type {HighScoreDTO} from "../api/generated/"; // TODO: maybe wrong
  import {LeaderboardService} from "../api/generated/";
  import {formatDatetime} from "src/shared/utils";

  let rows: HighScoreDTO[] = [];

    onMount(() => {
        LeaderboardService.getLeaderboardLeaderboardGet().then((data) => {
            rows = data;
        });
    });
</script>

<div class="container">
    {#if rows.length > 0}
        <h3 class="title">Leaderboard</h3>
        <table>
            <thead>
            <tr>
                <th>#</th>
                <th>Player</th>
                <th>Score</th>
                <th>Date</th>
            </tr>
            </thead>
            <tbody>
            {#each rows as row, i}
                <tr>
                    <td>{i + 1}</td>
                    <td>{row.nickname}</td>
                    <td>{row.score}</td>
                    <td>{formatDatetime(row.timestamp)}</td>
                </tr>
            {/each}
            </tbody>
        </table>
    {/if}
</div>

<style>
    .title {
        font-style: italic;
    }

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    table {
        margin-top: 1px;
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1.5em;
    }

    th,
    td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }

    th {
        background-color: #f2f2f2;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
</style>
