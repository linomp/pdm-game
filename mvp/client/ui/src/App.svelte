<script lang="ts">
  import { onMount } from "svelte";
  import { Route, Router } from "svelte-navigator";
  import { GameParametersService, OpenAPI } from "./api/generated/";
  import { globalSettings } from "src/stores/stores";
  import { isUndefinedOrNull } from "src/shared/utils";
  import HomePage from "src/pages/HomePage.svelte";
  import Spinner from "src/components/graphical/Spinner.svelte";
  import Preloader from "src/components/Preloader.svelte";

  OpenAPI.BASE = import.meta.env.VITE_API_BASE;

  onMount(async () => {
    try {
      globalSettings.set(
        await GameParametersService.getParametersGameParametersGet(),
      );
    } catch (error) {
      alert(
        "Error fetching game settings or connecting to MQTT broker. Please refresh the page.",
      );
    }
  });
</script>

<svelte:head>
  <title>The Predictive Maintenance Game</title>
</svelte:head>

<Router primary={false}>
  <Preloader />
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
