<script lang="ts">
  import {Chart, LineSeries, PriceLine, TimeScale,} from "svelte-lightweight-charts";
  import type {TimeSeriesPoint} from "src/shared/types";

  export let data: TimeSeriesPoint[];
  export let warningLevel: number;
</script>

<Chart width={280} height={250}>
  <LineSeries {data}>
    <PriceLine
      title="!"
      price={warningLevel}
      color={undefined}
      lineWidth={undefined}
      lineStyle={undefined}
      axisLabelVisible={true}
    />
  </LineSeries>
  <TimeScale timeVisible={true} secondsVisible={true}/>
</Chart>
