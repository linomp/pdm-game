<script lang="ts">
  import { formatNumber, isUndefinedOrNull } from "src/shared/utils";
  import TimeSeriesChart from "./TimeSeriesChart.svelte";
  import type { TimeSeriesPoint } from "src/shared/types";

  export let parameter: string;
  export let value: number | null;
  export let sensorPurchaseButtonDisabled: boolean;
  export let purchaseSensor: (parameter: string) => void;
  export let sensorCost: number;

  export let data: TimeSeriesPoint[];

  const formatParameterName = (parameter: string) => {
    return parameter
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };
</script>

<div class="sensor">
  <div class="title">
    {formatParameterName(parameter)}
  </div>
  <small class="temp-value">
    ({formatNumber(value) ?? "???"})
  </small>
  <div class="display">
    {#if isUndefinedOrNull(value)}
      <button
        disabled={sensorPurchaseButtonDisabled}
        on:click={() => purchaseSensor(parameter)}
      >
        Buy (${sensorCost})
      </button>
    {:else}
      <TimeSeriesChart {data} />
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
  .temp-value {
    margin-bottom: 0.5em;
  }
  .display {
    margin-bottom: 2em;
  }
</style>
