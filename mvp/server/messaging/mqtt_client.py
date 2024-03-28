import os
from datetime import datetime

import paho.mqtt.client as paho
from dotenv import load_dotenv
from paho import mqtt
from paho.mqtt.enums import CallbackAPIVersion

load_dotenv()

MQTT_HOST = os.environ.get("MQTT_HOST", "test.mosquitto.org")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_TOPIC_PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "pdmgame/clients")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"{datetime.now()}: MqttClient - connection successful")
    else:
        print(f"{datetime.now()}: MqttClient - connection failed. Code: {rc}")


class MqttClient:
    __client__: paho.Client = None

    def __init__(self):
        if MQTT_USER is None:
            return

        client = paho.Client(client_id="pdmgame_server", userdata=None, protocol=paho.MQTTv5,
                             callback_api_version=CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect

        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

        print(
            f"{datetime.now()}: MqttClient - attempting connection to {MQTT_HOST}:{MQTT_PORT} with user {MQTT_USER}"
        )

        client.connect(MQTT_HOST, MQTT_PORT)
        client.loop_start()

        self.__client__ = client

    def publish_parameter(self, client_uid: str, parameter_name: str, payload: float):
        if self.__client__ is None:
            return

        self.__client__.publish(
            f"{MQTT_TOPIC_PREFIX}/{client_uid}/{parameter_name}", payload=payload, qos=1
        )
