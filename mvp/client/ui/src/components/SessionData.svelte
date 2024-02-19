<script lang="ts">
  import { PlayerActionsService, type GameSessionDTO } from "src/api/generated";

  export let maintenanceCost: number;
  export let dayInProgress: boolean;
  export let maintenanceButtonDisabled: boolean;
  export let gameOver: boolean;
  export let gameSession: GameSessionDTO;
  export let setPerformedMaintenanceFlag: () => void;
  export let advanceToNextDay: () => Promise<void>;
  export let updateGameSession: (newObj: GameSessionDTO) => void;

  const doMaintenance = async () => {
    if (gameOver) {
      return;
    }

    try {
      const result =
        await PlayerActionsService.doMaintenancePlayerActionsMaintenanceInterventionsPost(
          gameSession?.id,
        );
      updateGameSession(result);
      setPerformedMaintenanceFlag();
    } catch (error: any) {
      if (error.status === 400) {
        alert("Not enough funds to perform maintenance!");
      } else {
        console.error("Error performing maintenance:", error);
      }
    }
  };
</script>

<div class="session-data">
  <h3>Game Session Details</h3>
  <p>Current Step: {gameSession.current_step}</p>
  <p>Available Funds: {gameSession.available_funds}</p>
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
