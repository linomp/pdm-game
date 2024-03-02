<script lang="ts">
  import { formatNumber, isUndefinedOrNull } from "src/shared/utils";
  import TimeSeriesChart from "./TimeSeriesChart.svelte";

  export let parameter: string;
  export let value: number | null;
  export let sensorPurchaseButtonDisabled: boolean;
  export let purchaseSensor: (parameter: string) => void;
  export let sensorCost: number;

  const formatParameterName = (parameter: string) => {
    return parameter
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  const data = [
    { time: "2019-04-11", value: 80.01 },
    { time: "2019-04-12", value: 96.63 },
    { time: "2019-04-13", value: 76.64 },
    { time: "2019-04-14", value: 81.89 },
    { time: "2019-04-15", value: 74.43 },
    { time: "2019-04-16", value: 80.01 },
    { time: "2019-04-17", value: 96.63 },
    { time: "2019-04-18", value: 76.64 },
    { time: "2019-04-19", value: 81.89 },
    { time: "2019-04-20", value: 74.43 },
  ];
  // TODO
  // - get the data from machine snapshots store, process and pass to the chart
  // - style HomePage as in the mockup
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
