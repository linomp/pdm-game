<script lang="ts">
  import {Chart, LineSeries, PriceLine, TimeScale} from "svelte-lightweight-charts";
  import type {TimeSeriesPoint} from "src/shared/types";
  import {
    TIME_SERIES_DESKTOP_HEIGHT,
    TIME_SERIES_DESKTOP_WIDTH,
    TIME_SERIES_MOBILE_HEIGHT,
    TIME_SERIES_MOBILE_WIDTH
  } from "src/shared/constants";
  import {isOnNarrowScreen} from "src/shared/stores";

  export let data: TimeSeriesPoint[];
    export let warningLevel: number;
</script>

<Chart
        width={$isOnNarrowScreen ? TIME_SERIES_MOBILE_WIDTH :  TIME_SERIES_DESKTOP_WIDTH}
        height={$isOnNarrowScreen ? TIME_SERIES_MOBILE_HEIGHT :  TIME_SERIES_DESKTOP_HEIGHT}
>
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
