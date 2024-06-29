<script lang="ts">
  import {onMount} from "svelte";
  import {Chart, LineSeries, PriceLine, TimeScale} from "svelte-lightweight-charts";
  import type {TimeSeriesPoint} from "src/shared/types";

  export let data: TimeSeriesPoint[];
  export let warningLevel: number;

  let chartWidth: number;
  let chartHeight: number;

  const setChartDimensions = () => {
    if (window.innerWidth <= 950) {  // Mobile breakpoint
      chartWidth = 320;
      chartHeight = 100;
    } else {
      chartWidth = 280;
      chartHeight = 250;
    }
  };

  onMount(() => {
    setChartDimensions();
    window.addEventListener("resize", setChartDimensions);
    return () => window.removeEventListener("resize", setChartDimensions);
  });
</script>

<Chart width={chartWidth} height={chartHeight}>
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
