<script lang="ts">
  import { getClient } from "src/messaging/mqttFunctions";
  import { SessionsService, type GameSessionDTO } from "../api/generated";
  import { isUndefinedOrNull } from "src/shared/utils";
  import { gameSession, mqttClient } from "src/stores/stores";

  export let updateGameSession: (newGameSessionDto: GameSessionDTO) => void;
  export let checkForGameOver: () => void;

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

      // Build MQTT client
      mqttClient.set(await getClient(mqttConnectionDetails));
      $mqttClient.on("message", (topic, message): any => {
        const casted = JSON.parse(message.toString()) as GameSessionDTO;
        //console.log(`Received message on topic ${topic}`, casted);
        updateGameSession(casted);
      });
    } catch (error) {
      console.error("Error fetching session:", error);
    }
  };
</script>

{#if isUndefinedOrNull($gameSession)}
  <button class="start-session-btn" on:click={startSession}>
    Start Session
  </button>
{/if}

<style>
  .start-session-btn {
    max-width: fit-content;
  }
</style>
