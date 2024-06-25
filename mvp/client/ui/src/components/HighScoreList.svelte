<script lang="ts">
  import {onMount} from "svelte";
  import type {HighScoreDTO} from "../api/generated/"; // TODO: maybe wrong
  import {LeaderboardService} from "../api/generated/";
  import {formatDatetime, formatNumber} from "src/shared/utils";

  let rows: HighScoreDTO[] = [];

  onMount(() => {
    LeaderboardService.getLeaderboardLeaderboardGet().then((data) => {
      rows = data;
    });
  });
</script>

<div class="container">
  {#if rows.length > 0}
    <div class="table-wrapper">
      <table>
        <thead>
        <tr>
          <th>Rank</th>
          <th>Player</th>
          <th>Score</th>
          <th>Lvl Reached</th>
          <th>Net Profit</th>
          <th>Date</th>
        </tr>
        </thead>
        <tbody>
        {#each rows as row, i}
          <tr>
            <td>#{i + 1}</td>
            <td>{row.nickname}</td>
            <td>{row.score}</td>
            <td>{row.level_reached}</td>
            <td>$ {formatNumber(row.cash_balance)}</td>
            <td>{formatDatetime(row.timestamp)}</td>
          </tr>
        {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .table-wrapper {
    width: 90%;
    overflow-x: auto;
  }

  table {
    margin-top: 1px;
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5em;
    table-layout: fixed;
  }

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
    word-wrap: break-word;
  }

  th {
    background-color: #f2f2f2;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }

  @media (max-width: 600px) {
    th,
    td {
      padding: 4px;
      font-size: 12px;
    }

    .title {
      font-size: 18px;
    }
  }
</style>
