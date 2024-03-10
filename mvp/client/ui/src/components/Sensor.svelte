<script lang="ts">
  import { isUndefinedOrNull } from "src/shared/utils";
  import TimeSeriesChart from "./graphical/TimeSeriesChart.svelte";
  import type { TimeSeriesPoint } from "src/shared/types";
  import { gameSession } from "src/stores/stores";

  export let parameter: string;
  export let value: number | null;
  export let sensorPurchaseButtonDisabled: boolean;
  export let purchaseSensor: (parameter: string) => void;
  export let sensorCost: number;

  export let data: TimeSeriesPoint[];
  export let warningLevel: number;

  const formatParameterName = (parameter: string) => {
    return parameter
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  // TODO: instead of rerendering the whole chart, update the data using a ref like in this example:
  // https://svelte.dev/repl/c06c05db84a0466199ddd40c6622903c?version=4.2.12
</script>

<div class="sensor">
  <div class="title">
    {formatParameterName(parameter)}
  </div>
  <div class="display">
    {#if isUndefinedOrNull(value)}
      <button
        disabled={sensorPurchaseButtonDisabled}
        on:click={() => purchaseSensor(parameter)}
      >
        Buy (${sensorCost})
      </button>
    {:else}
      {#key `${$gameSession?.current_step}-${value}`}
        <TimeSeriesChart {data} {warningLevel} />
      {/key}
    {/if}
  </div>
</div>

<style>
  .sensor {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 1em;
  }
  .title {
    margin-bottom: 0.5em;
  }
  .display {
    margin-bottom: 2em;
  }
</style>
