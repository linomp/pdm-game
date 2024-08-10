<script lang="ts">
    import {dayInProgress, gameOver, gameSession} from "src/shared/stores";
    import {isUndefinedOrNull} from "src/shared/utils";
    import {RUNNING_MACHINE_SRC, STOPPED_MACHINE_SRC,} from "src/shared/constants";

    let stopAnimation = false;

    $: {
        stopAnimation = $gameOver || !$dayInProgress;
    }
</script>

<img
        class="machine-view"
        src={stopAnimation ? STOPPED_MACHINE_SRC : RUNNING_MACHINE_SRC}
        alt="..."
        width="369"
        height="276"
        hidden={isUndefinedOrNull($gameSession)}
/>
