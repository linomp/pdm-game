<script lang="ts">
  import {
    RUNNING_MACHINE_SRC,
    STOPPED_MACHINE_SRC,
  } from "src/shared/constants";
</script>

<img
  class="preload-image"
  src={RUNNING_MACHINE_SRC}
  alt="loading gif..."
  width="0"
  height="0"
  hidden={true}
/>

<img
  class="preload-image"
  src={STOPPED_MACHINE_SRC}
  alt="loading gif..."
  width="0"
  height="0"
  hidden={true}
/>
