<script>
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  export let data;
</script>

<Chart width={200} height={200}>
  <LineSeries {data} />
</Chart>
