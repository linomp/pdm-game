import mqtt from "mqtt";

export const getClient = async (): Promise<mqtt.MqttClient> => {

    const brokerUrl = import.meta.env.VITE_MQTT_HOST;

    try {

        const client = await mqtt.connectAsync(
            brokerUrl,
            {
                username: import.meta.env.VITE_MQTT_USERNAME,
                password: import.meta.env.VITE_MQTT_PASSWORD
            }
        );

        if (import.meta.env.VITE_DEBUG) {
            console.log("Connected to MQTT broker at: ", brokerUrl);
            client.subscribe(`${import.meta.env.VITE_MQTT_TOPIC_PREFIX}/test`,
                (err) => {
                    if (err) {
                        console.error("Error subscribing to topic: ", err);
                    }
                }
            );
            client.on("message", (topic, message) => {
                console.log(`Received message on topic ${topic}: ${message.toString()}`);
            });
        }

        return client;

    } catch (error) {
        console.error(`Error connecting to MQTT broker ${brokerUrl}: `, error);
        throw error;
    }
}