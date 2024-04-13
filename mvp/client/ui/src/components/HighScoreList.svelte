<!-- LeaderboardService: do a call and put the results into a table -->
<script lang="ts">
  import {onMount} from "svelte";
  import type {HighScoreDTO} from "../api/generated/"; // TODO: maybe wrong
  import {LeaderboardService} from "../api/generated/";

  let scores: HighScoreDTO[] = [];

  onMount(() => {
    LeaderboardService.getLeaderboardLeaderboardGet().then((data) => {
      scores = data;
    });
  });
</script>

<table>
  <thead>
  <tr>
    <!--  rename the table headers to match the modelnickname: string;
        score: number;
        timestamp: string;  -->

    <th>Nickname</th>
    <th>Score</th>
    <th>Date</th>
  </tr>
  </thead>
  <tbody>
  {#each scores as score}
    <tr>
      <td>{score.nickname}</td>
      <td>{score.score}</td>
      <td>{score.timestamp}</td>
    </tr>
  {/each}
  </tbody>
</table>

<style>
  table {
    margin-top: 10px;
    width: 100%;
    border-collapse: collapse;
  }

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #f2f2f2;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
</style>
