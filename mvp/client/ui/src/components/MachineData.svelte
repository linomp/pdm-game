<script lang="ts">
    import {isNotUndefinedNorNull} from "src/shared/utils";
    import {type GameSessionDTO, PlayerActionsService} from "src/shared/api";
    import {
        dayInProgress,
        gameOver,
        gameSession,
        globalSettings,
        isOnNarrowScreen,
        predictionPurchaseButtonDisabled,
        sensorPurchaseButtonDisabled,
    } from "src/shared/stores";
    import Sensor from "src/components/Sensor.svelte";
    import UserMessages from "src/components/UserMessages.svelte";

    export let updateGameSession: (newGameSessionDto: GameSessionDTO) => void;

    $: {
        sensorPurchaseButtonDisabled.set(
            $gameSession?.is_game_over ||
            $dayInProgress ||
            ($gameSession?.available_funds ?? 0) < $globalSettings.sensor_cost,
        );

        predictionPurchaseButtonDisabled.set(
            $gameSession?.is_game_over ||
            $dayInProgress ||
            ($gameSession?.available_funds ?? 0) <
            $globalSettings.prediction_model_cost,
        );
    }

    const purchaseSensor = async (sensorName: string) => {
        if ($gameOver) {
            return;
        }

        try {
            const newGameSessionDto =
                await PlayerActionsService.purchaseSensorPlayerActionsPurchasesSensorsPost(
                    sensorName,
                    $gameSession?.id!,
                );
            updateGameSession(newGameSessionDto);
        } catch (error: any) {
            if (error.status === 400) {
                alert(error.body.message);
            } else {
                console.error("Error buying sensor:", error);
            }
        }
    };

    const purchaseRulPredictionModel = async () => {
        if ($gameOver) {
            return;
        }

        try {
            const newGameSessionDto =
                await PlayerActionsService.purchasePredictionPlayerActionsPurchasesPredictionModelsPost(
                    "predicted_rul",
                    $gameSession?.id!,
                );
            updateGameSession(newGameSessionDto);
        } catch (error: any) {
            if (error.status === 400) {
                alert(error.body.message);
            } else {
                console.error("Error buying prediction model:", error);
            }
        }
    };
</script>

{#if isNotUndefinedNorNull($gameSession)}
    <div class="machine-data">
        {#if $isOnNarrowScreen}
            {#key 'narrow'}
                <UserMessages messages={$gameSession?.user_messages ?? {}}/>
            {/key}
        {/if}
        <div class="sensors-display">
            {#each Object.entries($gameSession?.machine_state?.operational_parameters ?? {}) as [parameter, value]}
                <Sensor
                        sensorCost={$globalSettings.sensor_cost}
                        sensorPurchaseButtonDisabled={$sensorPurchaseButtonDisabled}
                        {parameter}
                        {value}
                        {purchaseSensor}
                />
            {/each}
        </div>
        <div class="rul-display">
            <span> {"Remaining Useful Life 🔮"}: </span>
            <span>{$gameSession?.machine_state?.predicted_rul
                ? `${$gameSession.machine_state?.predicted_rul} steps`
                : "???"}
      </span>
            <span
                    hidden={isNotUndefinedNorNull(
          $gameSession?.machine_state?.predicted_rul,
        )}
            >
        <button
                disabled={$predictionPurchaseButtonDisabled}
                on:mousedown={() => purchaseRulPredictionModel()}
        >
          Buy Predictive Model (${$globalSettings.prediction_model_cost})
        </button>
      </span>
        </div>
        {#if !$isOnNarrowScreen}
            {#key 'wide'}
                <UserMessages messages={$gameSession?.user_messages ?? {}}/>
            {/key}
        {/if}
    </div>
{/if}

<style>
    .machine-data {
        display: flex;
        margin-bottom: 2em;
        position: relative;
        gap: 2em;
        align-items: center;
        flex-direction: column;
    }

    .sensors-display {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
    }

    .rul-display {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        align-items: center;
    }
</style>
