import mqtt from "mqtt";
import type { GameSessionDTO, MqttFrontendConnectionDetails } from "src/api/generated";

export const getClient = async (connectionDetails: MqttFrontendConnectionDetails): Promise<mqtt.MqttClient> => {

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
            }
        );

        client.subscribe(`${connectionDetails.base_topic}`,
            (err) => {
                if (err) {
                    console.error("Error subscribing to topic: ", err);
                }
            }
        );

        // if (import.meta.env.VITE_DEBUG) {
        //     client.on("message", (topic, message): any => {
        //         const casted = JSON.parse(message.toString()) as GameSessionDTO;
        //         console.log(`Received message on topic ${topic}`, casted);
        //     });
        // }

        return client;

    } catch (error) {
        console.error(`Error connecting to MQTT broker ${brokerUrl}: `, error);
        throw error;
    }
}