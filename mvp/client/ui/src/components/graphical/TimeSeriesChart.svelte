<script>
  import {
    Chart,
    LineSeries,
    PriceLine,
    TimeScale,
  } from "svelte-lightweight-charts";
  export let data;
</script>

<Chart width={300} height={250}>
  <LineSeries {data}>
    <!-- TODO: get the danger zone indicator value from Backend -->
    <PriceLine
      title="!"
      price={100}
      color={undefined}
      lineWidth={undefined}
      lineStyle={undefined}
      axisLabelVisible={true}
    />
  </LineSeries>
  <TimeScale timeVisible={true} secondsVisible={true} />
</Chart>
