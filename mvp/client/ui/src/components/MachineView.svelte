<script lang="ts">
  import runningMachineSrc from "/img/healthy.gif";
  const stoppedMachineSrc = new URL("/img/stopped.PNG", import.meta.url).href;

  export let stopAnimation: boolean;
  export let hidden: boolean;
</script>

<img
  class="machine-view"
  src={stopAnimation ? stoppedMachineSrc : runningMachineSrc}
  alt="..."
  width="369"
  height="276"
  {hidden}
/>
