<script lang="ts">
    import {getUpdatedTimeseries,} from "src/shared/utils";
    import GameOver from "src/components/GameOver.svelte";
    import MachineAnimation from "src/components/MachineAnimation.svelte";
    import SessionData from "src/components/SessionData.svelte";
    import MachineData from "src/components/MachineData.svelte";
    import Lobby from "src/components/Lobby.svelte";
    import {
        gameOver,
        gameOverReason,
        gameSession,
        globalSettings,
        isOnNarrowScreen,
        mqttClient,
        mqttClientUnsubscribe,
    } from "src/shared/stores";
    import type {GameSessionWithTimeSeries} from "src/shared/types";
    import type {GameSessionDTO} from "src/shared/api";
    import {MOBILE_BREAKPOINT} from "src/shared/constants";
    import {onMount} from "svelte";

    const updateGameSession = async (newGameSessionDto: GameSessionDTO) => {
        // TODO: this is a workaround to prevent the game from updating the game session if it receives an outdated one
        //       e.g. if an MQTT message arrives after the last POST request is resolved
        if (
            $gameSession &&
            ($gameSession?.is_game_over ||
                (newGameSessionDto.current_step < $gameSession?.current_step ?? 0))
        ) {
            return;
        }

        gameOver.set(newGameSessionDto.is_game_over);
        gameOverReason.set(newGameSessionDto.game_over_reason ?? null);

        if (newGameSessionDto.is_game_over) {
            if (import.meta.env.VITE_DEBUG) {
                console.log("Game over. Last known GameSessionDTO:", newGameSessionDto);
            }

            $mqttClientUnsubscribe?.();
        }

        gameSession.update(
            (
                previousGameSession: GameSessionWithTimeSeries | null,
            ): GameSessionWithTimeSeries => {
                const previousTimeSeries =
                    previousGameSession?.formattedTimeSeries ?? {};

                return {
                    ...newGameSessionDto,
                    formattedTimeSeries: getUpdatedTimeseries(
                        newGameSessionDto,
                        previousTimeSeries,
                    ),
                };
            },
        );
    };

    const cleanupGameSession = () => {
        gameSession.set(null);
        gameOver.set(false);
        gameOverReason.set(null);
        mqttClient.update(() => null!);
        mqttClientUnsubscribe.update(() => null!);
    };

    const updateNarrowScreenFlag = () => {
        isOnNarrowScreen.set(window.innerWidth <= MOBILE_BREAKPOINT);
    };

    onMount(() => {
        updateNarrowScreenFlag();
        window.addEventListener("resize", updateNarrowScreenFlag);
        return () => window.removeEventListener("resize", updateNarrowScreenFlag);
    });
</script>

<div class="homepage">
    <h2 class="title">
        <a class="title-link" href="https://github.com/linomp/pdm-game" target="_blank">
            The Predictive Maintenance Game
        </a>
    </h2>
    <Lobby {updateGameSession}/>
    <div class="game-area">
        <div class="basic-controls">
            <MachineAnimation/>
            <GameOver {cleanupGameSession}/>
            <SessionData
                    maintenanceCost={$globalSettings.maintenance_cost}
                    {updateGameSession}
            />
        </div>
        <div class="monitoring-controls">
            <MachineData {updateGameSession}/>
        </div>
    </div>
</div>

<style>
    .homepage {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .title {
        margin-bottom: 2em;
        text-align: center;
    }

    .game-area {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 2em;
        flex-wrap: wrap;
    }

    .basic-controls {
        display: flex;
        flex-direction: column;
        max-width: fit-content;
    }

    .title-link {
        text-decoration: none;
        color: inherit;
        background: none;
        border: none;
        padding: 0;
        margin: 0;
        font-size: inherit;
        font-weight: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        display: inline;
        cursor: pointer;
    }

    .title-link:hover {
        text-decoration: underline;
        color: blue;
    }
</style>
