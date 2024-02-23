<script lang="ts">
  import { dayInProgress, gameOver, gameSession } from "src/stores/stores";
  import { isUndefinedOrNull } from "src/shared/utils";
  import runningMachineSrc from "/img/healthy.gif";
  const stoppedMachineSrc = new URL("/img/stopped.PNG", import.meta.url).href;

  let stopAnimation = false;

  $: {
    stopAnimation = $gameOver || !$dayInProgress;
  }
</script>

<img
  class="machine-view"
  src={stopAnimation ? stoppedMachineSrc : runningMachineSrc}
  alt="..."
  width="369"
  height="276"
  hidden={isUndefinedOrNull($gameSession)}
/>
