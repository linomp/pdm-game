import mqtt from "mqtt";

export const getClient = async (): Promise<mqtt.MqttClient> => {

    const brokerUrl = "wss://test.mosquitto.org:8081/mqtt";//import.meta.env.VITE_MQTT_BROKER_URL;

    try {
        const client = await mqtt.connectAsync(brokerUrl);
        if (import.meta.env.VITE_DEBUG) {
            console.log("Connected to MQTT broker at: ", brokerUrl);
            client.subscribe("pdmgame/clients/test");
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