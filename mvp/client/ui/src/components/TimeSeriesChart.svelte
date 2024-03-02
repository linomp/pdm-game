<script>
  import { Chart, LineSeries } from "svelte-lightweight-charts";
  export let data;
</script>

<Chart width={300} height={250}>
  <LineSeries {data} />
</Chart>
