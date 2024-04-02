import mqtt, { type Packet } from "mqtt";
import type { GameSessionDTO, MqttFrontendConnectionDetails } from "src/api/generated";

export const getClient = async (
    connectionDetails: MqttFrontendConnectionDetails,
    messageHandler: (
        topic: string,
        message: Buffer,
    ) => Promise<void>
): Promise<[mqtt.MqttClient, () => void]> => {

    const brokerUrl = `wss://${connectionDetails.host}:${connectionDetails.port}/mqtt`;

    try {

        if (import.meta.env.VITE_DEBUG) {
            console.log(`Connecting to MQTT broker at ${brokerUrl}`);
            console.log(`Base topic: `, connectionDetails.base_topic);
        }

        const client = await mqtt.connectAsync(
            brokerUrl,
            {
                username: connectionDetails.username,
                password: connectionDetails.password,
                protocolVersion: 4, // MQTT 3.1.1
            }
        );

        await client.subscribeAsync(`${connectionDetails.base_topic}`);

        client.on("message", async (topic, message): Promise<void> => {
            if (import.meta.env.VITE_DEBUG) {
                const casted = JSON.parse(message.toString()) as GameSessionDTO;
                console.log(`Received message on topic ${topic}`, casted);
            }
            await messageHandler(topic, message);
        });

        return [
            client,
            () => {
                if (import.meta.env.VITE_DEBUG) {
                    console.log(`Unsubscribing from topic ${connectionDetails.base_topic}`);
                }
                client.unsubscribe(`${connectionDetails.base_topic}`);
            }
        ];

    } catch (error) {
        console.error(`Error connecting to MQTT broker ${brokerUrl}: `, error);
        throw error;
    }
}