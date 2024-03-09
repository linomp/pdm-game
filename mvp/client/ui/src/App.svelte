<script lang="ts">
  import { onMount } from "svelte";
  import { Route, Router } from "svelte-navigator";
  import { GameParametersService, OpenAPI } from "./api/generated/";
  import HomePage from "src/pages/HomePage.svelte";
  import Spinner from "src/components/graphical/Spinner.svelte";
  import { globalSettings } from "./stores/stores";
  import { isUndefinedOrNull } from "./shared/utils";

  OpenAPI.BASE = import.meta.env.VITE_API_BASE;

  onMount(async () => {
    try {
      const result =
        await GameParametersService.getParametersGameParametersGet();
      globalSettings.set(result);
    } catch (error) {
      alert("Error fetching game settings. Please refresh the page.");
    }
  });
</script>

<svelte:head>
  <title>The Predictive Maintenance Game</title>
</svelte:head>

<Router primary={false}>
  {#if isUndefinedOrNull($globalSettings)}
    <div class="spinner-container">
      <Spinner />
    </div>
  {:else}
    <div>
      <Route path="/" component={HomePage} />
    </div>
  {/if}
</Router>

<style>
  .spinner-container {
    width: 5%;
    margin: 0 auto;
  }
</style>
