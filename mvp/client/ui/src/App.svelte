<script lang="ts">
  import { onMount } from "svelte";
  import { Route, Router } from "svelte-navigator";
  import {
    GameParametersService,
    OpenAPI,
    type GameParametersDTO,
  } from "./api/generated/";
  import HomePage from "src/pages/HomePage.svelte";
  import Spinner from "src/components/Spinner.svelte";

  OpenAPI.BASE = import.meta.env.VITE_API_BASE;

  let globalSettings: GameParametersDTO | null = null;

  onMount(async () => {
    try {
      globalSettings =
        await GameParametersService.getParametersGameParametersGet();
    } catch (error) {
      alert("Error fetching game settings. Please refresh the page.");
    }
  });
</script>

<svelte:head>
  <title>The Predictive Maintenance Game</title>
</svelte:head>

<Router primary={false}>
  {#if globalSettings}
    <div>
      <Route path="/" component={HomePage} {globalSettings} />
    </div>
  {:else}
    <div class="spinner-container">
      <Spinner />
    </div>
  {/if}
</Router>

<style>
  .spinner-container {
    width: 5%;
    margin: 0 auto;
  }
</style>
