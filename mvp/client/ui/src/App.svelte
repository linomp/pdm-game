<script lang="ts">
  import { Route, Router } from "svelte-navigator";
  import HomePage from "src/pages/HomePage.svelte";
  import { onMount } from "svelte";
  import { GameParametersService } from "./api/generated/services/GameParametersService";
  import { OpenAPI } from "./api/generated/core/OpenAPI";

  OpenAPI.BASE = import.meta.env.VITE_API_BASE;

  onMount(async () => {
    try {
      let globalSettings =
        await GameParametersService.getParametersGameParametersGet();
      console.log("API works!", globalSettings);
    } catch (error) {
      console.error("Error fetching global settings:", error);
    }
  });
</script>

<svelte:head>
  <title>The Predictive Maintenance Game</title>
</svelte:head>

<Router primary={false}>
  <div>
    <Route path="/" component={HomePage} />
  </div>
</Router>
