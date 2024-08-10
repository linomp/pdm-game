<script lang="ts">
  import {onMount} from "svelte";
  import {Route, Router} from "svelte-navigator";
  import {GameParametersService} from "src/shared/api";
  import {globalSettings} from "src/shared/stores";
  import {isUndefinedOrNull} from "src/shared/utils";
  import HomePage from "src/components/HomePage.svelte";
  import Spinner from "src/components/Spinner.svelte";
  import Preloader from "src/components/Preloader.svelte";

  onMount(() => {
        GameParametersService.getParametersGameParametersGet()
            .then((response) => {
                globalSettings.set(response);
            })
            .catch((error) => {
                alert(
                    "Error fetching game settings or connecting to MQTT broker. Please refresh the page.",
                );
            });
    });
</script>

<svelte:head>
    <title>The Predictive Maintenance Game</title>
</svelte:head>

<Router primary={false}>
    <Preloader/>
    {#if isUndefinedOrNull($globalSettings)}
        <div class="spinner-container">
            <Spinner/>
        </div>
    {:else}
        <div>
            <Route path="/" component={HomePage}/>
        </div>
    {/if}
</Router>

<style>
    .spinner-container {
        width: 5%;
        margin: 0 auto;
    }
</style>
