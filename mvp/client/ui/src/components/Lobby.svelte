<script lang="ts">
    import {getClient} from "src/messaging/mqttFunctions";
    import {type GameSessionDTO, SessionsService} from "../api/generated";
    import {isUndefinedOrNull} from "src/shared/utils";
    import {gameSession, mqttClient, mqttClientUnsubscribe,} from "src/stores/stores";
    import HighScoreList from "src/components/HighScoreList.svelte";

    export let updateGameSession: (newGameSessionDto: GameSessionDTO) => void;

    const startSession = async () => {
        try {
            // Get game session
            const newGameSessionDto =
                await SessionsService.createSessionSessionsPost();
            updateGameSession(newGameSessionDto);

            // Get MQTT connection details
            const mqttConnectionDetails =
                await SessionsService.getMqttConnectionDetailsSessionsMqttConnectionDetailsGet(
                    newGameSessionDto.id,
                );

            // Build & set up MQTT client
            if (isUndefinedOrNull($mqttClient)) {
                const messageHandler = async (
                    topic: string,
                    message: Buffer,
                ): Promise<void> => {
                    const casted = JSON.parse(message.toString()) as GameSessionDTO;
                    updateGameSession(casted);
                };

                const [client, unsubscribe] = await getClient(
                    mqttConnectionDetails,
                    messageHandler,
                );
                mqttClient.set(client);
                mqttClientUnsubscribe.set(unsubscribe);
            } else {
                if (import.meta.env.VITE_DEBUG) {
                    console.log("Cleaning up old subscription");
                }
            }
        } catch (error) {
            console.error("Error fetching session:", error);
        }
    };
</script>

{#if isUndefinedOrNull($gameSession)}
    <div class="lobby">
        <HighScoreList/>
        <button class="start-session-btn" on:click={startSession}>
            Play Now
        </button>
    </div>
{/if}

<style>

    .start-session-btn {
        max-width: fit-content;
        padding: 0.25em 0.5em;
        font-size: medium;
    }

    .lobby {
        display: flex;
        flex-direction: column;
        max-width: fit-content;
        align-items: center;
    }
</style>
