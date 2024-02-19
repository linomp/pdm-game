<script lang="ts">
  export let currentStep: number;
  export let availableFunds: number;
  export let maintenanceCost: number;
  export let dayInProgress: boolean;
  export let maintenanceButtonDisabled: boolean;
  export let advanceToNextDay: () => void;
  export let doMaintenance: () => void;
</script>

<div class="session-data">
  <h3>Game Session Details</h3>
  <p>Current Step: {currentStep}</p>
  <p>Available Funds: {availableFunds}</p>
  <div class="session-commands">
    <button on:click={advanceToNextDay} disabled={dayInProgress}>
      Advance to next day
    </button>
    <button on:click={doMaintenance} disabled={maintenanceButtonDisabled}>
      Perform Maintenance (${maintenanceCost})
    </button>
  </div>
</div>

<style>
  .session-commands {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
</style>
